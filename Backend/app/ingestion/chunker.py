"""
Chunking engine that dispatches to the correct strategy based on document type.
"""
from typing import Dict

from app.ingestion.strategies import (
    ChunkingStrategy,
    DecisionGuideStrategy,
    FAQStrategy,
    ScenarioStrategy,
    SemanticSectionStrategy,
)
from app.modules.knowledge.models import DocumentType, KnowledgeChunk, KnowledgeDocument

class ChunkingEngine:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self._strategies: Dict[DocumentType, ChunkingStrategy] = {
            DocumentType.FAQ: FAQStrategy(),
            DocumentType.SCENARIO: ScenarioStrategy(),
            DocumentType.DECISION_GUIDE: DecisionGuideStrategy(),
        }
        self._default_strategy = SemanticSectionStrategy()

    def process(self, document: KnowledgeDocument) -> list[KnowledgeChunk]:
        """
        Process a document and return a list of knowledge chunks.
        """
        strategy = self._strategies.get(document.metadata.document_type, self._default_strategy)
        return strategy.chunk(document, self.max_size)
