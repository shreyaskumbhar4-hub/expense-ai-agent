from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse

from src.agent import run_agent

app = FastAPI(title="Expense AI Agent")


class ChatRequest(BaseModel):
    user_id: int
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def home():
    return FileResponse("src/static/index.html")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = run_agent(request.message, request.user_id)
    return {"response": response}