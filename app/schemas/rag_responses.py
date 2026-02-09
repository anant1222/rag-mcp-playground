"""Response schemas for RAG endpoints"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class IngestResponseData(BaseModel):
    """Data model for document ingestion response"""
    status: str = Field(..., description="Ingestion status")
    chunks_created: int = Field(..., description="Number of chunks created")
    embeddings_generated: int = Field(..., description="Number of embeddings generated")
    total_vectors: int = Field(..., description="Total vectors in index")
    source: str = Field(..., description="Source document name")


class SourceInfo(BaseModel):
    """Source information for retrieved chunks"""
    source: str = Field(..., description="Source document name")
    chunk_id: int = Field(..., description="Chunk ID")
    similarity_score: float = Field(..., description="Similarity score")


class RAGQueryResponseData(BaseModel):
    """Data model for RAG query response"""
    answer: str = Field(..., description="Generated answer")
    context: List[str] = Field(..., description="Retrieved context chunks")
    sources: List[SourceInfo] = Field(..., description="Source information")
    query: str = Field(..., description="Original query")


class CompareResponseData(BaseModel):
    """Data model for comparison response"""
    query: str = Field(..., description="Original query")
    rag_answer: str = Field(..., description="Answer with RAG")
    non_rag_answer: str = Field(..., description="Answer without RAG")
    rag_sources: List[SourceInfo] = Field(..., description="RAG sources")
    rag_context_count: int = Field(..., description="Number of context chunks used")
    comparison: Dict = Field(..., description="Comparison metrics")
