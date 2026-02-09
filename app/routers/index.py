"""API routes"""

from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import StreamingResponse
from app.schemas.requests import AskRequest, ChatRequest, StreamRequest
from app.schemas.responses import AskResponseData, ChatResponseData
from app.schemas.base import StandardResponse
from app.services import get_llm_service
from app.utils.response_helpers import create_response, get_request_id
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/health", tags=["Health"], response_model=StandardResponse[dict])
async def health_check(request: Request) -> StandardResponse[dict]:
    """
    Health check endpoint

    Returns the health status of the API.
    """
    request_id = get_request_id(request)
    return create_response(
        message="Service is healthy",
        status_code=status.HTTP_200_OK,
        data={"status": "ok", "service": "AI LLM API"},
        request_id=request_id,
    )


@router.post(
    "/ask",
    tags=["Simple AI Response"],
    response_model=StandardResponse[AskResponseData],
)
async def ask_route(
    request: Request, body: AskRequest
) -> StandardResponse[AskResponseData]:
    """
    Simple LLM response endpoint

    - **prompt**: User's question or prompt (required)
    - **timeout**: Optional timeout override in seconds (1-300)

    Returns a simple LLM response to the user's prompt.
    """
    request_id = get_request_id(request)
    llm_service = get_llm_service()

    response_text = await llm_service.ask(prompt=body.prompt, timeout=body.timeout)

    response_data = AskResponseData(
        response=response_text, model=llm_service.model
    )

    return create_response(message="Response generated successfully",status_code=status.HTTP_200_OK,data=response_data,request_id=request_id)


@router.post("/chat",tags=["Chat with System Prompt"],response_model=StandardResponse[ChatResponseData])
async def chat_route(request: Request, body: ChatRequest ) -> StandardResponse[ChatResponseData]:
    """
    Chat endpoint with system and user prompts

    - **system_prompt**: System instruction or context (required)
    - **user_prompt**: User's message (required)
    - **timeout**: Optional timeout override in seconds (1-300)

    Returns an LLM response using both system and user prompts.
    """
    request_id = get_request_id(request)
    llm_service = get_llm_service()

    response_text = await llm_service.chat(
        system_prompt=body.system_prompt,
        user_prompt=body.user_prompt,
        timeout=body.timeout,
    )

    response_data = ChatResponseData(
        response=response_text, model=llm_service.model
    )

    return create_response(
        message="Chat response generated successfully",
        status_code=status.HTTP_200_OK,
        data=response_data,
        request_id=request_id,
    )


@router.post("/stream", tags=["Streaming Response"])
async def stream_route(request: Request, body: StreamRequest) -> StreamingResponse:
    """
    Streaming LLM response endpoint

    - **prompt**: User's prompt (required)
    - **system_prompt**: Optional system instruction
    - **timeout**: Optional timeout override in seconds (1-600)

    Returns a streaming response from the LLM.
    Note: Streaming endpoints return plain text chunks, not JSON.
    """
    request_id = get_request_id(request)

    async def generate_stream():
        try:
            llm_service = get_llm_service()
            chunk_count = 0

            async for chunk in llm_service.stream(
                prompt=body.prompt,
                system_prompt=body.system_prompt,
                timeout=body.timeout,
            ):
                chunk_count += 1
                yield chunk

            # Log completion
            logger.info(
                f"Stream completed with {chunk_count} chunks (request_id: {request_id})"
            )

        except Exception as e:
            logger.error(f"Stream error (request_id: {request_id}): {str(e)}")
            yield f"\n[Error: {str(e)}]"

    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Request-ID": request_id,
        },
    )


def register_routers(app: FastAPI) -> None:
    """Register all routers with the FastAPI app"""
    app.include_router(router)

    # Register RAG router
    from app.routers import rag
    app.include_router(rag.router)
