from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import agent

app = FastAPI(
    title="DevOps AI Agent API",
    version="1.0.0"
)

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Later restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "message": "DevOps AI Agent API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "agent": "online"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = agent.invoke(
        {
            "messages": [
                ("user", request.message)
            ]
        }
    )

    answer = response["messages"][-1].content
    return {
    "success": True,
    "question": request.message,
    "answer": answer,
    "tool": "Unknown",
    "command": "Unknown",
    "execution_time": 0.0,
    }

    # return {
    #     "success": True,
    #     "question": request.message,
    #     "answer": answer
    #}