"""
DevOps AI Agent API

Handles:

- Chat
- Memory
- Intelligent question routing
- RAG document retrieval
- RAG source attribution
- RAG retrieval metadata
- DevOps agent execution
- General LLM questions
- File uploads
- Document listing
- Document deletion
"""

from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import agent
from llm import llm
from memory import memory

from rag.rag_service import rag_service

from services.question_router import (
    question_router,
    QuestionRoute,
)


# =====================================================
# Application
# =====================================================

app = FastAPI(
    title="DevOps AI Agent API",
    version="1.0.0",
)


# =====================================================
# Upload Directory
# =====================================================

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Request Models
# =====================================================

class ChatRequest(BaseModel):

    conversation_id: str

    message: str


# =====================================================
# Root
# =====================================================

@app.get("/")
def root():

    return {
        "message": "DevOps AI Agent API",
        "status": "running",
    }


# =====================================================
# Health
# =====================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "agent": "online",
    }


# =====================================================
# Chat
# =====================================================

@app.post("/chat")
def chat(
    request: ChatRequest,
):

    print("=" * 60)

    print(
        "Conversation:",
        request.conversation_id,
    )

    print(
        "Question:",
        request.message,
    )

    print("=" * 60)


    # =================================================
    # Save user message
    # =================================================

    memory.add_message(
        request.conversation_id,
        "user",
        request.message,
    )


    # =================================================
    # Check uploaded documents
    # =================================================

    try:

        documents = rag_service.list_documents(
            conversation_id=request.conversation_id,
        )

    except Exception as exc:

        print(
            "Document lookup failed:",
            str(exc),
        )

        documents = []


    has_documents = bool(
        documents
    )


    print(
        "Documents Available:",
        has_documents,
    )


    # =================================================
    # Determine Question Route
    # =================================================

    route = question_router.route(
        question=request.message,
        has_documents=has_documents,
    )


    print(
        "Question Route:",
        route.value,
    )


    # =================================================
    # Retrieve Conversation History
    # =================================================

    history = memory.get_messages(
        request.conversation_id,
    )


    # Current user message was just added,
    # therefore exclude it from previous history.

    previous_messages = history[:-1]

    messages = []


    for msg in previous_messages:

        messages.append(
            (
                msg.role,
                msg.content,
            )
        )


    # =================================================
    # Default RAG Metadata
    # =================================================

    rag_sources = []

    rag_retrieval = {
        "chunks_retrieved": 0,
        "results": [],
    }


    # =================================================
    # RAG ROUTE
    # =================================================

    if route == QuestionRoute.RAG:

        print(
            "Processing through RAG..."
        )


        # -------------------------------------------------
        # Retrieve context + sources + metadata
        # -------------------------------------------------

        rag_result = (
            rag_service.retrieve_context_with_metadata(
                query=request.message,
                conversation_id=(
                    request.conversation_id
                ),
            )
        )


        # -------------------------------------------------
        # Extract context
        # -------------------------------------------------

        rag_context = (
            rag_result.get(
                "context",
                "",
            )
        )


        # -------------------------------------------------
        # Extract sources
        # -------------------------------------------------

        rag_sources = (
            rag_result.get(
                "sources",
                [],
            )
        )


        # -------------------------------------------------
        # Extract retrieval metadata
        # -------------------------------------------------

        rag_retrieval = (
            rag_result.get(
                "retrieval",
                {
                    "chunks_retrieved": 0,
                    "results": [],
                },
            )
        )


        print(
            "RAG Sources:",
            rag_sources,
        )


        print(
            "RAG Chunks Retrieved:",
            rag_retrieval.get(
                "chunks_retrieved",
                0,
            ),
        )


        print(
            "RAG Retrieval Results:",
            rag_retrieval.get(
                "results",
                [],
            ),
        )


        # -------------------------------------------------
        # Context found
        # -------------------------------------------------

        if rag_context:

            rag_answer = (
                rag_service.answer_from_context(
                    question=request.message,
                    context=rag_context,
                )
            )


            # -------------------------------------------------
            # RAG successfully answered
            # -------------------------------------------------

            if (
                rag_answer.strip()
                != "NOT_ENOUGH_CONTEXT"
            ):

                answer = rag_answer


                # -------------------------------------------------
                # Save assistant response
                # -------------------------------------------------

                memory.add_message(
                    request.conversation_id,
                    "assistant",
                    answer,
                )


                # -------------------------------------------------
                # RAG Response
                # -------------------------------------------------

                return {
                    "success": True,
                    "conversation_id": (
                        request.conversation_id
                    ),
                    "question": (
                        request.message
                    ),
                    "answer": answer,
                    "route": "rag",
                    "rag_used": True,
                    "agent_used": False,
                    "sources": rag_sources,
                    "retrieval": rag_retrieval,
                }


        # -------------------------------------------------
        # RAG could not answer
        # -------------------------------------------------

        print(
            "RAG could not answer. "
            "Falling back to agent."
        )


        # Sources and retrieval metadata are not
        # returned as final RAG data when the
        # Agent produces the answer.

        rag_sources = []

        rag_retrieval = {
            "chunks_retrieved": 0,
            "results": [],
        }

        route = QuestionRoute.AGENT


    # =================================================
    # GENERAL ROUTE
    # =================================================

    if route == QuestionRoute.GENERAL:

        print(
            "Processing general question..."
        )


        response = llm.invoke(
            request.message,
        )


        if hasattr(
            response,
            "content",
        ):

            answer = (
                response.content.strip()
            )

        else:

            answer = str(
                response
            ).strip()


        # -------------------------------------------------
        # Save assistant response
        # -------------------------------------------------

        memory.add_message(
            request.conversation_id,
            "assistant",
            answer,
        )


        # -------------------------------------------------
        # General Response
        # -------------------------------------------------

        return {
            "success": True,
            "conversation_id": (
                request.conversation_id
            ),
            "question": (
                request.message
            ),
            "answer": answer,
            "route": "general",
            "rag_used": False,
            "agent_used": False,
            "sources": [],
            "retrieval": {
                "chunks_retrieved": 0,
                "results": [],
            },
        }


    # =================================================
    # AGENT ROUTE
    # =================================================

    messages.append(
        (
            "user",
            request.message,
        )
    )


    print(
        "Processing through DevOps Agent..."
    )


    response = agent.invoke(
        {
            "messages": messages,
        }
    )


    answer = (
        response["messages"][-1]
        .content
    )


    # =================================================
    # Save Assistant Response
    # =================================================

    memory.add_message(
        request.conversation_id,
        "assistant",
        answer,
    )


    # =================================================
    # Agent Response
    # =================================================

    return {
        "success": True,
        "conversation_id": (
            request.conversation_id
        ),
        "question": request.message,
        "answer": answer,
        "route": "agent",
        "rag_used": False,
        "agent_used": True,
        "sources": [],
        "retrieval": {
            "chunks_retrieved": 0,
            "results": [],
        },
    }


# =====================================================
# File Upload
# =====================================================

@app.post("/upload")
async def upload_file(
    conversation_id: str = Form(...),
    file: UploadFile = File(...),
):

    # =================================================
    # Validate Filename
    # =================================================

    if not file.filename:

        return {
            "success": False,
            "message": "No file provided.",
        }


    # =================================================
    # Secure Filename
    # =================================================

    filename = Path(
        file.filename
    ).name


    # =================================================
    # Conversation Upload Directory
    # =================================================

    conversation_dir = (
        UPLOAD_DIR
        / str(conversation_id)
    )


    conversation_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


    # =================================================
    # File Path
    # =================================================

    file_path = (
        conversation_dir
        / filename
    )


    # =================================================
    # Read File
    # =================================================

    try:

        content = await file.read()

        file_path.write_bytes(
            content
        )

    except Exception as exc:

        return {
            "success": False,
            "filename": filename,
            "conversation_id": (
                conversation_id
            ),
            "message": (
                f"Unable to save file: {exc}"
            ),
        }


    # =================================================
    # Ingest Document
    # =================================================

    try:

        result = (
            rag_service.ingest_file(
                filepath=str(file_path),
                conversation_id=(
                    conversation_id
                ),
            )
        )


        return {
            "success": result["success"],
            "filename": result["filename"],
            "chunks": result["chunks"],
            "conversation_id": (
                conversation_id
            ),
            "message": result["message"],
        }


    except Exception as exc:

        return {
            "success": False,
            "filename": filename,
            "conversation_id": (
                conversation_id
            ),
            "message": str(exc),
        }


# =====================================================
# List Documents
# =====================================================

@app.get(
    "/documents/{conversation_id}"
)
def list_documents(
    conversation_id: str,
):

    try:

        documents = (
            rag_service.list_documents(
                conversation_id=(
                    conversation_id
                ),
            )
        )


        return {
            "success": True,
            "conversation_id": (
                conversation_id
            ),
            "documents": documents,
        }


    except Exception as exc:

        return {
            "success": False,
            "conversation_id": (
                conversation_id
            ),
            "documents": [],
            "message": str(exc),
        }


# =====================================================
# Delete Document
# =====================================================

@app.delete(
    "/documents/{conversation_id}/{filename}"
)
def delete_document(
    conversation_id: str,
    filename: str,
):

    try:

        # -------------------------------------------------
        # Delete from ChromaDB
        # -------------------------------------------------

        result = (
            rag_service.delete_document(
                conversation_id=(
                    conversation_id
                ),
                filename=filename,
            )
        )


        # -------------------------------------------------
        # Delete physical file
        # -------------------------------------------------

        file_path = (
            UPLOAD_DIR
            / str(conversation_id)
            / Path(filename).name
        )


        if file_path.exists():

            file_path.unlink()


        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return {
            "success": True,
            "conversation_id": (
                conversation_id
            ),
            "filename": filename,
            "message": (
                "Document deleted successfully."
            ),
            "result": result,
        }


    except Exception as exc:

        return {
            "success": False,
            "conversation_id": (
                conversation_id
            ),
            "filename": filename,
            "message": str(exc),
        }