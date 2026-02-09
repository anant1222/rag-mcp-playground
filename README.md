# GenAI RAG with MCP - Complete Tutorial & Implementation

A production-ready FastAPI application demonstrating **Retrieval-Augmented Generation (RAG)** using OpenAI embeddings, FAISS vector database, and LLM integration. This project serves as a comprehensive guide to understanding and implementing RAG systems from scratch.

> **Note**: This repository focuses on GenAI fundamentals and RAG implementation. Future MCP (Model Context Protocol) integration planned.

---

## 🎯 What is RAG?

**RAG (Retrieval-Augmented Generation)** combines information retrieval with LLM generation to provide accurate, context-aware answers by:

1. **Searching** through your documents
2. **Finding** relevant information
3. **Injecting** that information into the LLM prompt
4. **Generating** answers based on retrieved context

### Why RAG?

- ✅ **Accuracy**: Answers based on your specific documents
- ✅ **Relevance**: Finds most relevant information automatically
- ✅ **Transparency**: Can cite sources
- ✅ **Up-to-date**: Update documents without retraining LLM
- ✅ **Domain-specific**: Works with any domain knowledge

---

## 🚀 Features

### Core RAG Features
- 📄 **PDF Document Processing**: Extract and process PDF documents
- ✂️ **Intelligent Chunking**: Split documents into optimal chunks with overlap
- 🔢 **Embedding Generation**: Convert text to vectors using OpenAI embeddings
- 💾 **Vector Database**: Store and search using FAISS (local, no cloud needed)
- 🔍 **Semantic Search**: Find relevant information by meaning, not keywords
- 🤖 **LLM Integration**: Generate answers using OpenAI GPT models
- 🔄 **RAG vs Non-RAG Comparison**: Compare answers with and without context

### Production Features
- ✅ **Unified Response Format**: Consistent API responses
- ✅ **Input Validation**: Comprehensive request validation
- ✅ **Error Handling**: Robust error handling with custom exceptions
- ✅ **Timeout Management**: Configurable timeouts for all operations
- ✅ **Logging**: Structured logging throughout
- ✅ **Entity Resolution**: Smart name recognition (e.g., "Anant" → "Anant Kumar Yadav")
- ✅ **Natural Responses**: Conversational, concise answers

---

## 📋 Prerequisites

- Python 3.9+
- OpenAI API Key
- pip (Python package manager)

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd genai-rag-mcp
```

### 2. Install Dependencies

```bash
pip install -r requirement.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Timeout Configuration (in seconds)
REQUEST_TIMEOUT=30
STREAM_TIMEOUT=60

# Message Length Limits
MAX_MESSAGE_LENGTH=10000
MAX_SYSTEM_MESSAGE_LENGTH=5000
```

### 4. Create Data Directory

```bash
mkdir -p data
```

---

## 🚀 Quick Start

### 1. Start the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 2. Ingest a Document

```bash
curl -X POST "http://localhost:8000/rag/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_path": "your_document.pdf"
  }'
```

### 3. Query with RAG

```bash
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic of the document?",
    "top_k": 3
  }'
```

---

## 📚 How RAG Works - Complete Flow

### Phase 1: Document Processing (One-Time Setup)

```
┌─────────────────────────────────────────┐
│  1. Load PDF Document                    │
│     Input: your_document.pdf            │
│     Output: Raw text content            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  2. Split into Chunks                   │
│     - Size: 1000 characters             │
│     - Overlap: 200 characters           │
│     - Preserve sentence boundaries      │
│     Output: List of text chunks         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  3. Generate Embeddings                │
│     - Convert each chunk to vector      │
│     - Using OpenAI text-embedding-3-small│
│     - Dimension: 1536 numbers           │
│     Output: Vector embeddings           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  4. Store in Vector Database (FAISS)   │
│     - Store vectors + text + metadata   │
│     - Save to disk for persistence      │
│     Output: Searchable vector index     │
└─────────────────────────────────────────┘
```

### Phase 2: Query Processing (Runtime)

```
┌─────────────────────────────────────────┐
│  5. User Query                         │
│     Input: "What is the main topic?"    │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  6. Enhance Query                      │
│     - Entity resolution                 │
│     - Query expansion                  │
│     Output: Enhanced query             │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  7. Generate Query Embedding           │
│     - Convert query to vector           │
│     - Same embedding model              │
│     Output: Query vector               │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  8. Search Vector Database             │
│     - Compare query with all vectors    │
│     - Calculate similarity scores       │
│     - Return top-K most similar        │
│     Output: Relevant chunks            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  9. Filter & Rank Context               │
│     - Filter by similarity threshold    │
│     - Rank by relevance                │
│     Output: Top-quality chunks         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  10. Build Prompt with Context          │
│      - Inject retrieved chunks          │
│      - Add instructions                │
│      Output: Enhanced prompt           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  11. Generate Answer                    │
│      - LLM processes prompt            │
│      - Generates context-aware answer  │
│      Output: Final answer              │
└─────────────────────────────────────────┘
```

---

## 🏗️ Architecture

### Project Structure

```
genai-rag-mcp/
├── app/
│   ├── config.py                 # Configuration settings
│   ├── main.py                   # Application entry point
│   │
│   ├── services/                 # Business logic
│   │   ├── document_processor.py # PDF loading & chunking
│   │   ├── embedding_service.py  # Embedding generation
│   │   ├── vector_store.py       # FAISS vector store
│   │   ├── rag_service.py       # Main RAG orchestrator
│   │   └── llm_service.py        # LLM integration
│   │
│   ├── interfaces/               # Service abstractions
│   │   └── llm_service.py       # LLM service interface
│   │
│   ├── routers/                 # API routes
│   │   ├── index.py            # Basic endpoints (/ask, /chat, /stream)
│   │   └── rag.py              # RAG endpoints
│   │
│   ├── schemas/                 # Request/Response models
│   │   ├── base.py             # Unified response format
│   │   ├── requests.py         # Request schemas
│   │   ├── responses.py        # Response schemas
│   │   ├── rag_requests.py     # RAG request schemas
│   │   └── rag_responses.py    # RAG response schemas
│   │
│   ├── middleware/              # Middleware
│   │   └── error_handler.py    # Error handling
│   │
│   └── utils/                   # Utilities
│       ├── logger.py            # Logging configuration
│       ├── exceptions.py        # Custom exceptions
│       ├── response_helpers.py  # Response helpers
│       └── prompts.py          # Prompt templates
│
├── data/                        # Vector database storage
│   ├── faiss_index             # FAISS index file
│   └── faiss_index.metadata.pkl # Metadata file
│
├── .env                         # Environment variables
├── requirement.txt              # Python dependencies
└── README.md                    # This file
```

---

## 📡 API Endpoints

### Basic LLM Endpoints

#### `POST /ask` - Simple LLM Response
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is machine learning?"}'
```

#### `POST /chat` - Chat with System Prompt
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "You are a helpful assistant.",
    "user_prompt": "Explain quantum computing"
  }'
```

#### `POST /stream` - Streaming Response
```bash
curl -X POST "http://localhost:8000/stream" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me a story"}' \
  --no-buffer
```

### RAG Endpoints

#### `POST /rag/ingest` - Ingest Document
Process and store a PDF document in the vector database.

```bash
curl -X POST "http://localhost:8000/rag/ingest" \
  -H "Content-Type: application/json" \
  -d '{"pdf_path": "document.pdf"}'
```

**Response:**
```json
{
  "message": "Document ingested successfully",
  "status_code": 200,
  "data": {
    "status": "success",
    "chunks_created": 15,
    "embeddings_generated": 15,
    "total_vectors": 15,
    "source": "document.pdf"
  }
}
```

#### `POST /rag/query` - Query with RAG
Query the system using RAG (Retrieval-Augmented Generation).

```bash
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic?",
    "top_k": 3
  }'
```

**Response:**
```json
{
  "message": "Query processed successfully",
  "status_code": 200,
  "data": {
    "answer": "The main topic is...",
    "context": ["chunk1", "chunk2", "chunk3"],
    "sources": [
      {
        "source": "document.pdf",
        "chunk_id": 5,
        "similarity_score": 0.89
      }
    ],
    "query": "What is the main topic?"
  }
}
```

#### `POST /rag/compare` - Compare RAG vs Non-RAG
Compare answers with and without RAG.

```bash
curl -X POST "http://localhost:8000/rag/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic?",
    "top_k": 3
  }'
```

**Response:**
```json
{
  "message": "Comparison completed successfully",
  "status_code": 200,
  "data": {
    "query": "What is the main topic?",
    "rag_answer": "Based on the documents...",
    "non_rag_answer": "I don't have specific information...",
    "rag_sources": [...],
    "rag_context_count": 3,
    "comparison": {
      "rag_has_sources": true,
      "rag_answer_length": 450,
      "non_rag_answer_length": 120
    }
  }
}
```

#### `GET /rag/stats` - Get Statistics
Get statistics about the vector store.

```bash
curl -X GET "http://localhost:8000/rag/stats"
```

---

## 🎓 Understanding the Components

### 1. Document Processor
- **Purpose**: Extract text from PDFs and split into chunks
- **Key Features**: Sentence boundary detection, overlap handling
- **File**: `app/services/document_processor.py`

### 2. Embedding Service
- **Purpose**: Convert text to numerical vectors
- **Model**: OpenAI `text-embedding-3-small` (1536 dimensions)
- **File**: `app/services/embedding_service.py`

### 3. Vector Store (FAISS)
- **Purpose**: Store and search vectors efficiently
- **Type**: Local FAISS index (no cloud needed)
- **File**: `app/services/vector_store.py`

### 4. RAG Service
- **Purpose**: Orchestrate the complete RAG pipeline
- **Features**: Query enhancement, context filtering, answer generation
- **File**: `app/services/rag_service.py`

---

## 🔧 Configuration

### Environment Variables

```env
# Required
OPENAI_API_KEY=your_api_key_here

# Optional (with defaults)
OPENAI_MODEL=gpt-3.5-turbo
REQUEST_TIMEOUT=30
STREAM_TIMEOUT=60
MAX_MESSAGE_LENGTH=10000
MAX_SYSTEM_MESSAGE_LENGTH=5000
```

### RAG Configuration

Default settings in `rag_service.py`:
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Embedding Model**: `text-embedding-3-small`
- **Vector Dimension**: 1536
- **Top-K Retrieval**: 3-5 chunks
- **Similarity Threshold**: 0.3

---

## 📖 Step-by-Step Tutorial

### Step 1: Prepare Your Document

Place your PDF file in the project root:
```bash
cp your_document.pdf .
```

### Step 2: Ingest the Document

```bash
curl -X POST "http://localhost:8000/rag/ingest" \
  -H "Content-Type: application/json" \
  -d '{"pdf_path": "your_document.pdf"}'
```

**What happens:**
1. PDF is loaded and text extracted
2. Text is split into chunks
3. Each chunk is converted to an embedding (1536 numbers)
4. Embeddings are stored in FAISS vector database
5. Index is saved to `data/faiss_index`

### Step 3: Query Your Documents

```bash
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key points?",
    "top_k": 3
  }'
```

**What happens:**
1. Query is enhanced (entity resolution)
2. Query is converted to embedding
3. FAISS searches for similar chunks
4. Top-K chunks are filtered and ranked
5. Context is injected into prompt
6. LLM generates answer using context

### Step 4: Compare RAG vs Non-RAG

```bash
curl -X POST "http://localhost:8000/rag/compare" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the key points?"}'
```

See the difference between:
- **RAG**: Answers with document context
- **Non-RAG**: Answers without context

---

## 🎯 Key Concepts Explained

### What are Embeddings?

Embeddings are numerical representations of text meaning:
- Similar texts → Similar vectors
- Enables semantic search (meaning-based, not keyword-based)
- Example: "Backend Engineer" and "Software Developer" have similar vectors

### What is FAISS?

FAISS (Facebook AI Similarity Search):
- **Local library** (not a cloud service)
- Stores vectors efficiently
- Performs fast similarity search
- No credentials or cloud setup needed

### What is Vector Dimension?

- **Dimension** = Number of numbers in each vector
- **1536** = OpenAI's embedding model creates 1536 numbers per text
- More dimensions = More detailed representation

---

## 🔍 Example Workflow

### Complete Example

```bash
# 1. Start server
python main.py

# 2. Ingest document
curl -X POST "http://localhost:8000/rag/ingest" \
  -H "Content-Type: application/json" \
  -d '{"pdf_path": "document.pdf"}'

# 3. Query with RAG
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What technologies are mentioned?",
    "top_k": 3
  }'

# 4. Compare results
curl -X POST "http://localhost:8000/rag/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What technologies are mentioned?",
    "top_k": 3
  }'
```

---

## 🧪 Testing

### Test RAG System

1. **Ingest a document**
2. **Query with various questions**
3. **Compare RAG vs non-RAG**
4. **Check statistics**

### Expected Results

**With RAG:**
- Specific answers from your documents
- Accurate information
- Source citations
- Context-aware responses

**Without RAG:**
- Generic answers
- May say "I don't have information"
- No citations

---

## 🚧 Future Enhancements

### Planned Features
- 🔄 **MCP Integration**: Model Context Protocol support
- 📊 **Advanced Analytics**: Query performance metrics
- 🔍 **Hybrid Search**: Combine keyword + semantic search
- 📈 **Re-ranking**: LLM-based result re-ranking
- 🌐 **Multi-document Support**: Process multiple PDFs
- 🔐 **Access Control**: Document-level permissions

---

## 📚 Learning Resources

### Understanding RAG
- [RAG Flow Explanation](RAG_FLOW_EXPLANATION.md) - Complete RAG flow
- [Vector Database Explained](VECTOR_DATABASE_EXPLAINED.md) - How vector DBs work
- [FAISS Explanation](FAISS_EXPLANATION.md) - FAISS details

### Code Documentation
- [RAG Improvements](RAG_IMPROVEMENTS.md) - Optimization techniques
- [RAG Usage Guide](RAG_USAGE_GUIDE.md) - Usage examples
- [Complete Status](RAG_COMPLETE_STATUS.md) - Implementation status

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional document formats (DOCX, TXT, etc.)
- More embedding models
- Advanced chunking strategies
- Performance optimizations
- MCP integration examples

---

## 📝 License

MIT License - Feel free to use this project for learning and development.

---

## 🙏 Acknowledgments

- OpenAI for embedding and LLM APIs
- Facebook AI Research for FAISS
- FastAPI for the web framework
- PyPDF2 for PDF processing

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the documentation files
- Review the code comments

---

## 🎓 Educational Purpose

This repository is designed to:
- ✅ Teach GenAI fundamentals
- ✅ Demonstrate RAG implementation
- ✅ Show vector database usage
- ✅ Provide production-ready code
- ✅ Serve as a learning resource

**Perfect for:**
- Learning RAG from scratch
- Understanding vector databases
- Building production RAG systems
- Experimenting with GenAI

---

**Happy Learning! 🚀**
