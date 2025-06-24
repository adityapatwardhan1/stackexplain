# To run: uvicorn main:app --reload

from fastapi import FastAPI
from pydantic import BaseModel 
from openai import OpenAI, InternalServerError
import os 
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import re 
import json
import time 

# Load API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# FastAPI app setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class ErrorRequest(BaseModel):
    error: str 

# Optional: Add common error type hints to prompt
def add_error_type_info(prompt: str) -> str:
    error_types = [
        "OverflowError", "ZeroDivisionError", "FloatingPointError",
        "IndexError", "KeyError", "TypeError", "AssertionError", 
        "AttributeError", "EOFError", "ImportError", "NameError"
    ]
    for err_type in error_types:
        if err_type in prompt:
            prompt += f"\nNote: This seems to be a {err_type}."
            break
    return prompt

# Validate model output and add fallbacks
def validate_fields(parsed: dict) -> dict:
    return {
        "error_type": parsed.get("error_type", "UnknownError"),
        "explanation": parsed.get("explanation", "No explanation available."),
        "suggested_fix": parsed.get("suggested_fix", "No fix available."),
        "relevant_link": parsed.get("relevant_link", "https://docs.python.org/3/")
    }

# API endpoint
@app.post("/explain")
async def explain_error(req: ErrorRequest):
    prompt = f"""You are an expert Python debugging assistant.
Your task is to analyze the following error message, explain it simply for a beginner, suggest a fix, and (if possible) provide a link to documentation.

Respond in JSON with:
- error_type
- explanation
- suggested_fix
- relevant_link

Respond ONLY with a raw JSON object. Do not include any code block formatting.

Error:
{req.error}
"""

    prompt = add_error_type_info(prompt)

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    retries = 3

    for i in range(retries):
        try:
            completion = client.chat.completions.create(
                model="mistralai/mistral-small-3.2-24b-instruct:free",
                messages=[{"role": "user", "content": prompt}],
            )
            content = completion.choices[0].message.content.strip()

            # Strip markdown ```json
            if content.startswith("```json") or content.startswith("```"):
                content = re.sub(r"^```(json)?", "", content).strip().rstrip("```").strip()

            parsed = json.loads(content)
            return validate_fields(parsed)

        except InternalServerError:
            if i < retries - 1:
                time.sleep(2 ** i)
            else:
                return validate_fields({
                    "error_type": "ModelUnavailable",
                    "explanation": "The model is temporarily unavailable. Please try again shortly.",
                    "suggested_fix": "Wait a moment and try again. This may be due to server load on the free model.",
                    "relevant_link": "https://openrouter.ai/docs"
                })

        except Exception as e:
            if i < retries - 1:
                time.sleep(2 ** i)
            else:
                return validate_fields({
                    "error_type": "InternalError",
                    "explanation": "An internal error occurred while processing your request.",
                    "suggested_fix": str(e),
                    "relevant_link": "https://openrouter.ai/docs"
                })
