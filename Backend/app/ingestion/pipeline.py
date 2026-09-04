"""
Orchestrator pipeline for knowledge ingestion (Phase 1A).
"""
from pathlib import Path
import logging

from app.ingestion.discovery import discover_knowledge_files
from app.ingestion.parser import parse_knowledge_file, extract_sections
from app.ingestion.normalizer import normalize_document
from app.ingestion.chunker import ChunkingEngine
from app.core.config import get_settings
from app.modules.knowledge.models import KnowledgeChunk, KnowledgeDocument

logger = logging.getLogger(__name__)

class DuplicateDocumentIDError(ValueError):
    """Raised when multiple files claim the same document ID."""
    pass

def run_ingestion(root_dir: Path) -> list[KnowledgeChunk]:
    """
    Run the ingestion pipeline on the given knowledge root directory.
    
    Returns:
        List of KnowledgeChunk objects ready for indexing.
    """
    settings = get_settings()
    md_files = discover_knowledge_files(root_dir)
    documents = []
    seen_ids = {}
    
    chunking_engine = ChunkingEngine(max_size=settings.CHUNK_MAX_SIZE)
    chunks = []
    
    for file_path in md_files:
        try:
            front_matter, markdown_content = parse_knowledge_file(file_path)
            sections = extract_sections(markdown_content)
            doc = normalize_document(file_path, front_matter, markdown_content, sections)
            
            if doc.document_id in seen_ids:
                raise DuplicateDocumentIDError(
                    f"Duplicate document ID found: '{doc.document_id}'\n"
                    f"File 1: {seen_ids[doc.document_id]}\n"
                    f"File 2: {file_path}"
                )
            
            seen_ids[doc.document_id] = file_path
            documents.append(doc)
            
            # Perform Chunking
            doc_chunks = chunking_engine.process(doc)
            chunks.extend(doc_chunks)
            
        except Exception as e:
            # The prompt requires strict failure:
            # "Do not silently recover from errors that could result in incorrect banking knowledge."
            logger.error(f"Ingestion failed for file {file_path}: {e}")
            raise

    return chunks
