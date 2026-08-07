

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# from agent import agent

from services.chat_service import chat_service

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
    conversation_id: str
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

    response = chat_service.ask(request.message)

    return {
        "success": response.success,
        "question": request.message,
        "answer": response.answer,
        "tool": response.tool,
        "command": response.command,
        "execution_time": response.execution_time,
    }

# @app.post("/chat")
# def chat(request: ChatRequest):

#     response = agent.invoke(
#         {
#             "messages": [
#                 ("user", request.message)
#             ]
#         }
#     )

#     answer = response["messages"][-1].content
    
#     return {
#         "success": True,
#         "question": request.message,
#         "answer": answer
#     }

