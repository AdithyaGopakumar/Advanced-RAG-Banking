"""Deterministic Markdown and front-matter parsing.

The section split follows the Phase 1A rule: H2–H4 headings open a new
section. The H1 is the document title check and is not itself a section.
Original Markdown inside each section is preserved.
"""

import re
from dataclasses import dataclass, field
from datetime import date, datetime

import yaml

_FRONT_MATTER = re.compile(
    r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n",
    re.DOTALL,
)
_HEADING = re.compile(r"^(#{1,6})[ \t]+(\S.*?)\s*$")
_SECTION_LEVELS = range(2, 5)


@dataclass(frozen=True)
class FrontMatterSplit:
    """Raw front matter plus the body that follows it."""

    data: dict[str, object]
    body: str
    body_start_line: int


@dataclass
class RawSection:
    """A heading section before document identity is attached."""

    heading: str
    heading_level: int
    heading_path: list[str]
    content: str
    start_line: int
    end_line: int


@dataclass
class ParsedBody:
    """Heading structure extracted from a Markdown body."""

    h1: str | None
    h1_count: int
    leading_content: str
    preamble: str
    sections: list[RawSection] = field(default_factory=list)


def split_front_matter(text: str) -> FrontMatterSplit | None:
    """Return parsed front matter, or None when the block is absent or invalid.

    A present but unreadable block is reported by raising ValueError so the
    caller can distinguish "missing" from "malformed".
    """
    if text.startswith("\ufeff"):
        text = text.removeprefix("\ufeff")

    match = _FRONT_MATTER.match(text)
    if match is None:
        if text.lstrip("\ufeff").startswith("---"):
            raise ValueError("Front matter block is not closed")
        return None

    try:
        loaded = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"Front matter is not valid YAML: {exc}") from exc

    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        raise ValueError("Front matter must be a mapping")

    body = text[match.end() :]
    body_start_line = text[: match.end()].count("\n") + 1
    return FrontMatterSplit(
        data=_normalize_metadata(loaded),
        body=body,
        body_start_line=body_start_line,
    )


def parse_body(body: str, body_start_line: int, document_title: str) -> ParsedBody:
    """Split a Markdown body into an H1 check and H2–H4 sections."""
    lines = body.splitlines(keepends=True)
    h1: str | None = None
    h1_count = 0
    h1_line_index: int | None = None
    heading_stack: list[tuple[int, str]] = []
    sections: list[RawSection] = []
    current_heading: tuple[int, str, int] | None = None
    current_lines: list[str] = []

    def close_section(end_index: int) -> None:
        nonlocal current_heading, current_lines
        if current_heading is None:
            return
        level, heading, start_index = current_heading
        content = "".join(current_lines)
        start_line = body_start_line + start_index
        end_line = start_line if not content else body_start_line + end_index - 1
        sections.append(
            RawSection(
                heading=heading,
                heading_level=level,
                heading_path=[document_title, *[item[1] for item in heading_stack]],
                content=content,
                start_line=start_line,
                end_line=end_line,
            )
        )
        current_heading = None
        current_lines = []

    for index, line in enumerate(lines):
        heading_match = _HEADING.match(line.rstrip("\r\n"))
        if heading_match is None:
            if current_heading is not None:
                current_lines.append(line)
            continue

        level = len(heading_match.group(1))
        heading = heading_match.group(2).strip()

        if level == 1:
            h1_count += 1
            if h1 is None:
                h1 = heading
                h1_line_index = index
            elif current_heading is not None:
                current_lines.append(line)
            continue

        if level not in _SECTION_LEVELS:
            if current_heading is not None:
                current_lines.append(line)
            continue

        close_section(index)
        while heading_stack and heading_stack[-1][0] >= level:
            heading_stack.pop()
        current_heading = (level, heading, index)
        heading_stack.append((level, heading))

    close_section(len(lines))

    leading_lines: list[str] = []
    preamble_lines: list[str] = []
    first_section_index = sections[0].start_line - body_start_line if sections else len(lines)
    for index, line in enumerate(lines):
        if index >= first_section_index:
            break
        if h1_line_index is None or index < h1_line_index:
            leading_lines.append(line)
        elif index > h1_line_index:
            preamble_lines.append(line)

    # Breadcrumbs follow the heading hierarchy in the body. The front matter
    # title is only a fallback when the body has no H1.
    path_root = h1 or document_title
    for section in sections:
        section.heading_path = [path_root, *section.heading_path[1:]]

    return ParsedBody(
        h1=h1,
        h1_count=h1_count,
        leading_content="".join(leading_lines),
        preamble="".join(preamble_lines),
        sections=sections,
    )


def _normalize_metadata(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        return {}
    return {str(key): _normalize_value(item) for key, item in value.items()}


def _normalize_value(value: object) -> object:
    """Convert YAML date objects to ISO strings without changing other scalars."""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _normalize_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_value(item) for item in value]
    return value
