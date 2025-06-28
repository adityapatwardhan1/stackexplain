from openai import OpenAI, InternalServerError
import os, json, re, time
from dotenv import load_dotenv
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

import json

# "mistralai/mistral-small-3.2-24b-instruct:free"

def build_prompt(error: str, model_to_use="deepseek/deepseek-chat-v3-0324:free") -> str:
    examples = [
        {
            "language": "Python",
            "input": "IndexError: list index out of range",
            "output": {
                "error_type": "IndexError",
                "explanation": "You tried to access a position in a list that doesn't exist.",
                "suggested_fix": "Make sure your index is within the bounds of the list (0 to len(list)-1).",
                "relevant_links": [
                    "https://docs.python.org/3/library/exceptions.html#IndexError"
                ]
            }
        },
        {
            "language": "JavaScript",
            "input": "TypeError: undefined is not a function",
            "output": {
                "error_type": "TypeError",
                "explanation": "You're trying to call something that isn't defined as a function.",
                "suggested_fix": "Check if the variable you're calling is actually assigned to a function.",
                "relevant_links": [
                    "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors/Not_a_function"
                ]
            }
        },
        {
            "language": "Java",
            "input": "NullPointerException",
            "output": {
                "error_type": "NullPointerException",
                "explanation": "You're trying to use an object reference that is null.",
                "suggested_fix": "Check if the object is null before calling methods or accessing fields on it.",
                "relevant_links": [
                    "https://docs.oracle.com/javase/8/docs/api/java/lang/NullPointerException.html"
                ]
            }
        }
    ]

    few_shot_block = ""
    for ex in examples:
        few_shot_block += f"""Example:
This is a {ex["language"]} error.

Input:
{ex["input"]}

Output:
{json.dumps(ex["output"], indent=2)}

"""

    instruction_block = """You are an expert multilingual debugging assistant.

Your task is to analyze code error messages from various programming languages (like Python, JavaScript, Java, etc.), explain what causes them, suggest a fix, and provide up to 3 helpful documentation links.

Always respond with a raw JSON object in the following format (no markdown, no code blocks):

{
  "error_type": "...",
  "explanation": "...",
  "suggested_fix": "...",
  "relevant_links": ["...", "...", "..."]
}

Think step-by-step if needed, but only output the final JSON.

"""

    query_block = f"""Now explain this error:

Input:
{error}
"""

    # Use few-shot prompting only for DeepSeek or Gemini
    if any(keyword in model_to_use.lower() for keyword in ["deepseek", "gemini"]):
        return instruction_block + few_shot_block + query_block
    else:
        return instruction_block + query_block


def verify_link(url: str, max_title_len: int = 100) -> bool:
    """Check if a link is reachable and has a reasonable HTML title."""
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.string if soup.title else ""
        # Check title exists and isn't nonsense or empty
        if title and len(title) <= max_title_len:
            return True
        return False
    except Exception as e:
        # print(e)
        return False

def clean_links(links: list[str], max_len: int = 200) -> list[str]:
    cleaned = []
    for link in links:
        if not isinstance(link, str):
            continue
        if len(link) > max_len:
            continue  # too long
        if any(bad in link for bad in ["duckduckgo.com", "google.com/search"]):
            continue
        # Verify the link is valid and relevant by checking if reachable and has a title
        if verify_link(link):
            cleaned.append(link)
        else:
            pass
            # print(f"Discarded invalid/unreachable link: {link}")
        if len(cleaned) >= 3:
            break
    return cleaned


def explain_error(error_msg: str, model_to_use: str = "deepseek/deepseek-chat-v3-0324:free", retries: int = 3) -> dict:
    prompt = build_prompt(error_msg, model_to_use=model_to_use)
    for i in range(retries):
        try:
            resp = client.chat.completions.create(
                model=model_to_use,
                messages=[{"role": "user", "content": prompt}],
            )
            content = resp.choices[0].message.content.strip()
            if content.startswith("```"):
                content = re.sub(r"^```(?:json)?", "", content).strip().rstrip("```").strip()
            data = json.loads(content)
            links = clean_links(data.get("relevant_links", []))
            return {
                "error_type": data.get("error_type", "UnknownError"),
                "explanation": data.get("explanation", "No explanation available."),
                "suggested_fix": data.get("suggested_fix", "No fix available."),
                "relevant_links": links,
            }
        except InternalServerError:
            if i < retries - 1:
                time.sleep(2 ** i)
                continue
            return {
                "error_type": "ModelUnavailable",
                "explanation": "Model temporarily unavailable—try again later.",
                "suggested_fix": "",
                "relevant_links": ["https://openrouter.ai/docs"]
            }
        except Exception as e:
            if i < retries - 1:
                time.sleep(2 ** i)
                continue
            return {
                "error_type": "InternalError",
                "explanation": "Internal error occurred.",
                "suggested_fix": str(e),
                "relevant_links": []
            }
