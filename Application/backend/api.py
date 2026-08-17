"""
DevOps AI Agent API

Handles:

- Chat
- Memory
- Conversation context
- Intelligent question routing
- RAG document retrieval
- RAG source attribution
- RAG retrieval metadata
- DevOps agent execution
- Agent tool execution metadata
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

from services.conversation_context import (
    conversation_context,
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
# Agent Tool Metadata
# =====================================================

def extract_agent_tool_execution(
    response,
):
    """
    Extract tool execution information from
    the LangChain agent response.

    Returns:

    [
        {
            "tool": "kubectl_pods",
            "status": "completed",
            "input": {},
            "output": "..."
        }
    ]
    """

    executions = []

    messages = response.get(
        "messages",
        [],
    )

    for message in messages:

        # =================================================
        # Tool Call Message
        # =================================================

        tool_calls = getattr(
            message,
            "tool_calls",
            None,
        )

        if tool_calls:

            for tool_call in tool_calls:

                if not isinstance(
                    tool_call,
                    dict,
                ):
                    continue

                tool_name = (
                    tool_call.get("name")
                    or tool_call.get("tool")
                    or "unknown"
                )

                tool_input = (
                    tool_call.get("args")
                    or tool_call.get("input")
                    or {}
                )

                executions.append(
                    {
                        "tool": tool_name,
                        "status": "started",
                        "input": tool_input,
                        "output": None,
                    }
                )

        # =================================================
        # Tool Result Message
        # =================================================

        message_type = getattr(
            message,
            "type",
            "",
        )

        if message_type == "tool":

            tool_name = getattr(
                message,
                "name",
                None,
            )

            if not tool_name:
                tool_name = "unknown"

            tool_output = getattr(
                message,
                "content",
                None,
            )

            # =================================================
            # Match Tool Result
            # =================================================

            matched = False

            for execution in reversed(
                executions
            ):

                if (
                    execution["tool"]
                    == tool_name
                    and execution["output"]
                    is None
                ):

                    execution["status"] = (
                        "completed"
                    )

                    execution["output"] = (
                        tool_output
                    )

                    matched = True

                    break

            # =================================================
            # No Matching Tool Call
            # =================================================

            if not matched:

                executions.append(
                    {
                        "tool": tool_name,
                        "status": "completed",
                        "input": {},
                        "output": tool_output,
                    }
                )

    return executions


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
    # Save User Message
    # =================================================

    memory.add_message(
        request.conversation_id,
        "user",
        request.message,
    )


    # =================================================
    # Retrieve Conversation History
    # =================================================

    history = memory.get_messages(
        request.conversation_id,
    )


    # Current user message was just added.
    # Exclude it from previous history.

    previous_messages = history[:-1]


    # =================================================
    # Resolve Conversation Context
    # =================================================

    resolved_question = (
        conversation_context.resolve_question(
            question=request.message,
            history=previous_messages,
        )
    )


    print(
        "Original Question:",
        request.message,
    )

    print(
        "Resolved Question:",
        resolved_question,
    )


    # =================================================
    # Check Uploaded Documents
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
        question=resolved_question,
        has_documents=has_documents,
    )


    print(
        "Question Route:",
        route.value,
    )


    # =================================================
    # Prepare Previous Messages
    # =================================================

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
    # Default Agent Metadata
    # =================================================

    agent_tool_execution = []


    # =================================================
    # RAG ROUTE
    # =================================================

    if route == QuestionRoute.RAG:

        print(
            "Processing through RAG..."
        )


        # -------------------------------------------------
        # Retrieve Context
        # -------------------------------------------------

        rag_result = (
            rag_service.retrieve_context_with_metadata(
                query=resolved_question,
                conversation_id=(
                    request.conversation_id
                ),
            )
        )


        # -------------------------------------------------
        # Context
        # -------------------------------------------------

        rag_context = (
            rag_result.get(
                "context",
                "",
            )
        )


        # -------------------------------------------------
        # Sources
        # -------------------------------------------------

        rag_sources = (
            rag_result.get(
                "sources",
                [],
            )
        )


        # -------------------------------------------------
        # Retrieval Metadata
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
        # Answer From Context
        # -------------------------------------------------

        if rag_context:

            rag_answer = (
                rag_service.answer_from_context(
                    question=resolved_question,
                    context=rag_context,
                )
            )


            # -------------------------------------------------
            # RAG Successfully Answered
            # -------------------------------------------------

            if (
                rag_answer.strip()
                != "NOT_ENOUGH_CONTEXT"
            ):

                answer = rag_answer


                memory.add_message(
                    request.conversation_id,
                    "assistant",
                    answer,
                )


                return {
                    "success": True,
                    "conversation_id": (
                        request.conversation_id
                    ),
                    "question": (
                        request.message
                    ),
                    "resolved_question": (
                        resolved_question
                    ),
                    "answer": answer,
                    "route": "rag",
                    "rag_used": True,
                    "agent_used": False,
                    "sources": rag_sources,
                    "retrieval": rag_retrieval,
                    "tool_execution": [],
                }


        # -------------------------------------------------
        # RAG Could Not Answer
        # -------------------------------------------------

        print(
            "RAG could not answer. "
            "Falling back to agent."
        )


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
            resolved_question,
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


        memory.add_message(
            request.conversation_id,
            "assistant",
            answer,
        )


        return {
            "success": True,
            "conversation_id": (
                request.conversation_id
            ),
            "question": (
                request.message
            ),
            "resolved_question": (
                resolved_question
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
            "tool_execution": [],
        }


    # =================================================
    # AGENT ROUTE
    # =================================================

    messages.append(
        (
            "user",
            resolved_question,
        )
    )


    print(
        "Processing through DevOps Agent..."
    )


    try:

        response = agent.invoke(
            {
                "messages": messages,
            }
        )


        # =================================================
        # Debug Raw Agent Response
        # =================================================

        print("=" * 60)
        print("AGENT RAW RESPONSE")
        print(response)
        print("=" * 60)


        # =================================================
        # Extract Tool Execution Metadata
        # =================================================

        agent_tool_execution = (
            extract_agent_tool_execution(
                response
            )
        )


        print(
            "Agent Tool Execution:",
            agent_tool_execution,
        )


        # =================================================
        # Extract Final Answer
        # =================================================

        answer = (
            response["messages"][-1]
            .content
        )


    except Exception as exc:

        print(
            "Agent execution failed:",
            str(exc),
        )


        answer = (
            "Unable to execute the DevOps agent."
        )


        agent_tool_execution = [
            {
                "tool": "unknown",
                "status": "failed",
                "input": {},
                "output": str(exc),
            }
        ]


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
        "resolved_question": (
            resolved_question
        ),
        "answer": answer,
        "route": "agent",
        "rag_used": False,
        "agent_used": True,
        "sources": [],
        "retrieval": {
            "chunks_retrieved": 0,
            "results": [],
        },
        "tool_execution": (
            agent_tool_execution
        ),
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