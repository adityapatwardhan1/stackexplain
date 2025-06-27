# To run: uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core import explain_error

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ErrorRequest(BaseModel):
    error: str

@app.post("/explain")
async def explain(req: ErrorRequest):
    return explain_error(req.error)

'''
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
    prompt = f"""
    You are an expert Python debugging assistant.

    You will be given an error message that a beginner doesn't understand. Your job is to explain it **clearly**,       suggest a likely fix, and optionally provide a relevant link to official documentation or StackOverflow.

    Please follow this output format strictly (as a raw JSON object, **no commentary or markdown**):

    {{
    "error_type": "...",          // One-word name of the error (e.g., TypeError)
    "explanation": "...",         // Explain in beginner-friendly language (1-2 sentences)
    "suggested_fix": "...",       // Concrete fix or advice
    "relevant_link": "..." // Link to documentation or a helpful StackOverflow post
    }}
    
    Think through the problem in steps (but do not include this reasoning in the final output).
    
    Rules:
    - Respond ONLY with a valid JSON object, no markdown formatting.
    - Do not include code block fences (like ```json).
    - Choose a relevant link — official docs preferred, StackOverflow if needed.\n"""

    # This few-shot example worsens the quality a lot
    few_shot = """
    Example:

    Input Error:
    TypeError: unsupported operand type(s) for +: 'int' and 'str'

    Output:
    {
    "error_type": "TypeError",
    "explanation": "You tried to add an integer and a string, which aren't compatible types in Python.",
    "suggested_fix": "Convert the string to an int using int(), or convert the int to a string using str().",
    "relevant_link": "https://stackoverflow.com/questions/75556765/how-to-add-a-string-to-an-integer-in-python"
    }\n"""

    few_shot = ""
    
    directive = """Now process the next error:

    Input Error:
    {req.error}\n"""

    prompt = prompt + few_shot + directive + add_error_type_info(prompt)

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
'''