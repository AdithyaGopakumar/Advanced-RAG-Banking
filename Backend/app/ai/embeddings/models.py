"""Embedding results returned by any provider."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

EmbeddingPurpose = Literal["document", "query"]


class Embedding(BaseModel):
    """One vector and the model that produced it."""

    model_config = ConfigDict(extra="forbid")

    model: str
    purpose: EmbeddingPurpose
    vector: list[float]


class EmbeddingBatch(BaseModel):
    """Vectors in the same order as the submitted texts."""

    model_config = ConfigDict(extra="forbid")

    model: str
    purpose: EmbeddingPurpose
    embeddings: list[Embedding] = Field(default_factory=list)

    @property
    def vectors(self) -> list[list[float]]:
        return [item.vector for item in self.embeddings]
