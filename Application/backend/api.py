from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import agent
from memory import memory
from rag.rag_service import rag_service


app = FastAPI(
    title="DevOps AI Agent API",
    version="1.0.0",
)


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models

class ChatRequest(BaseModel):
    conversation_id: str
    message: str


# Root

@app.get("/")
def root():

    return {
        "message": "DevOps AI Agent API",
        "status": "running",
    }


# Health

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "agent": "online",
    }


# Chat

@app.post("/chat")
def chat(request: ChatRequest):

    print("=" * 60)
    print("Conversation:", request.conversation_id)
    print("Question:", request.message)
    print("=" * 60)

    # -------------------------------------------------
    # Save user message to memory
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

    messages = []

    for msg in history:

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
    # Add RAG context if available
    # -------------------------------------------------

    if rag_context:

        rag_message = (
            "Relevant infrastructure/document context "
            "retrieved from the user's uploaded files:\n\n"
            f"{rag_context}\n\n"
            "Use this context when it is relevant to "
            "answering the user's question."
        )

        messages.insert(
            max(len(messages) - 1, 0),
            (
                "system",
                rag_message,
            ),
        )

    # -------------------------------------------------
    # Invoke Agent
    # -------------------------------------------------

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
        "rag_used": bool(rag_context),
    }