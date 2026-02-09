"""Prompt templates for LLM interactions"""

from typing import List


def build_rag_prompt(context: str, user_query: str) -> str:
    """
    Build RAG prompt with context and user query

    Args:
        context: Retrieved context chunks from vector store
        user_query: User's question

    Returns:
        Formatted prompt string
    """
    prompt = f"""You are a helpful assistant. Answer the user's question based on the provided context from documents.

Context from documents:
{context}

User Question: {user_query}

Instructions:
- Answer the question using ONLY the information provided in the context above
- If the context doesn't contain enough information, say so
- Be specific and cite relevant details from the context
- Do not make up information that isn't in the context

Answer:"""

    return prompt


def build_rag_prompt_with_sources(context_chunks: List[str], user_query: str) -> str:
    """
    Build RAG prompt with numbered context chunks for better citation

    Args:
        context_chunks: List of context chunks
        user_query: User's question

    Returns:
        Formatted prompt string with numbered sources
    """
    numbered_context = "\n\n---\n\n".join(
        [f"[Source {i+1}]\n{chunk}" for i, chunk in enumerate(context_chunks)]
    )

    prompt = f"""You are a helpful assistant answering questions based on provided documents. Answer naturally and conversationally, as if you're explaining to a friend.

Context from documents:
{numbered_context}

User Question: {user_query}

Important Instructions:
1. **Entity Resolution**: If the question mentions a person's first name (e.g., "Anant"), understand that it refers to their full name when mentioned in the context (e.g., "Anant Kumar Yadav"). Use the full name when appropriate.

2. **Answer Style**:
   - Answer naturally and conversationally
   - Don't use phrases like "Based on the context" or "According to Source X" - just answer directly
   - Write as if you know this information personally
   - Use "he/his" or "she/her" naturally when referring to people

3. **Relevance & Conciseness**:
   - Answer STRICTLY what is asked - nothing more, nothing less
   - If a question can be answered briefly (yes/no or one sentence), keep it short
   - Do not add unnecessary information, background, or extra details unless directly relevant
   - Stay focused on the specific question asked
   - Avoid verbose explanations when a simple answer suffices

4. **Information Usage**:
   - Use ONLY the information provided in the context above
   - If multiple sources mention the same thing, synthesize the information naturally
   - If the context doesn't contain enough information, say so clearly and briefly
   - Do not make up information that isn't in the context

5. **Citations**:
   - Only mention sources if directly asked or if it adds clarity
   - Don't cite sources in every sentence - integrate information naturally

6. **Clarity**:
   - If the question is ambiguous, provide the most relevant answer based on context
   - If asking "Who is X?", provide a clear introduction with full name and key details
   - Be direct and to the point

Answer the question naturally and concisely:"""

    return prompt


def build_simple_prompt(user_query: str) -> str:
    """
    Build simple prompt without context (for non-RAG queries)

    Args:
        user_query: User's question

    Returns:
        Simple prompt string
    """
    return user_query


def build_comparison_prompt(user_query: str) -> str:
    """
    Build prompt for comparing RAG vs non-RAG answers

    Args:
        user_query: User's question

    Returns:
        Prompt for comparison analysis
    """
    prompt = f"""Analyze the following question and provide insights:

Question: {user_query}

Please consider:
- What type of information would be needed to answer this?
- Would document-based context improve the answer?
- What are the limitations of answering without specific documents?

Analysis:"""

    return prompt


def enhance_query_for_entity_resolution(query: str) -> str:
    """
    Enhance query to help with entity resolution

    Args:
        query: Original user query

    Returns:
        Enhanced query with entity hints
    """
    # Common name variations - can be expanded
    entity_mappings = {
        "anant": "Anant Kumar Yadav",
        "anant's": "Anant Kumar Yadav's",
        "anant has": "Anant Kumar Yadav has",
        "anant is": "Anant Kumar Yadav is",
        "who is anant": "who is Anant Kumar Yadav",
        "what is anant": "what is Anant Kumar Yadav",
    }

    query_lower = query.lower()

    # Check if query contains entity references
    for key, value in entity_mappings.items():
        if key in query_lower:
            # Add both the original and full name to help retrieval
            enhanced = f"{query} (also search for: {value})"
            return enhanced

    return query
