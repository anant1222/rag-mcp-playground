"""Request schemas for RAG endpoints"""

from pydantic import BaseModel, Field
from typing import Optional


class IngestDocumentRequest(BaseModel):
    """Request schema for document ingestion"""
    pdf_path: str = Field(..., description="Path to PDF file to ingest")

    class Config:
        json_schema_extra = {
            "example": {
                "pdf_path": "Anant_Personal_Profile_DeepDive.pdf"
            }
        }


class RAGQueryRequest(BaseModel):
    """Request schema for RAG query"""
    query: str = Field(..., min_length=1, description="User's question")
    top_k: Optional[int] = Field(3, ge=1, le=10, description="Number of top chunks to retrieve")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is Anant's experience with GenAI?",
                "top_k": 3
            }
        }


class CompareRequest(BaseModel):
    """Request schema for RAG vs non-RAG comparison"""
    query: str = Field(..., min_length=1, description="User's question")
    top_k: Optional[int] = Field(3, ge=1, le=10, description="Number of top chunks to retrieve")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is Anant's experience with GenAI?",
                "top_k": 3
            }
        }
