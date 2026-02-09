# RAG System Usage Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirement.txt
```

### 2. Set Environment Variables

Make sure your `.env` file has:
```env
OPENAI_API_KEY=your_api_key_here
```

### 3. Start the Server

```bash
python main.py
```

---

## 📋 API Endpoints

### 1. **Ingest Document** - `POST /rag/ingest`

Process and store a PDF document in the vector database.

**Request:**
```bash
curl -X POST "http://localhost:8000/rag/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_path": "Anant_Personal_Profile_DeepDive.pdf"
  }'
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
    "source": "Anant_Personal_Profile_DeepDive.pdf"
  }
}
```

---

### 2. **Query with RAG** - `POST /rag/query`

Query the system using RAG (Retrieval-Augmented Generation).

**Request:**
```bash
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Anant's experience with GenAI?",
    "top_k": 3
  }'
```

**Response:**
```json
{
  "message": "Query processed successfully",
  "status_code": 200,
  "data": {
    "answer": "Based on the provided context, Anant has extensive experience with GenAI including...",
    "context": [
      "GenAI & LLMs: OpenAI Assistants, tool calling...",
      "Ruv AI – Agentic AI Platform: Implemented...",
      "Led internal Generative AI training sessions..."
    ],
    "sources": [
      {
        "source": "Anant_Personal_Profile_DeepDive.pdf",
        "chunk_id": 5,
        "similarity_score": 0.89
      }
    ],
    "query": "What is Anant's experience with GenAI?"
  }
}
```

---

### 3. **Compare RAG vs Non-RAG** - `POST /rag/compare`

Compare answers with and without RAG.

**Request:**
```bash
curl -X POST "http://localhost:8000/rag/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Anant's experience with GenAI?",
    "top_k": 3
  }'
```

**Response:**
```json
{
  "message": "Comparison completed successfully",
  "status_code": 200,
  "data": {
    "query": "What is Anant's experience with GenAI?",
    "rag_answer": "Based on the provided context, Anant has extensive experience...",
    "non_rag_answer": "I don't have specific information about Anant's experience...",
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

---

### 4. **Get RAG Stats** - `GET /rag/stats`

Get statistics about the vector store.

**Request:**
```bash
curl -X GET "http://localhost:8000/rag/stats"
```

**Response:**
```json
{
  "message": "RAG statistics retrieved successfully",
  "status_code": 200,
  "data": {
    "total_vectors": 15,
    "dimension": 1536,
    "index_path": "data/faiss_index"
  }
}
```

---

## 🔄 Complete Workflow

### Step 1: Ingest Your PDF

```bash
curl -X POST "http://localhost:8000/rag/ingest" \
  -H "Content-Type: application/json" \
  -d '{"pdf_path": "Anant_Personal_Profile_DeepDive.pdf"}'
```

### Step 2: Query with RAG

```bash
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Anant's experience with GenAI?",
    "top_k": 3
  }'
```

### Step 3: Compare RAG vs Non-RAG

```bash
curl -X POST "http://localhost:8000/rag/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Anant's experience with GenAI?",
    "top_k": 3
  }'
```

---

## 📊 Expected Comparison Results

### Query: "What is Anant's experience with GenAI?"

**Without RAG:**
- Generic answer
- No specific details
- May say "I don't have information"

**With RAG:**
- Specific details from PDF
- Cites relevant sections
- Accurate information about:
  - OpenAI Assistants
  - Tool calling
  - RAG pipelines
  - Multi-agent orchestration
  - Training sessions

---

## 🎯 Testing Examples

### Example 1: Experience Query
```json
{
  "query": "What is Anant's backend engineering experience?",
  "top_k": 3
}
```

### Example 2: Project Query
```json
{
  "query": "Tell me about the Ruv AI project",
  "top_k": 3
}
```

### Example 3: Skills Query
```json
{
  "query": "What technologies does Anant work with?",
  "top_k": 5
}
```

---

## 📁 File Structure

```
python_AI/
├── app/
│   ├── services/
│   │   ├── document_processor.py  # PDF loading & chunking
│   │   ├── embedding_service.py   # Embedding generation
│   │   ├── vector_store.py        # FAISS vector store
│   │   └── rag_service.py         # Main RAG orchestrator
│   ├── routers/
│   │   └── rag.py                 # RAG API endpoints
│   └── schemas/
│       ├── rag_requests.py        # Request schemas
│       └── rag_responses.py       # Response schemas
├── data/
│   ├── faiss_index               # FAISS index file
│   └── faiss_index.metadata.pkl  # Metadata file
└── Anant_Personal_Profile_DeepDive.pdf
```

---

## 🔍 How It Works

1. **Ingest**: PDF → Chunks → Embeddings → FAISS
2. **Query**: Question → Embedding → Search → Context → LLM → Answer
3. **Compare**: Same question → RAG answer + Non-RAG answer → Comparison

---

## ✅ Next Steps

1. Run `/rag/ingest` with your PDF
2. Test `/rag/query` with various questions
3. Use `/rag/compare` to see the difference
4. Analyze the results and improve chunking if needed
