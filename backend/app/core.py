from openai import OpenAI, InternalServerError
import os, json, re, time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

def build_prompt(error: str) -> str:
    
    return f"""You are an expert Python debugging assistant.

    You will be given an error message that a beginner doesn't understand. Your job is to explain it **clearly**, suggest a likely fix, and optionally provide a relevant link to official documentation or StackOverflow.

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
    - Choose a relevant link — official docs preferred, StackOverflow if needed.

    Error:
    {error}
    """

def explain_error(error_msg: str, retries: int = 3) -> dict:
    prompt = build_prompt(error_msg)
    for i in range(retries):
        try:
            resp = client.chat.completions.create(
                model="mistralai/mistral-small-3.2-24b-instruct:free",
                messages=[{"role": "user", "content": prompt}],
            )
            content = resp.choices[0].message.content.strip()
            # strip code fences
            if content.startswith("```"):
                content = re.sub(r"^```(?:json)?", "", content).strip().rstrip("```").strip()
            data = json.loads(content)
            # ensure all fields
            return {
                "error_type": data.get("error_type", "UnknownError"),
                "explanation": data.get("explanation", "No explanation available."),
                "suggested_fix": data.get("suggested_fix", "No fix available."),
                "relevant_link": data.get("relevant_link", "")
            }
        except InternalServerError:
            if i < retries - 1:
                time.sleep(2 ** i)
                continue
            return {
                "error_type": "ModelUnavailable",
                "explanation": "Model temporarily unavailable—try again later.",
                "suggested_fix": "",
                "relevant_link": "https://openrouter.ai/docs"
            }
        except Exception as e:
            if i < retries - 1:
                time.sleep(2 ** i)
                continue
            return {
                "error_type": "InternalError",
                "explanation": "Internal error occurred.",
                "suggested_fix": str(e),
                "relevant_link": ""
            }