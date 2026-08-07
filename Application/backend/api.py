from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import agent
from memory import memory


app = FastAPI(
    title="DevOps AI Agent API",
    version="1.0.0",
)

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    conversation_id: str
    message: str


@app.get("/")
def root():
    return {
        "message": "DevOps AI Agent API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "agent": "online",
    }


@app.post("/chat")
def chat(request: ChatRequest):

    # Save user message
    memory.add_message(
        request.conversation_id,
        "user",
        request.message,
    )

    # Load conversation history
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

    # Send conversation history to the agent
    response = agent.invoke(
        {
            "messages": messages
        }
    )

    answer = response["messages"][-1].content

    # Save AI response
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
    }