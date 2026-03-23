from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models.requests import ChunkMetadata


@dataclass
class ChunkDocument:
    text: str
    metadata: ChunkMetadata
    content_hash: str


def _tiktoken_len(text: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def _extract_heading_before(text: str, position: int) -> str:
    headings = list(
        re.finditer(r"^#{1,3}\s+(.+)$", text[:position], re.MULTILINE)
    )
    if headings:
        return headings[-1].group(1).strip()
    return ""


def chunk_document(text: str, metadata: ChunkMetadata) -> list[ChunkDocument]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=_tiktoken_len,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    raw_chunks = splitter.split_text(text)
    results: list[ChunkDocument] = []

    for chunk_text in raw_chunks:
        if _tiktoken_len(chunk_text) < 50:
            continue

        pos = text.find(chunk_text[:50])
        section = (
            _extract_heading_before(text, pos)
            if pos >= 0
            else metadata.section
        )

        chunk_meta = ChunkMetadata(
            chapter=metadata.chapter,
            section=section or metadata.section,
            slug=metadata.slug,
            source_url=metadata.source_url,
        )
        content_hash = hashlib.sha256(chunk_text.encode()).hexdigest()
        results.append(
            ChunkDocument(
                text=chunk_text,
                metadata=chunk_meta,
                content_hash=content_hash,
            )
        )

    return results
