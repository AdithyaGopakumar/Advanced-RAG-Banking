"""
Normalization logic for the knowledge ingestion pipeline.
"""
from pathlib import Path

from pydantic import ValidationError

from app.modules.knowledge.identity import generate_section_id, slugify_heading
from app.modules.knowledge.models import (
    DocumentMetadata,
    DocumentProvenance,
    KnowledgeDocument,
    KnowledgeRelationship,
    KnowledgeSection,
    RelationshipType,
)


def normalize_document(
    file_path: Path,
    front_matter: dict,
    markdown_content: str,
    parsed_sections: list[tuple[str, int, str]]
) -> KnowledgeDocument:
    """
    Normalize parsed raw data into a strongly typed KnowledgeDocument.
    """
    try:
        # Extract base fields that belong directly on the document
        document_id = front_matter.pop("id")
        title = front_matter.pop("title")
        slug = front_matter.pop("slug")
        version = str(front_matter.pop("version", "1.0"))
        
        # Relationships can be flat strings or typed dicts
        related_documents = front_matter.pop("related_documents", [])
        raw_relationships = front_matter.pop("relationships", [])
        
        # The remaining front matter maps to DocumentMetadata
        metadata = DocumentMetadata(**front_matter)
        
    except KeyError as e:
        raise ValueError(f"{file_path}: Missing required field in front matter: {e}")
    except ValidationError as e:
        raise ValueError(f"{file_path}: Invalid metadata. Details: {e}")
        
    provenance = DocumentProvenance(
        source=front_matter.get("source"),
        source_location=str(file_path.as_posix()),  # Use posix path for consistency
        version=version,
    )
    
    sections = []
    position = 0
    
    # Track parent_section_id (e.g. H2 is parent of H3)
    last_section_at_level = {}
    
    for heading, level, content in parsed_sections:
        heading_slug = slugify_heading(heading)
        
        # Fallback if heading is "Root" or unslugifiable
        if not heading_slug:
            heading_slug = "root"
            
        section_id = generate_section_id(document_id, heading_slug)
        
        # Find the parent section ID.
        parent_id = None
        for l in range(level - 1, 0, -1):
            if l in last_section_at_level:
                parent_id = last_section_at_level[l]
                break
                
        section = KnowledgeSection(
            section_id=section_id,
            document_id=document_id,
            heading=heading,
            level=level,
            position=position,
            content=content,
            parent_section_id=parent_id,
        )
        sections.append(section)
        
        # Update tracking
        last_section_at_level[level] = section_id
        # Clear deeper levels
        keys_to_remove = [k for k in last_section_at_level.keys() if k > level]
        for k in keys_to_remove:
            del last_section_at_level[k]
            
        position += 1

    # Map typed relationships
    relationships = []
    for rel in raw_relationships:
        try:
            relationships.append(
                KnowledgeRelationship(
                    relationship_type=RelationshipType(rel.get("type")),
                    target_id=rel.get("target_id")
                )
            )
        except Exception as e:
            raise ValueError(f"{file_path}: Invalid relationship {rel}. Details: {e}")
    
    return KnowledgeDocument(
        document_id=document_id,
        title=title,
        slug=slug,
        metadata=metadata,
        provenance=provenance,
        content=markdown_content,
        sections=sections,
        related_documents=related_documents,
        relationships=relationships,
    )
