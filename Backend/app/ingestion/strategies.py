"""
Knowledge-type-aware chunking strategies.
"""
from typing import Protocol

from app.ingestion.splitter import controlled_split
from app.modules.knowledge.identity import content_hash, generate_chunk_id
from app.modules.knowledge.models import (
    ChunkContext,
    ChunkMetadata,
    ChunkProvenance,
    ChunkType,
    KnowledgeChunk,
    KnowledgeDocument,
    KnowledgeSection,
)

class ChunkingStrategy(Protocol):
    def chunk(self, document: KnowledgeDocument, max_size: int) -> list[KnowledgeChunk]:
        """Convert a document into chunks according to the strategy."""
        ...

def _build_heading_path(section: KnowledgeSection, document: KnowledgeDocument) -> list[str]:
    path = []
    current_id = section.section_id
    while current_id:
        curr_sec = next((s for s in document.sections if s.section_id == current_id), None)
        if not curr_sec:
            break
        path.insert(0, curr_sec.heading)
        current_id = curr_sec.parent_section_id
    return path

def _create_chunk(
    doc: KnowledgeDocument,
    section: KnowledgeSection,
    text: str,
    position: int,
    chunk_type: ChunkType = ChunkType.PARAGRAPH,
    parent_chunk_id: str | None = None,
) -> KnowledgeChunk:
    section_slug = section.section_id.split("::")[-1]
    chunk_id = generate_chunk_id(doc.document_id, section_slug, position)
    
    metadata = ChunkMetadata(
        domain=doc.metadata.domain,
        category=doc.metadata.category,
        sub_category=doc.metadata.sub_category,
        document_type=doc.metadata.document_type,
        product=doc.metadata.product,
        customer_segment=doc.metadata.customer_segment,
        channel=doc.metadata.channel,
        region=doc.metadata.region,
        language=doc.metadata.language,
        keywords=doc.metadata.keywords,
        tags=doc.metadata.tags,
        search_aliases=doc.metadata.search_aliases,
        priority=doc.metadata.priority,
        authority=doc.metadata.authority,
        status=doc.metadata.status,
        confidentiality=doc.metadata.confidentiality,
        effective_from=doc.metadata.effective_from,
        effective_until=doc.metadata.effective_until,
    )
    
    provenance = ChunkProvenance(
        source=doc.provenance.source,
        document_version=doc.provenance.version,
        section=section.heading,
        source_location=doc.provenance.source_location,
    )
    
    context = ChunkContext(
        document_title=doc.title,
        heading_path=_build_heading_path(section, doc),
    )
    
    return KnowledgeChunk(
        chunk_id=chunk_id,
        document_id=doc.document_id,
        section_id=section.section_id,
        parent_chunk_id=parent_chunk_id,
        chunk_type=chunk_type,
        position=position,
        text=text,
        content_hash=content_hash(text),
        metadata=metadata,
        provenance=provenance,
        context=context,
        relationships=doc.relationships,
    )


class SemanticSectionStrategy:
    """
    Default strategy for Products, Policies, Procedures, Rules, Definitions.
    Every section becomes a chunk. Oversized sections are split.
    """
    def chunk(self, document: KnowledgeDocument, max_size: int) -> list[KnowledgeChunk]:
        chunks = []
        position = 0
        
        for section in document.sections:
            text = section.content.strip()
            if not text:
                continue
                
            segments = controlled_split(text, max_size)
            
            parent_id = None
            for idx, segment in enumerate(segments):
                chunk = _create_chunk(
                    document, section, segment, position, ChunkType.PARAGRAPH, parent_id
                )
                if idx == 0 and len(segments) > 1:
                    parent_id = chunk.chunk_id
                    
                chunks.append(chunk)
                position += 1
                
        return chunks


class FAQStrategy:
    """
    FAQ chunking strategy.
    Each section represents a Question + Answer and should remain atomic.
    """
    def chunk(self, document: KnowledgeDocument, max_size: int) -> list[KnowledgeChunk]:
        chunks = []
        position = 0
        
        for section in document.sections:
            # Skip the root overview if it's just the document title
            if section.level == 1 and len(document.sections) > 1:
                lines = section.content.strip().split("\n")
                if len(lines) <= 1:
                    continue
                
            text = section.content.strip()
            if not text:
                continue
                
            segments = controlled_split(text, max_size)
            parent_id = None
            for idx, segment in enumerate(segments):
                chunk = _create_chunk(
                    document, section, segment, position, ChunkType.FAQ_ENTRY, parent_id
                )
                if idx == 0 and len(segments) > 1:
                    parent_id = chunk.chunk_id
                chunks.append(chunk)
                position += 1
                
        return chunks


class ScenarioStrategy:
    """
    Scenario strategy.
    The entire document describes a complete thought process. It should be one chunk if possible.
    If it exceeds max_size, it is split semantically.
    """
    def chunk(self, document: KnowledgeDocument, max_size: int) -> list[KnowledgeChunk]:
        if not document.sections:
            return []
            
        full_text = "\n\n".join(s.content.strip() for s in document.sections if s.content.strip())
        segments = controlled_split(full_text, max_size)
        
        root_section = document.sections[0]
        
        chunks = []
        position = 0
        parent_id = None
        for idx, segment in enumerate(segments):
            chunk = _create_chunk(
                document, root_section, segment, position, ChunkType.PARAGRAPH, parent_id
            )
            if idx == 0 and len(segments) > 1:
                parent_id = chunk.chunk_id
            chunks.append(chunk)
            position += 1
            
        return chunks


class DecisionGuideStrategy:
    """
    Decision Guide strategy.
    Chunked at the atomic decision-rule level, typically mapped to document sections.
    """
    def chunk(self, document: KnowledgeDocument, max_size: int) -> list[KnowledgeChunk]:
        chunks = []
        position = 0
        
        for section in document.sections:
            # Similar to FAQ, skip empty roots
            if section.level == 1 and len(document.sections) > 1:
                lines = section.content.strip().split("\n")
                if len(lines) <= 1:
                    continue
                
            text = section.content.strip()
            if not text:
                continue
                
            segments = controlled_split(text, max_size)
            parent_id = None
            for idx, segment in enumerate(segments):
                chunk = _create_chunk(
                    document, section, segment, position, ChunkType.PARAGRAPH, parent_id
                )
                if idx == 0 and len(segments) > 1:
                    parent_id = chunk.chunk_id
                chunks.append(chunk)
                position += 1
                
        return chunks
