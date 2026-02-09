"""RAG API routes"""

from fastapi import APIRouter, Request, status
from app.schemas.rag_requests import (
    IngestDocumentRequest,
    RAGQueryRequest,
    CompareRequest,
)
from app.schemas.rag_responses import (
    IngestResponseData,
    RAGQueryResponseData,
    CompareResponseData,
)
from app.schemas.base import StandardResponse
from app.services.rag_service import get_rag_service
from app.utils.response_helpers import create_response, get_request_id
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post(
    "/ingest",
    response_model=StandardResponse[IngestResponseData],
)
async def ingest_document(
    request: Request, body: IngestDocumentRequest
) -> StandardResponse[IngestResponseData]:
    """
    Ingest a PDF document into the vector store

    - **pdf_path**: Path to PDF file (relative to project root)

    This endpoint processes the PDF, creates chunks, generates embeddings,
    and stores them in the FAISS vector database.
    """
    request_id = get_request_id(request)
    rag_service = get_rag_service()

    try:
        result = await rag_service.ingest_document(body.pdf_path)

        response_data = IngestResponseData(**result)

        return create_response(
            message="Document ingested successfully",
            status_code=status.HTTP_200_OK,
            data=response_data,
            request_id=request_id,
        )
    except Exception as e:
        logger.error(f"Error ingesting document: {str(e)}")
        return create_response(
            message=f"Failed to ingest document: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=None,
            request_id=request_id,
        )


@router.post(
    "/query",
    response_model=StandardResponse[RAGQueryResponseData],
)
async def rag_query(
    request: Request, body: RAGQueryRequest
) -> StandardResponse[RAGQueryResponseData]:
    """
    Query the RAG system with a question

    - **query**: Your question
    - **top_k**: Number of top chunks to retrieve (default: 3)

    Returns an answer generated using RAG (Retrieval-Augmented Generation).
    """
    request_id = get_request_id(request)
    rag_service = get_rag_service()

    try:
        result = await rag_service.query(body.query, top_k=body.top_k)

        # Convert sources to SourceInfo objects
        from app.schemas.rag_responses import SourceInfo
        sources = [
            SourceInfo(
                source=source["source"],
                chunk_id=source["chunk_id"],
                similarity_score=source["similarity_score"],
            )
            for source in result["sources"]
        ]

        response_data = RAGQueryResponseData(
            answer=result["answer"],
            context=result["context"],
            sources=sources,
            query=result["query"],
        )

        return create_response(
            message="Query processed successfully",
            status_code=status.HTTP_200_OK,
            data=response_data,
            request_id=request_id,
        )
    except Exception as e:
        logger.error(f"Error processing RAG query: {str(e)}")
        return create_response(
            message=f"Failed to process query: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=None,
            request_id=request_id,
        )


@router.post(
    "/compare",
    response_model=StandardResponse[CompareResponseData],
)
async def compare_rag(
    request: Request, body: CompareRequest
) -> StandardResponse[CompareResponseData]:
    """
    Compare RAG vs non-RAG answers

    - **query**: Your question
    - **top_k**: Number of top chunks to retrieve for RAG (default: 3)

    Returns both RAG and non-RAG answers for comparison.
    """
    request_id = get_request_id(request)
    rag_service = get_rag_service()

    try:
        result = await rag_service.compare_rag_vs_non_rag(body.query, top_k=body.top_k)

        # Convert sources to SourceInfo objects
        from app.schemas.rag_responses import SourceInfo
        sources = [
            SourceInfo(
                source=source["source"],
                chunk_id=source["chunk_id"],
                similarity_score=source["similarity_score"],
            )
            for source in result["rag_sources"]
        ]

        response_data = CompareResponseData(
            query=result["query"],
            rag_answer=result["rag_answer"],
            non_rag_answer=result["non_rag_answer"],
            rag_sources=sources,
            rag_context_count=result["rag_context_count"],
            comparison=result["comparison"],
        )

        return create_response(
            message="Comparison completed successfully",
            status_code=status.HTTP_200_OK,
            data=response_data,
            request_id=request_id,
        )
    except Exception as e:
        logger.error(f"Error comparing RAG vs non-RAG: {str(e)}")
        return create_response(
            message=f"Failed to compare: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=None,
            request_id=request_id,
        )


@router.get("/stats", response_model=StandardResponse[dict])
async def get_rag_stats(request: Request) -> StandardResponse[dict]:
    """
    Get statistics about the RAG system

    Returns information about the vector store including total vectors.
    """
    request_id = get_request_id(request)
    rag_service = get_rag_service()

    try:
        stats = rag_service.get_stats()

        return create_response(
            message="RAG statistics retrieved successfully",
            status_code=status.HTTP_200_OK,
            data=stats,
            request_id=request_id,
        )
    except Exception as e:
        logger.error(f"Error getting RAG stats: {str(e)}")
        return create_response(
            message=f"Failed to get stats: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=None,
            request_id=request_id,
        )
