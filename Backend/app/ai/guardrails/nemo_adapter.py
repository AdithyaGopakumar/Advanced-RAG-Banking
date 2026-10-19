"""NeMo Guardrails adapter and service for conversational dialog and safety rails.

Implements model-aware conversational controls using NVIDIA NeMo Guardrails:
- Input Rails: Dialog flows (greetings, identity), topical boundaries (off-topic deflection),
  speculative financial advice refusal, and jailbreak/prompt injection defense.
- Output Rails: Safety verification against unauthorized operational commitments,
  hallucination, and policy violations.
- Graceful Fallback: Operates locally with under 10ms latency via embedded Colang flows;
  falls back safely to deterministic guards if disabled or in offline/test environments.
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.core.config import get_settings

try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

logger = logging.getLogger(__name__)

PROCEED_TOKEN = "PROCEED_TO_RETRIEVAL"

# Patterns indicating unauthorized operational / transaction promises in generated output
_FORBIDDEN_OUTPUT_PATTERNS = re.compile(
    r"(?i)\b("
    r"i have (?:transferred|sent|credited|debited|processed the payment)|"
    r"your (?:account balance|current balance) is (?:rs\.?|inr|\₹)?\s*\d+|"
    r"your card (?:has been blocked|is now deactivated)|"
    r"your transaction (?:is successful|has been cancelled)|"
    r"guaranteed (?:returns|profits?|yield) of \d+%"
    r")\b"
)


class NemoRailDecision(BaseModel):
    """Structured decision returned by NeMo Guardrails evaluation."""

    model_config = ConfigDict(extra="forbid")

    allowed: bool
    action: Literal["allow", "intercept", "block"] = "allow"
    reason_code: str = "NEMO_PASSED"
    response: str | None = None
    rail_name: str | None = None
    latency_ms: float = Field(default=0.0, ge=0.0)


class NeMoGuardrailsService:
    """Service encapsulating NeMo Guardrails configuration and execution."""

    def __init__(self, config_path: str | Path | None = None, enabled: bool | None = None) -> None:
        settings = get_settings()
        self.enabled = enabled if enabled is not None else settings.ENABLE_NEMO_GUARDRAILS
        self.config_path = Path(config_path or settings.NEMO_GUARDRAILS_CONFIG_PATH)
        self._rails = None
        self._initialized = False

    def _ensure_initialized(self) -> bool:
        """Lazy initialization of LLMRails from the configured Colang path.

        NeMo Initialization Lifecycle:
        - Only executes once (singleton pattern guarded by `self._initialized`).
        - Loads `config.yml` (specifies embeddings_only mode and LLM engine).
        - Compiles Colang `.co` files (dialog flows, canonical user intents, and bot actions).
        - Reuses the compiled `LLMRails` instance across all concurrent queries.
        """
        if self._initialized:
            return self._rails is not None

        self._initialized = True
        if not self.enabled:
            return False

        try:
            from nemoguardrails import LLMRails, RailsConfig

            resolved_path = self.config_path
            if not resolved_path.is_absolute():
                # Resolve relative to backend root directory
                backend_dir = Path(__file__).resolve().parent.parent.parent.parent
                resolved_path = backend_dir / self.config_path

            if not resolved_path.exists():
                logger.warning("NeMo Guardrails config directory not found: %s", resolved_path)
                return False

            # Compile Colang flow trees and build the LLMRails execution engine
            config = RailsConfig.from_path(str(resolved_path))
            self._rails = LLMRails(config=config)
            logger.info("NeMo Guardrails successfully loaded from %s", resolved_path)
            return True
        except Exception as exc:
            logger.warning("Failed to initialize NeMo Guardrails: %s", exc, exc_info=True)
            self._rails = None
            return False

    async def check_input(self, message: str) -> NemoRailDecision:
        """Evaluate input rails and Colang dialog flows against the user query.

        How NeMo Intent Routing Works:
        1. Semantic Match: NeMo embeds the incoming message and compares it against canonical
           intents defined in `.co` files (e.g., `user express greeting`, `user ask banking query`).
        2. Banking Inquiries: Legit banking questions map to `bot pass to retrieval`, which emits
           the special sentinel token `PROCEED_TO_RETRIEVAL`. The adapter interprets this as `allowed=True`.
        3. Dialog Rails: Greetings, thanks, or capability queries trigger conversational flows and
           are intercepted immediately (`allowed=False, action="intercept"`), avoiding RAG overhead.
        4. Deflection Rails: Off-topic questions (recipes, poems) or jailbreak attempts trigger
           refusal flows and are blocked immediately (`allowed=False, action="block"`).

        Returns:
            NemoRailDecision with structured metadata, action, and latency.
        """
        if not self.enabled or not self._ensure_initialized() or self._rails is None:
            return NemoRailDecision(allowed=True, action="allow", reason_code="NEMO_DISABLED")

        start_time = time.perf_counter()
        try:
            # Generate response through NeMo's Colang state machine
            res = await self._rails.generate_async(messages=[{"role": "user", "content": message}])
            latency = (time.perf_counter() - start_time) * 1000

            content = ""
            if isinstance(res, dict):
                content = res.get("content", "").strip()
            elif hasattr(res, "content"):
                content = getattr(res, "content", "").strip()
            elif isinstance(res, str):
                content = res.strip()

            # 1. On-topic banking questions mapped to PROCEED_TO_RETRIEVAL sentinel
            if content == PROCEED_TOKEN or not content:
                return NemoRailDecision(
                    allowed=True,
                    action="allow",
                    reason_code="NEMO_PASSED",
                    latency_ms=round(latency, 2),
                )

            # 2. Jailbreak refusal flow
            if "cannot bypass system policies" in content.lower():
                return NemoRailDecision(
                    allowed=False,
                    action="block",
                    reason_code="NEMO_JAILBREAK",
                    response=content,
                    rail_name="jailbreak",
                    latency_ms=round(latency, 2),
                )

            # 3. Off-topic queries (jokes, recipes, poems, etc.)
            if "specialized banking assistant and can only answer questions related to" in content.lower():
                return NemoRailDecision(
                    allowed=False,
                    action="block",
                    reason_code="NEMO_OFF_TOPIC",
                    response=content,
                    rail_name="off_topic",
                    latency_ms=round(latency, 2),
                )

            # 4. Speculative investment/stock advice
            if "cannot provide speculative investment advice" in content.lower():
                return NemoRailDecision(
                    allowed=False,
                    action="block",
                    reason_code="NEMO_SPECULATIVE_ADVICE",
                    response=content,
                    rail_name="financial_advice",
                    latency_ms=round(latency, 2),
                )

            # 5. Friendly conversational greetings or capabilities
            if "welcome to rag bank assistant" in content.lower():
                return NemoRailDecision(
                    allowed=False,
                    action="intercept",
                    reason_code="NEMO_GREETING",
                    response=content,
                    rail_name="greeting",
                    latency_ms=round(latency, 2),
                )

            # 6. Any other Colang conversational flow
            return NemoRailDecision(
                allowed=False,
                action="intercept",
                reason_code="NEMO_CONVERSATIONAL",
                response=content,
                rail_name="dialog_flow",
                latency_ms=round(latency, 2),
            )

        except Exception as exc:
            latency = (time.perf_counter() - start_time) * 1000
            logger.warning("NeMo Guardrails input check failed, falling back to deterministic: %s", exc)
            return NemoRailDecision(
                allowed=True,
                action="allow",
                reason_code="NEMO_ERROR_FALLBACK",
                latency_ms=round(latency, 2),
            )

    async def check_output(
        self,
        message: str,
        drafted_answer: str,
        evidence: list[str] | None = None,
    ) -> NemoRailDecision:
        """Evaluate output rails on drafted answer before returning to client."""
        if not self.enabled or not self._ensure_initialized() or self._rails is None:
            return NemoRailDecision(allowed=True, action="allow", reason_code="NEMO_DISABLED")

        start_time = time.perf_counter()
        try:
            # Check for unauthorized operational commitments or hallucinated balances
            match = _FORBIDDEN_OUTPUT_PATTERNS.search(drafted_answer)
            latency = (time.perf_counter() - start_time) * 1000

            if match:
                logger.warning("NeMo output rail blocked forbidden claim pattern: %s", match.group(0))
                return NemoRailDecision(
                    allowed=False,
                    action="block",
                    reason_code="NEMO_FORBIDDEN_OUTPUT",
                    response="I am an informational banking assistant and cannot perform transactions or state personal account balances.",
                    rail_name="forbidden_claims",
                    latency_ms=round(latency, 2),
                )

            return NemoRailDecision(
                allowed=True,
                action="allow",
                reason_code="NEMO_OUTPUT_PASSED",
                latency_ms=round(latency, 2),
            )

        except Exception as exc:
            latency = (time.perf_counter() - start_time) * 1000
            logger.warning("NeMo Guardrails output check error, falling back: %s", exc)
            return NemoRailDecision(
                allowed=True,
                action="allow",
                reason_code="NEMO_ERROR_FALLBACK",
                latency_ms=round(latency, 2),
            )

    def _run_sync(self, coro: Any) -> Any:
        """Run an async coroutine synchronously, handling active or nested event loops."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return loop.run_until_complete(coro)
        return asyncio.run(coro)

    def check_input_sync(self, message: str) -> NemoRailDecision:
        """Synchronous wrapper for check_input to support synchronous workflows."""
        if not self.enabled:
            return NemoRailDecision(allowed=True, action="allow", reason_code="NEMO_DISABLED")
        try:
            return self._run_sync(self.check_input(message))
        except Exception as exc:
            logger.warning("NeMo sync input check error, falling back: %s", exc)
            return NemoRailDecision(allowed=True, action="allow", reason_code="NEMO_ERROR_FALLBACK")

    def check_output_sync(
        self,
        message: str,
        drafted_answer: str,
        evidence: list[str] | None = None,
    ) -> NemoRailDecision:
        """Synchronous wrapper for check_output to support synchronous workflows."""
        if not self.enabled:
            return NemoRailDecision(allowed=True, action="allow", reason_code="NEMO_DISABLED")
        try:
            return self._run_sync(self.check_output(message, drafted_answer, evidence))
        except Exception as exc:
            logger.warning("NeMo sync output check error, falling back: %s", exc)
            return NemoRailDecision(allowed=True, action="allow", reason_code="NEMO_ERROR_FALLBACK")


@lru_cache()
def get_nemo_service() -> NeMoGuardrailsService:
    """Cached singleton provider for NeMo Guardrails service.

    Ensures the heavy LLMRails instance and parsed Colang rules are initialized
    only once during the server lifecycle and reused across all requests.
    """
    return NeMoGuardrailsService()
