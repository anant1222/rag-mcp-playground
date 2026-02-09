"""Vector store service using FAISS"""

import faiss
import numpy as np
import pickle
from typing import List, Dict, Optional
from pathlib import Path
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FAISSVectorStore:
    """FAISS-based vector store for similarity search"""

    def __init__(self, dimension: int = 1536, index_path: Optional[str] = None):
        """
        Initialize FAISS vector store

        Args:
            dimension: Dimension of embedding vectors (default: 1536 for text-embedding-3-small)
            index_path: Optional path to save/load index
        """
        self.dimension = dimension
        self.index_path = index_path
        self.index: Optional[faiss.Index] = None
        self.metadata: List[Dict] = []
        self._initialize_index()

    def _initialize_index(self):
        """Initialize or load FAISS index"""
        if self.index_path and Path(self.index_path).exists():
            self.load_index()
        else:
            # Create new index using L2 distance (Euclidean)
            self.index = faiss.IndexFlatL2(self.dimension)
            logger.info(f"Initialized new FAISS index with dimension {self.dimension}")

    def add_vectors(self, embeddings: List[List[float]], metadata: List[Dict]):
        """
        Add vectors and metadata to the index

        Args:
            embeddings: List of embedding vectors
            metadata: List of metadata dictionaries (one per embedding)

        Raises:
            ValueError: If dimensions don't match or counts don't match
        """
        if not embeddings:
            raise ValueError("Embeddings list cannot be empty")

        if len(embeddings) != len(metadata):
            raise ValueError(f"Embeddings count ({len(embeddings)}) must match metadata count ({len(metadata)})")

        # Convert to numpy array
        vectors = np.array(embeddings, dtype=np.float32)

        # Validate dimensions
        if vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Vector dimension {vectors.shape[1]} doesn't match index dimension {self.dimension}"
            )

        # Add to index
        self.index.add(vectors)

        # Store metadata
        self.metadata.extend(metadata)

        logger.info(f"Added {len(embeddings)} vectors to index. Total vectors: {self.index.ntotal}")

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """
        Search for similar vectors

        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return

        Returns:
            List of results with metadata and similarity scores
        """
        if self.index is None or self.index.ntotal == 0:
            raise ValueError("Index is empty. Please add vectors first.")

        if len(query_embedding) != self.dimension:
            raise ValueError(
                f"Query embedding dimension {len(query_embedding)} doesn't match index dimension {self.dimension}"
            )

        # Convert query to numpy array
        query_vector = np.array([query_embedding], dtype=np.float32)

        # Search
        distances, indices = self.index.search(query_vector, top_k)

        # Build results with metadata
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                result = {
                    "rank": i + 1,
                    "chunk_id": self.metadata[idx].get("chunk_id"),
                    "text": self.metadata[idx].get("text"),
                    "source": self.metadata[idx].get("source"),
                    "similarity_score": float(1 / (1 + distance)),  # Convert distance to similarity
                    "distance": float(distance),
                    "metadata": self.metadata[idx],
                }
                results.append(result)

        logger.info(f"Found {len(results)} results for query")
        return results

    def save_index(self, index_path: Optional[str] = None):
        """
        Save index and metadata to disk

        Args:
            index_path: Path to save index (uses self.index_path if not provided)
        """
        save_path = index_path or self.index_path
        if not save_path:
            raise ValueError("No index path provided")

        save_path_obj = Path(save_path)
        save_path_obj.parent.mkdir(parents=True, exist_ok=True)

        # Save FAISS index
        faiss.write_index(self.index, str(save_path_obj))

        # Save metadata
        metadata_path = save_path_obj.with_suffix(".metadata.pkl")
        with open(metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

        logger.info(f"Saved index to {save_path} and metadata to {metadata_path}")

    def load_index(self, index_path: Optional[str] = None):
        """
        Load index and metadata from disk

        Args:
            index_path: Path to load index from (uses self.index_path if not provided)
        """
        load_path = index_path or self.index_path
        if not load_path:
            raise ValueError("No index path provided")

        load_path_obj = Path(load_path)
        if not load_path_obj.exists():
            raise FileNotFoundError(f"Index file not found: {load_path}")

        # Load FAISS index
        self.index = faiss.read_index(str(load_path_obj))

        # Load metadata
        metadata_path = load_path_obj.with_suffix(".metadata.pkl")
        if metadata_path.exists():
            with open(metadata_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            logger.warning(f"Metadata file not found: {metadata_path}")
            self.metadata = []

        logger.info(f"Loaded index with {self.index.ntotal} vectors from {load_path}")

    def get_stats(self) -> Dict:
        """Get statistics about the vector store"""
        return {
            "total_vectors": self.index.ntotal if self.index else 0,
            "dimension": self.dimension,
            "index_path": self.index_path,
        }
