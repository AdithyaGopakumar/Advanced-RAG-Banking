"""
Markdown and YAML front matter parser for knowledge documents.
"""
import yaml
from pathlib import Path


class MissingFrontMatterError(ValueError):
    """Raised when a document lacks YAML front matter."""
    pass


class MalformedYAMLError(ValueError):
    """Raised when the YAML front matter cannot be parsed."""
    pass


def parse_knowledge_file(file_path: Path) -> tuple[dict, str]:
    """
    Parse a knowledge file into YAML front matter and Markdown content.
    
    Returns:
        tuple: (front_matter_dict, markdown_content_str)
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        raise ValueError(f"Failed to read file {file_path}: {e}")
        
    if not content.startswith("---"):
        raise MissingFrontMatterError(f"{file_path}: Missing '---' at the start of the file.")
    
    # Split by the next '---' on a newline
    parts = content.split("\n---", 1)
    if len(parts) < 2:
        raise MissingFrontMatterError(f"{file_path}: Missing closing '---' for front matter.")
    
    front_matter_str = parts[0][3:]  # Strip the leading '---'
    markdown_content = parts[1]
    
    # Strip the leading newline that follows the closing '---'
    if markdown_content.startswith("\n"):
        markdown_content = markdown_content[1:]
        
    try:
        front_matter = yaml.safe_load(front_matter_str)
    except yaml.YAMLError as e:
        raise MalformedYAMLError(f"{file_path}: Malformed YAML front matter. Details: {e}")
        
    if not isinstance(front_matter, dict):
        raise MalformedYAMLError(f"{file_path}: Front matter must be a YAML dictionary.")
        
    return front_matter, markdown_content


def extract_sections(markdown_content: str) -> list[tuple[str, int, str]]:
    """
    Stateful line scanner to extract structural sections from Markdown content.
    
    - H1 is treated as the root context (level 1).
    - H2+ are treated as subsections.
    - Preserves exact Markdown content within each section.
    - Ignores heading-like lines inside fenced code blocks.
    
    Returns:
        List of tuples: (heading_title, level, section_markdown_content)
    """
    sections = []
    
    current_heading = "Root"
    current_level = 1
    current_content_lines = []
    
    in_fenced_code_block = False
    
    for line in markdown_content.splitlines():
        # Toggle code block state
        if line.lstrip().startswith("```"):
            in_fenced_code_block = not in_fenced_code_block
            
        if not in_fenced_code_block and line.startswith("#"):
            # Check if it's an ATX heading
            parts = line.split(" ", 1)
            # Make sure all characters before space are '#'
            if len(parts) == 2 and all(c == "#" for c in parts[0]):
                level = len(parts[0])
                
                # Close the previous section
                if current_content_lines or current_heading != "Root":
                    sections.append((current_heading, current_level, "\n".join(current_content_lines)))
                
                # Start the new section
                current_heading = parts[1].strip()
                current_level = level
                current_content_lines = [line]
                continue

        current_content_lines.append(line)
        
    # Append the last section
    if current_content_lines or current_heading != "Root":
        sections.append((current_heading, current_level, "\n".join(current_content_lines)))
        
    return sections
