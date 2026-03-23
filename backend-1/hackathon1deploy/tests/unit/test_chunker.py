from __future__ import annotations

from app.models.requests import ChunkMetadata
from app.services.chunker import chunk_document

META = ChunkMetadata(chapter="Week 1", section="Intro", slug="week-1/intro")


def test_long_text_produces_multiple_chunks():
    text = "This is a sentence about robotics. " * 200
    chunks = chunk_document(text, META)
    assert len(chunks) > 1


def test_short_text_returns_empty():
    chunks = chunk_document("Short.", META)
    assert chunks == []


def test_heading_assigned_to_chunks():
    text = "## ROS 2 Nodes\n\n" + "ROS 2 node content about middleware. " * 60
    chunks = chunk_document(text, META)
    assert any("ROS 2 Nodes" in c.metadata.section for c in chunks)


def test_same_text_same_hash():
    text = "Consistent content about robots. " * 100
    c1 = chunk_document(text, META)
    c2 = chunk_document(text, META)
    assert len(c1) > 0
    assert c1[0].content_hash == c2[0].content_hash


def test_chunks_have_correct_metadata():
    text = "Some content about robots and AI. " * 80
    chunks = chunk_document(text, META)
    for c in chunks:
        assert c.metadata.chapter == "Week 1"
        assert c.metadata.slug == "week-1/intro"
