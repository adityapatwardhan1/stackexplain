# To run: uvicorn main:app --reload

# Import Dependencies
from fastapi import FastAPI, Request
from pydantic import BaseModel 
from openai import OpenAI
import requests
import os 
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ErrorRequest(BaseModel):
    error: str 

@app.post("/explain")
async def explain_error(req: ErrorRequest):
    """
    Add docstring
    Parameters:
    Returns:
    """
    prompt = f"Explain the following error in simple terms, and suggest a fix:\n\n{req.error}"
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    # Get and return response
    completion = client.chat.completions.create(
        model="mistralai/mistral-small-3.2-24b-instruct:free",
        messages=[{"role": "user", "content": prompt}]
    )
    explanation = completion.choices[0].message.content
    return { "explanation": explanation }
