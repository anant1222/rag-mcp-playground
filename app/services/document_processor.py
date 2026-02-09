"""Document processing service for PDF loading and chunking"""

from typing import List
import PyPDF2
from pathlib import Path
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DocumentProcessor:
    """Service for processing documents (PDF loading and chunking)"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize document processor

        Args:
            chunk_size: Size of each text chunk in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_pdf(self, pdf_path: str) -> str:
        """
        Load and extract text from PDF file

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text content

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF cannot be read
        """
        try:
            pdf_path_obj = Path(pdf_path)
            if not pdf_path_obj.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")

            text_content = []
            with open(pdf_path_obj, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)

                logger.info(f"Loading PDF: {pdf_path} ({total_pages} pages)")

                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        text = page.extract_text()
                        if text.strip():
                            text_content.append(f"--- Page {page_num} ---\n{text}")
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num}: {str(e)}")

            full_text = "\n\n".join(text_content)
            logger.info(f"Extracted {len(full_text)} characters from PDF")
            return full_text

        except Exception as e:
            logger.error(f"Error loading PDF: {str(e)}")
            raise ValueError(f"Failed to load PDF: {str(e)}")

    def chunk_text(self, text: str) -> List[dict]:
        """
        Split text into chunks with metadata

        Args:
            text: Text content to chunk

        Returns:
            List of chunks with metadata
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        chunks = []
        start = 0
        chunk_id = 0

        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size

            # Extract chunk
            chunk_text = text[start:end]

            # Try to end at sentence boundary
            if end < len(text):
                # Look for sentence endings
                last_period = chunk_text.rfind(".")
                last_newline = chunk_text.rfind("\n")
                last_boundary = max(last_period, last_newline)

                if last_boundary > self.chunk_size * 0.5:  # Only adjust if reasonable
                    chunk_text = chunk_text[: last_boundary + 1]
                    end = start + len(chunk_text)

            # Create chunk with metadata
            chunk_data = {
                "chunk_id": chunk_id,
                "text": chunk_text.strip(),
                "start_char": start,
                "end_char": end,
                "char_count": len(chunk_text),
            }

            chunks.append(chunk_data)
            chunk_id += 1

            # Move start position (with overlap)
            start = end - self.chunk_overlap

            # Prevent infinite loop
            if start >= len(text):
                break

        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks

    def process_pdf(self, pdf_path: str) -> List[dict]:
        """
        Complete PDF processing: load and chunk

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of chunks with metadata
        """
        text = self.load_pdf(pdf_path)
        chunks = self.chunk_text(text)

        # Add source information to each chunk
        pdf_name = Path(pdf_path).name
        for chunk in chunks:
            chunk["source"] = pdf_name
            chunk["source_path"] = pdf_path

        return chunks
