from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.utils.answer_generator import generate_answer
from typing import Optional

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to just the submission domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str
    attachment: Optional[str] = None  # not used yet


@app.get("/ping")
def ping():
    return {"message": "API is alive 🚀"}

@app.get("/")
def home():
    return {"message": "Welcome to the TDS Virtual TA API. Use POST /ask to ask questions."}

@app.post("/ask")
def ask_question(payload: QuestionRequest):
    answer, sources = generate_answer(payload.question)
    return {
        "answer": answer,
        "sources": sources
    }
