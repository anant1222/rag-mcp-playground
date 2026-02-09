"""RAG (Retrieval-Augmented Generation) service"""

from typing import List, Dict, Optional
from pathlib import Path
from app.services.document_processor import DocumentProcessor
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import FAISSVectorStore
from app.services import get_llm_service
from app.utils.logger import get_logger
from app.utils.prompts import build_rag_prompt_with_sources, enhance_query_for_entity_resolution

logger = get_logger(__name__)


class RAGService:
    """RAG service that orchestrates document processing, embedding, and retrieval"""

    def __init__(
        self,
        index_path: Optional[str] = "data/faiss_index",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        embedding_model: str = "text-embedding-3-small",
    ):
        """
        Initialize RAG service

        Args:
            index_path: Path to FAISS index storage
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            embedding_model: OpenAI embedding model name
        """
        self.document_processor = DocumentProcessor(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        self.embedding_service = EmbeddingService(model=embedding_model)
        self.vector_store = FAISSVectorStore(
            dimension=1536, index_path=index_path  # text-embedding-3-small dimension
        )
        self.llm_service = get_llm_service()
        self.index_path = index_path

    async def ingest_document(self, pdf_path: str) -> Dict:
        """
        Process and ingest a PDF document into the vector store

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with ingestion statistics
        """
        logger.info(f"Starting document ingestion: {pdf_path}")

        # Step 1: Load and chunk PDF
        chunks = self.document_processor.process_pdf(pdf_path)
        logger.info(f"Created {len(chunks)} chunks from PDF")

        # Step 2: Generate embeddings for all chunks
        texts = [chunk["text"] for chunk in chunks]
        embeddings = await self.embedding_service.generate_embeddings_batch(texts)
        logger.info(f"Generated {len(embeddings)} embeddings")

        # Step 3: Store in vector database
        self.vector_store.add_vectors(embeddings, chunks)

        # Step 4: Save index
        if self.index_path:
            self.vector_store.save_index()

        logger.info(f"Successfully ingested document: {pdf_path}")

        return {
            "status": "success",
            "chunks_created": len(chunks),
            "embeddings_generated": len(embeddings),
            "total_vectors": self.vector_store.index.ntotal,
            "source": Path(pdf_path).name,
        }

    def _filter_and_rank_context(self, results: List[Dict], min_similarity: float = 0.3) -> List[Dict]:
        """
        Filter and rank context chunks by relevance

        Args:
            results: Search results from vector store
            min_similarity: Minimum similarity score to include

        Returns:
            Filtered and ranked results
        """
        # Filter by minimum similarity
        filtered = [r for r in results if r.get("similarity_score", 0) >= min_similarity]

        # Sort by similarity score (highest first)
        filtered.sort(key=lambda x: x.get("similarity_score", 0), reverse=True)

        return filtered

    async def query(self, user_query: str, top_k: int = 5) -> Dict:
        """
        Query the RAG system with a user question

        Args:
            user_query: User's question
            top_k: Number of top chunks to retrieve

        Returns:
            Dictionary with answer and retrieved context
        """
        logger.info(f"Processing RAG query: {user_query}")

        # Step 1: Enhance query for better entity resolution
        enhanced_query = enhance_query_for_entity_resolution(user_query)
        logger.debug(f"Enhanced query: {enhanced_query}")

        # Step 2: Generate query embedding (use enhanced query for better retrieval)
        query_embedding = await self.embedding_service.generate_embedding(enhanced_query)

        # Step 3: Search vector store (retrieve more than needed for filtering)
        results = self.vector_store.search(query_embedding, top_k=top_k * 2)

        if not results:
            return {
                "answer": "I couldn't find relevant information in the documents to answer your question.",
                "context": [],
                "sources": [],
            }

        # Step 4: Filter and rank context by relevance
        filtered_results = self._filter_and_rank_context(results, min_similarity=0.3)

        # Take top_k after filtering
        top_results = filtered_results[:top_k]

        if not top_results:
            return {
                "answer": "I couldn't find relevant information in the documents to answer your question.",
                "context": [],
                "sources": [],
            }

        # Step 5: Build context from retrieved chunks
        context_chunks = [result["text"] for result in top_results]

        # Step 6: Build prompt with context (use original query for answer generation)
        prompt = build_rag_prompt_with_sources(context_chunks, user_query)

        # Step 7: Generate answer using LLM
        answer = await self.llm_service.ask(prompt)

        # Step 8: Prepare response
        sources = [
            {
                "source": result["source"],
                "chunk_id": result["chunk_id"],
                "similarity_score": result["similarity_score"],
            }
            for result in top_results
        ]

        return {
            "answer": answer,
            "context": context_chunks,
            "sources": sources,
            "query": user_query,
        }

    async def query_without_rag(self, user_query: str) -> str:
        """
        Query LLM without RAG (for comparison)

        Args:
            user_query: User's question

        Returns:
            LLM answer without context
        """
        logger.info(f"Processing query without RAG: {user_query}")
        answer = await self.llm_service.ask(user_query)
        return answer

    async def compare_rag_vs_non_rag(self, user_query: str, top_k: int = 3) -> Dict:
        """
        Compare RAG vs non-RAG answers

        Args:
            user_query: User's question
            top_k: Number of top chunks to retrieve for RAG

        Returns:
            Dictionary with both answers and comparison
        """
        logger.info(f"Comparing RAG vs non-RAG for query: {user_query}")

        # Get RAG answer
        rag_result = await self.query(user_query, top_k=top_k)

        # Get non-RAG answer
        non_rag_answer = await self.query_without_rag(user_query)

        return {
            "query": user_query,
            "rag_answer": rag_result["answer"],
            "non_rag_answer": non_rag_answer,
            "rag_sources": rag_result["sources"],
            "rag_context_count": len(rag_result["context"]),
            "comparison": {
                "rag_has_sources": len(rag_result["sources"]) > 0,
                "rag_answer_length": len(rag_result["answer"]),
                "non_rag_answer_length": len(non_rag_answer),
            },
        }

    def get_stats(self) -> Dict:
        """Get statistics about the RAG system"""
        return self.vector_store.get_stats()


# Singleton instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create RAG service instance"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
