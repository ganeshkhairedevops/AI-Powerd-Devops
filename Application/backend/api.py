from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import agent
from memory import memory
from rag.rag_service import rag_service


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
def chat(request: ChatRequest):

    print("=" * 60)
    print("Conversation:", request.conversation_id)
    print("Question:", request.message)
    print("=" * 60)

    # -------------------------------------------------
    # Save user message
    # -------------------------------------------------

    memory.add_message(
        request.conversation_id,
        "user",
        request.message,
    )

    # -------------------------------------------------
    # Retrieve conversation history
    # -------------------------------------------------

    history = memory.get_messages(
        request.conversation_id
    )

    previous_messages = history[:-1]

    messages = []

    for msg in previous_messages:

        messages.append(
            (
                msg.role,
                msg.content,
            )
        )

    # -------------------------------------------------
    # Retrieve RAG context
    # -------------------------------------------------

    rag_context = rag_service.retrieve_context(
        request.message
    )

    # -------------------------------------------------
    # Try answering directly from RAG
    # -------------------------------------------------

    if rag_context:

        rag_answer = rag_service.answer_from_context(
            question=request.message,
            context=rag_context,
        )

        # -------------------------------------------------
        # RAG successfully answered
        # -------------------------------------------------

        if rag_answer != "NOT_ENOUGH_CONTEXT":

            answer = rag_answer

            memory.add_message(
                request.conversation_id,
                "assistant",
                answer,
            )

            return {
                "success": True,
                "conversation_id": request.conversation_id,
                "question": request.message,
                "answer": answer,
                "rag_used": True,
                "agent_used": False,
            }

    # -------------------------------------------------
    # RAG could not answer
    # Use normal DevOps Agent
    # -------------------------------------------------

    messages.append(
        (
            "user",
            request.message,
        )
    )

    response = agent.invoke(
        {
            "messages": messages,
        }
    )

    answer = response["messages"][-1].content

    # -------------------------------------------------
    # Save assistant response
    # -------------------------------------------------

    memory.add_message(
        request.conversation_id,
        "assistant",
        answer,
    )

    # -------------------------------------------------
    # Response
    # -------------------------------------------------

    return {
        "success": True,
        "conversation_id": request.conversation_id,
        "question": request.message,
        "answer": answer,
        "rag_used": False,
        "agent_used": True,
    }

# =====================================================
# File Upload
# =====================================================

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
):

    if not file.filename:

        return {
            "success": False,
            "message": "No file provided.",
        }


    # -------------------------------------------------
    # Save uploaded file
    # -------------------------------------------------

    file_path = UPLOAD_DIR / file.filename

    content = await file.read()

    file_path.write_bytes(content)


    # -------------------------------------------------
    # Ingest document into RAG
    # -------------------------------------------------

    try:

        result = rag_service.ingest_file(
            str(file_path)
        )

        return {
            "success": result["success"],
            "filename": result["filename"],
            "chunks": result["chunks"],
            "message": result["message"],
        }


    except Exception as exc:

        return {
            "success": False,
            "filename": file.filename,
            "message": str(exc),
        }