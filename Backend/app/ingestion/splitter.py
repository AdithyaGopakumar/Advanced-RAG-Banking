"""
Controlled splitting logic for oversized knowledge chunks.
"""
import re

def controlled_split(text: str, max_size: int) -> list[str]:
    """
    Split an oversized text block into smaller segments, adhering to max_size where possible.
    Prioritizes splitting at double-newlines (paragraphs), then list items, then single newlines.
    Ensures tables are not fractured across chunks.
    
    Returns:
        List of strings representing the split chunks.
    """
    if len(text) <= max_size:
        return [text]

    # Split by double newline to preserve paragraph/block boundaries
    blocks = text.split("\n\n")
    
    chunks = []
    current_chunk = []
    current_len = 0
    
    for block in blocks:
        # +2 accounts for the "\n\n" joiner
        if current_chunk and current_len + len(block) + 2 <= max_size:
            current_chunk.append(block)
            current_len += len(block) + 2
        elif not current_chunk and len(block) <= max_size:
            current_chunk.append(block)
            current_len = len(block)
        else:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_len = 0
            
            if len(block) > max_size:
                # If a single block is too large, we must split it further.
                # If it appears to be a markdown table, do not fracture it.
                if "|---" in block or "| ---" in block:
                    chunks.append(block)
                else:
                    # Fallback to single newline split (preserves list item boundaries generally)
                    sub_blocks = block.split("\n")
                    sub_chunk = []
                    sub_len = 0
                    for line in sub_blocks:
                        if sub_chunk and sub_len + len(line) + 1 <= max_size:
                            sub_chunk.append(line)
                            sub_len += len(line) + 1
                        elif not sub_chunk and len(line) <= max_size:
                            sub_chunk.append(line)
                            sub_len = len(line)
                        else:
                            if sub_chunk:
                                chunks.append("\n".join(sub_chunk))
                            sub_chunk = [line]
                            sub_len = len(line)
                    if sub_chunk:
                        chunks.append("\n".join(sub_chunk))
            else:
                current_chunk.append(block)
                current_len = len(block)

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return [c.strip() for c in chunks if c.strip()]
