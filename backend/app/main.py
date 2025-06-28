# To run: uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .core import explain_error

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ErrorRequest(BaseModel):
    error: str

@app.post("/explain")
async def explain(req: ErrorRequest):
    return explain_error(req.error)
