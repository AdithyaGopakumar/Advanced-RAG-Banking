"""Turn a parsed knowledge document into retrieval chunks.

Chunk boundaries follow heading sections. Scenario and decision-guide
documents stay one chunk when they fit in the character budget, because
their sections are one decision. Tables and numbered procedures are not
split in the middle: a table stays with its introductory text, and a
procedure is split only between steps.

``CHUNK_MAX_SIZE`` is a character budget for the breadcrumb-prefixed
chunk text. It is a starting policy, not a tuned retrieval length.
"""

import re
from dataclasses import dataclass
from typing import Literal

from app.modules.knowledge.models import KnowledgeChunk, KnowledgeDocument, KnowledgeSection

ChunkType = Literal["section", "scenario", "decision_guide", "procedure", "table"]

_ORDERED_ITEM = re.compile(r"^(\d+)\.\s+\S")
_UNORDERED_ITEM = re.compile(r"^[-*+]\s+\S")
_TABLE_LINE = re.compile(r"^\|.+\|\s*$")
_RULE_LINE = re.compile(r"^-{3,}\s*$")
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")

_COHESIVE_TYPES = {
    "scenario": "scenario",
    "decision-guide": "decision_guide",
}


@dataclass
class _Piece:
    body: str
    chunk_type: ChunkType
    oversized: bool
    step_start: int | None = None
    step_end: int | None = None


@dataclass
class _Block:
    kind: str
    text: str
    step_start: int | None = None
    step_end: int | None = None


def chunk_document(
    document: KnowledgeDocument,
    *,
    max_size: int | None = None,
) -> list[KnowledgeChunk]:
    """Build deterministic chunks for one accepted knowledge document."""
    limit = _resolve_max_size(max_size)
    cohesive_type = _COHESIVE_TYPES.get(document.metadata.document_type)
    if cohesive_type is not None:
        drafts = _chunk_cohesive_document(document, cohesive_type, limit)
    else:
        drafts = _chunk_sections(document, "section", limit)
    return _assemble(document, drafts)


def _resolve_max_size(max_size: int | None) -> int:
    if max_size is None:
        from app.core.config import get_settings

        max_size = get_settings().CHUNK_MAX_SIZE
    if max_size <= 0:
        raise ValueError("Chunk size must be a positive character budget")
    return max_size


def _chunk_cohesive_document(
    document: KnowledgeDocument,
    chunk_type: str,
    max_size: int,
) -> list[tuple[KnowledgeSection | None, list[tuple[int, str]], _Piece]]:
    """Keep a scenario or decision guide whole when the budget allows."""
    breadcrumbs = [(1, document.h1)]
    body = _cohesive_body(document)
    if not body:
        return []
    if len(_render(breadcrumbs, body)) <= max_size:
        return [
            (
                None,
                breadcrumbs,
                _Piece(body=body, chunk_type=chunk_type, oversized=False),
            )
        ]
    # The guide no longer fits as one unit. Split on its own sections, but
    # keep the document type so a later stage can tell the parts belong together.
    return _chunk_sections(document, chunk_type, max_size)


def _chunk_sections(
    document: KnowledgeDocument,
    default_type: str,
    max_size: int,
) -> list[tuple[KnowledgeSection | None, list[tuple[int, str]], _Piece]]:
    drafts: list[tuple[KnowledgeSection | None, list[tuple[int, str]], _Piece]] = []
    preamble = _substantive(document.preamble)
    if preamble:
        breadcrumbs = [(1, document.h1)]
        for piece in _pieces_for_body(preamble, breadcrumbs, max_size, default_type):
            drafts.append((None, breadcrumbs, piece))

    stack: list[tuple[int, str]] = []
    for section in document.sections:
        while stack and stack[-1][0] >= section.heading_level:
            stack.pop()
        stack.append((section.heading_level, section.heading))
        root = section.heading_path[0] if section.heading_path else document.h1
        breadcrumbs = [(1, root), *stack]
        body = _substantive(section.content)
        if not body:
            continue
        for piece in _pieces_for_body(body, breadcrumbs, max_size, default_type):
            drafts.append((section, breadcrumbs, piece))
    return drafts


def _cohesive_body(document: KnowledgeDocument) -> str:
    parts: list[str] = []
    preamble = _substantive(document.preamble)
    if preamble:
        parts.append(preamble)
    for section in document.sections:
        body = _substantive(section.content)
        heading = f"{'#' * section.heading_level} {section.heading}"
        if body:
            parts.append(f"{heading}\n\n{body}")
        elif _section_has_substantive_descendant(document, section):
            parts.append(heading)
    return "\n\n".join(parts)


def _section_has_substantive_descendant(
    document: KnowledgeDocument,
    section: KnowledgeSection,
) -> bool:
    seen = False
    for candidate in document.sections:
        if candidate.section_id == section.section_id:
            seen = True
            continue
        if not seen:
            continue
        if candidate.heading_level <= section.heading_level:
            break
        if _substantive(candidate.content):
            return True
    return False


def _pieces_for_body(
    body: str,
    breadcrumbs: list[tuple[int, str]],
    max_size: int,
    default_type: ChunkType,
) -> list[_Piece]:
    if len(_render(breadcrumbs, body)) <= max_size:
        return [_Piece(body=body, chunk_type=default_type, oversized=False)]
    return _split_oversized(body, breadcrumbs, max_size, default_type)


def _split_oversized(
    body: str,
    breadcrumbs: list[tuple[int, str]],
    max_size: int,
    default_type: ChunkType,
) -> list[_Piece]:
    blocks = _parse_blocks(body)
    pieces: list[_Piece] = []
    pending: list[_Block] = []

    def flush() -> None:
        nonlocal pending
        if not pending:
            return
        pieces.append(_piece_from_blocks(pending, breadcrumbs, max_size, default_type))
        pending = []

    for block in blocks:
        if not _fits(breadcrumbs, block.text, max_size):
            flush()
            pieces.extend(_split_block(block, breadcrumbs, max_size, default_type))
            continue
        trial = pending + [block]
        if pending and not _fits(breadcrumbs, _join_blocks(trial), max_size):
            flush()
        pending.append(block)
    flush()
    return pieces or [_Piece(body=body, chunk_type=default_type, oversized=True)]


def _split_block(
    block: _Block,
    breadcrumbs: list[tuple[int, str]],
    max_size: int,
    default_type: ChunkType,
) -> list[_Piece]:
    if block.kind == "table":
        # A table that exceeds the budget is still one chunk. Splitting rows
        # would make the values ambiguous.
        return [
            _Piece(
                body=block.text,
                chunk_type="table",
                oversized=True,
            )
        ]
    if block.kind == "procedure":
        return _split_procedure(block.text, breadcrumbs, max_size)
    if block.kind == "list":
        return _split_marked_items(
            block.text,
            breadcrumbs,
            max_size,
            default_type,
            ordered=False,
        )
    return _split_paragraph(block.text, breadcrumbs, max_size, default_type)


def _split_procedure(
    text: str,
    breadcrumbs: list[tuple[int, str]],
    max_size: int,
) -> list[_Piece]:
    return _split_marked_items(text, breadcrumbs, max_size, "procedure", ordered=True)


def _split_marked_items(
    text: str,
    breadcrumbs: list[tuple[int, str]],
    max_size: int,
    chunk_type: ChunkType,
    *,
    ordered: bool,
) -> list[_Piece]:
    intro, items = _marked_items(text, ordered=ordered)
    if not items:
        return _split_paragraph(text, breadcrumbs, max_size, chunk_type)

    pieces: list[_Piece] = []
    current: list[tuple[int | None, str]] = []

    def emit(group: list[tuple[int | None, str]], *, include_intro: bool) -> None:
        if not group:
            return
        body = _join_item_group(intro if include_intro else "", group)
        steps = [step for step, _item in group if step is not None]
        pieces.append(
            _Piece(
                body=body,
                chunk_type=chunk_type,
                oversized=not _fits(breadcrumbs, body, max_size),
                step_start=steps[0] if ordered and steps else None,
                step_end=steps[-1] if ordered and steps else None,
            )
        )

    for item in items:
        trial = current + [item]
        body = _join_item_group(intro if not pieces else "", trial)
        if current and not _fits(breadcrumbs, body, max_size):
            emit(current, include_intro=not pieces)
            current = [item]
            continue
        current = trial
    emit(current, include_intro=not pieces)
    return pieces


def _split_paragraph(
    text: str,
    breadcrumbs: list[tuple[int, str]],
    max_size: int,
    chunk_type: ChunkType,
) -> list[_Piece]:
    sentences = [part for part in _SENTENCE_BOUNDARY.split(text) if part.strip()]
    if len(sentences) <= 1:
        groups = _split_on_words(text, breadcrumbs, max_size)
    else:
        groups = []
        for group in _pack_strings(sentences, breadcrumbs, max_size):
            if _fits(breadcrumbs, group, max_size):
                groups.append(group)
            else:
                groups.extend(_split_on_words(group, breadcrumbs, max_size))
    return [
        _Piece(
            body=group,
            chunk_type=chunk_type,
            oversized=not _fits(breadcrumbs, group, max_size),
        )
        for group in groups
    ]


def _pack_strings(
    parts: list[str],
    breadcrumbs: list[tuple[int, str]],
    max_size: int,
) -> list[str]:
    groups: list[str] = []
    current = ""
    for part in parts:
        candidate = part if not current else f"{current} {part}"
        if current and not _fits(breadcrumbs, candidate, max_size):
            groups.append(current)
            current = part
            continue
        current = candidate
    if current:
        groups.append(current)
    return groups


def _split_on_words(
    text: str,
    breadcrumbs: list[tuple[int, str]],
    max_size: int,
) -> list[str]:
    words = text.split()
    if not words:
        return [text]
    groups: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join([*current, word])
        if current and not _fits(breadcrumbs, trial, max_size):
            groups.append(" ".join(current))
            current = [word]
            continue
        current.append(word)
    if current:
        groups.append(" ".join(current))
    return groups or [text]


def _parse_blocks(body: str) -> list[_Block]:
    lines = body.split("\n")
    blocks: list[_Block] = []
    index = 0
    while index < len(lines):
        if not lines[index].strip():
            index += 1
            continue
        if _is_table_line(lines[index]):
            start = index
            if blocks and blocks[-1].kind == "paragraph":
                start_text = blocks[-1].text
                blocks.pop()
                table_text, index = _consume_table(lines, index)
                text = f"{start_text}\n\n{table_text}" if start_text else table_text
                blocks.append(_Block("table", text))
                continue
            table_text, index = _consume_table(lines, start)
            blocks.append(_Block("table", table_text))
            continue
        if _ORDERED_ITEM.match(lines[index].strip()) or _UNORDERED_ITEM.match(lines[index].strip()):
            ordered = _ORDERED_ITEM.match(lines[index].strip()) is not None
            kind = "procedure" if ordered else "list"
            item_text, index, first_step, last_step = _consume_marked_list(lines, index, ordered)
            intro = ""
            if blocks and blocks[-1].kind == "paragraph":
                intro = blocks.pop().text
            text = f"{intro}\n\n{item_text}" if intro else item_text
            blocks.append(_Block(kind, text, first_step, last_step))
            continue
        paragraph, index = _consume_paragraph(lines, index)
        if paragraph:
            blocks.append(_Block("paragraph", paragraph))
    return blocks


def _consume_table(lines: list[str], start: int) -> tuple[str, int]:
    index = start
    while index < len(lines):
        if _is_table_line(lines[index]):
            index += 1
            continue
        if not lines[index].strip() and index + 1 < len(lines) and _is_table_line(lines[index + 1]):
            index += 1
            continue
        break
    return "\n".join(lines[start:index]).strip("\n"), index


def _consume_marked_list(
    lines: list[str],
    start: int,
    ordered: bool,
) -> tuple[str, int, int | None, int | None]:
    index = start
    first_step: int | None = None
    last_step: int | None = None
    while index < len(lines):
        stripped = lines[index].strip()
        ordered_match = _ORDERED_ITEM.match(stripped)
        unordered_match = _UNORDERED_ITEM.match(stripped)
        if ordered and ordered_match:
            step = int(ordered_match.group(1))
            first_step = step if first_step is None else first_step
            last_step = step
            index += 1
            continue
        if not ordered and unordered_match:
            index += 1
            continue
        if stripped and (lines[index].startswith((" ", "\t"))):
            index += 1
            continue
        if not stripped:
            nxt = index + 1
            while nxt < len(lines) and not lines[nxt].strip():
                nxt += 1
            if nxt < len(lines) and _continues_list(lines[nxt], ordered):
                index = nxt
                continue
        break
    return "\n".join(lines[start:index]).strip("\n"), index, first_step, last_step


def _continues_list(line: str, ordered: bool) -> bool:
    stripped = line.strip()
    if ordered:
        return _ORDERED_ITEM.match(stripped) is not None or line.startswith((" ", "\t"))
    return _UNORDERED_ITEM.match(stripped) is not None or line.startswith((" ", "\t"))


def _consume_paragraph(lines: list[str], start: int) -> tuple[str, int]:
    index = start
    while index < len(lines) and lines[index].strip():
        if index > start and (
            _is_table_line(lines[index])
            or _ORDERED_ITEM.match(lines[index].strip())
            or _UNORDERED_ITEM.match(lines[index].strip())
        ):
            break
        index += 1
    return "\n".join(lines[start:index]).strip("\n"), index


def _marked_items(text: str, *, ordered: bool) -> tuple[str, list[tuple[int | None, str]]]:
    lines = text.split("\n")
    intro: list[str] = []
    items: list[tuple[int | None, list[str]]] = []
    for line in lines:
        stripped = line.strip()
        ordered_match = _ORDERED_ITEM.match(stripped)
        unordered_match = _UNORDERED_ITEM.match(stripped)
        starts_item = (ordered and ordered_match) or (not ordered and unordered_match)
        if starts_item:
            step = int(ordered_match.group(1)) if ordered_match else None
            items.append((step, [line]))
            continue
        if items and (not stripped or line.startswith((" ", "\t"))):
            items[-1][1].append(line)
            continue
        if not items:
            intro.append(line)
            continue
        items[-1][1].append(line)
    rendered = [
        (step, "\n".join(lines_).strip("\n"))
        for step, lines_ in items
        if "\n".join(lines_).strip()
    ]
    return "\n".join(intro).strip("\n"), rendered


def _join_item_group(intro: str, items: list[tuple[int | None, str]]) -> str:
    body = "\n".join(item for _step, item in items)
    if intro:
        return f"{intro}\n\n{body}"
    return body


def _piece_from_blocks(
    blocks: list[_Block],
    breadcrumbs: list[tuple[int, str]],
    max_size: int,
    default_type: ChunkType,
) -> _Piece:
    body = _join_blocks(blocks)
    kinds = {block.kind for block in blocks}
    if kinds == {"table"}:
        chunk_type = "table"
    elif kinds == {"procedure"}:
        chunk_type = "procedure"
    else:
        chunk_type = default_type
    steps = [block.step_start for block in blocks if block.step_start is not None]
    ends = [block.step_end for block in blocks if block.step_end is not None]
    return _Piece(
        body=body,
        chunk_type=chunk_type,
        oversized=not _fits(breadcrumbs, body, max_size),
        step_start=steps[0] if chunk_type == "procedure" and steps else None,
        step_end=ends[-1] if chunk_type == "procedure" and ends else None,
    )


def _join_blocks(blocks: list[_Block]) -> str:
    return "\n\n".join(block.text for block in blocks if block.text)


def _fits(breadcrumbs: list[tuple[int, str]], body: str, max_size: int) -> bool:
    return len(_render(breadcrumbs, body)) <= max_size


def _render(breadcrumbs: list[tuple[int, str]], body: str) -> str:
    prefix = "\n".join(f"{'#' * level} {heading}" for level, heading in breadcrumbs)
    stripped = body.strip("\n")
    if not stripped:
        return prefix
    return f"{prefix}\n\n{stripped}"


def _is_table_line(line: str) -> bool:
    return _TABLE_LINE.match(line.strip()) is not None


def _substantive(content: str) -> str:
    """Return section text worth retrieving, without surrounding blank lines."""
    stripped = content.strip("\n")
    if not stripped.strip():
        return ""
    meaningful = [
        line.strip()
        for line in stripped.splitlines()
        if line.strip() and _RULE_LINE.match(line.strip()) is None
    ]
    if not meaningful:
        return ""
    return stripped


def _assemble(
    document: KnowledgeDocument,
    drafts: list[tuple[KnowledgeSection | None, list[tuple[int, str]], _Piece]],
) -> list[KnowledgeChunk]:
    metadata = document.metadata
    chunks: list[KnowledgeChunk] = []
    for index, (section, breadcrumbs, piece) in enumerate(drafts):
        heading_path = [heading for _level, heading in breadcrumbs]
        source_location = section.source_location if section is not None else document.source_path
        chunks.append(
            KnowledgeChunk(
                chunk_id=f"{document.document_id}#c{index:04d}",
                document_id=document.document_id,
                document_version=metadata.version,
                document_type=metadata.document_type,
                document_title=document.h1,
                section_id=section.section_id if section is not None else None,
                heading_path=heading_path,
                chunk_index=index,
                chunk_type=piece.chunk_type,
                status=metadata.status,
                effective_from=metadata.effective_from,
                effective_until=metadata.effective_until,
                product=metadata.sub_category,
                jurisdiction=metadata.region,
                audience=metadata.target_audience,
                source_location=source_location,
                source_path=document.source_path,
                content=piece.body,
                text=_render(breadcrumbs, piece.body),
                oversized=piece.oversized,
                procedure_step_start=piece.step_start,
                procedure_step_end=piece.step_end,
            )
        )
    return chunks
