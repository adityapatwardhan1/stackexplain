from openai import OpenAI, InternalServerError
import os, json, re, time, requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

def build_prompt(error: str, model_to_use="deepseek/deepseek-chat-v3-0324:free") -> str:
    examples = [
        {
            "input": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
            "output": {
                "error_type": "TypeError",
                "explanation": "You tried to add an integer and a string, which Python does not allow.",
                "suggested_fix": "Convert the integer or the string using int() or str() before adding.",
                "relevant_link": "https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator"
            }
        },
        {
            "input": "IndexError: list index out of range",
            "output": {
                "error_type": "IndexError",
                "explanation": "You tried to access a position in a list that doesn't exist.",
                "suggested_fix": "Make sure your index is within the bounds of the list (0 to len(list)-1).",
                "relevant_link": "https://docs.python.org/3/library/exceptions.html#IndexError"
            }
        }
    ]

    few_shot_block = ""
    for ex in examples:
        few_shot_block += f"""Example:

Input:
{ex["input"]}

Output:
{json.dumps(ex["output"], indent=2)}

"""

    instruction_block = """You are an expert Python 3 debugging assistant.

Your job is to explain Python error messages clearly for beginners, suggest a fix, and provide a relevant documentation link.

Always respond with a raw JSON object in the following format (no markdown, no code blocks):

{
  "error_type": "...",
  "explanation": "...",
  "suggested_fix": "...",
  "relevant_link": "..."
}

Think through the problem step-by-step before responding, but only output the final JSON.

"""

    query_block = f"""Now explain this error:

Input:
{error}
"""

    if any(keyword in model_to_use.lower() for keyword in ["deepseek", "gemini"]):
        return instruction_block + few_shot_block + query_block
    else:
        return instruction_block + query_block

def is_valid_url(url: str) -> bool:
    if not url.startswith("http"):
        return False
    try:
        resp = requests.head(url, allow_redirects=True, timeout=3)
        return resp.status_code < 400
    except requests.RequestException:
        return False

def search_fallback_link(error_type: str, error_msg: str) -> str:
    query = f"{error_type} site:stackoverflow.com"
    return f"https://duckduckgo.com/?q={requests.utils.quote(query)}"

def explain_error(error_msg: str, retries: int = 3) -> dict:
    prompt = build_prompt(error_msg)
    model_to_use = "deepseek/deepseek-chat-v3-0324:free"
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
            error_type = data.get("error_type", "UnknownError")
            explanation = data.get("explanation", "No explanation available.")
            suggested_fix = data.get("suggested_fix", "No fix available.")
            link = data.get("relevant_link", "")

            # Validate link
            if not is_valid_url(link):
                link = search_fallback_link(error_type, error_msg)

            return {
                "error_type": error_type,
                "explanation": explanation,
                "suggested_fix": suggested_fix,
                "relevant_link": link
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



# from openai import OpenAI, InternalServerError
# import os, json, re, time, requests
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("OPENROUTER_API_KEY")
# client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

# def build_prompt(error: str, model_to_use="deepseek/deepseek-chat-v3-0324:free") -> str:
#     examples = [
#         {
#             "input": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
#             "output": {
#                 "error_type": "TypeError",
#                 "explanation": "You tried to add an integer and a string, which Python does not allow.",
#                 "suggested_fix": "Convert the integer or the string using int() or str() before adding.",
#                 "relevant_link": "https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator"
#             }
#         },
#         {
#             "input": "IndexError: list index out of range",
#             "output": {
#                 "error_type": "IndexError",
#                 "explanation": "You tried to access a position in a list that doesn't exist.",
#                 "suggested_fix": "Make sure your index is within the bounds of the list (0 to len(list)-1).",
#                 "relevant_link": "https://docs.python.org/3/library/exceptions.html#IndexError"
#             }
#         }
#     ]

#     few_shot_block = ""
#     for ex in examples:
#         few_shot_block += f"""Example:

# Input:
# {ex["input"]}

# Output:
# {json.dumps(ex["output"], indent=2)}

# """

#     instruction_block = """You are an expert Python debugging assistant.

# Your job is to explain Python error messages clearly for beginners, suggest a fix, and provide a relevant documentation link.

# Always respond with a raw JSON object in the following format (no markdown, no code blocks):

# {
#   "error_type": "...",
#   "explanation": "...",
#   "suggested_fix": "...",
#   "relevant_link": "..."
# }

# Think through the problem step-by-step before responding, but only output the final JSON.

# """

#     query_block = f"""Now explain this error:

# Input:
# {error}
# """

#     if any(keyword in model_to_use.lower() for keyword in ["deepseek", "gemini"]):
#         return instruction_block + few_shot_block + query_block
#     else:
#         return instruction_block + query_block

# def is_valid_url(url: str) -> bool:
#     if not url.startswith("http"):
#         return False
#     try:
#         resp = requests.head(url, allow_redirects=True, timeout=3)
#         return resp.status_code < 400
#     except requests.RequestException:
#         return False

# def search_fallback_link(error_type: str, error_msg: str) -> str:
#     query = f"{error_type} site:stackoverflow.com"
#     return f"https://duckduckgo.com/?q={requests.utils.quote(query)}"

# def explain_error(error_msg: str, retries: int = 3) -> dict:
#     prompt = build_prompt(error_msg)
#     model_to_use = "deepseek/deepseek-chat-v3-0324:free"
#     for i in range(retries):
#         try:
#             resp = client.chat.completions.create(
#                 model=model_to_use,
#                 messages=[{"role": "user", "content": prompt}],
#             )
#             content = resp.choices[0].message.content.strip()
#             if content.startswith("```"):
#                 content = re.sub(r"^```(?:json)?", "", content).strip().rstrip("```").strip()

#             data = json.loads(content)
#             error_type = data.get("error_type", "UnknownError")
#             explanation = data.get("explanation", "No explanation available.")
#             suggested_fix = data.get("suggested_fix", "No fix available.")
#             link = data.get("relevant_link", "")

#             # Validate link
#             if not is_valid_url(link):
#                 link = search_fallback_link(error_type, error_msg)

#             return {
#                 "error_type": error_type,
#                 "explanation": explanation,
#                 "suggested_fix": suggested_fix,
#                 "relevant_link": link
#             }

#         except InternalServerError:
#             if i < retries - 1:
#                 time.sleep(2 ** i)
#                 continue
#             return {
#                 "error_type": "ModelUnavailable",
#                 "explanation": "Model temporarily unavailable—try again later.",
#                 "suggested_fix": "",
#                 "relevant_link": "https://openrouter.ai/docs"
#             }

#         except Exception as e:
#             if i < retries - 1:
#                 time.sleep(2 ** i)
#                 continue
#             return {
#                 "error_type": "InternalError",
#                 "explanation": "Internal error occurred.",
#                 "suggested_fix": str(e),
#                 "relevant_link": ""
#             }


# from openai import OpenAI, InternalServerError
# import os, json, re, time
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("OPENROUTER_API_KEY")
# client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

# def build_prompt(error: str, model_to_use="deepseek/deepseek-chat-v3-0324:free") -> str:
#     examples = [
#         {
#             "input": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
#             "output": {
#                 "error_type": "TypeError",
#                 "explanation": "You tried to add an integer and a string, which Python does not allow.",
#                 "suggested_fix": "Convert the integer or the string using int() or str() before adding.",
#                 "relevant_link": "https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator"
#             }
#         },
#         {
#             "input": "IndexError: list index out of range",
#             "output": {
#                 "error_type": "IndexError",
#                 "explanation": "You tried to access a position in a list that doesn't exist.",
#                 "suggested_fix": "Make sure your index is within the bounds of the list (0 to len(list)-1).",
#                 "relevant_link": "https://docs.python.org/3/library/exceptions.html#IndexError"
#             }
#         }
#     ]

#     few_shot_block = ""
#     for ex in examples:
#         few_shot_block += f"""Example:

# Input:
# {ex["input"]}

# Output:
# {json.dumps(ex["output"], indent=2)}

# """

#     instruction_block = """You are an expert Python debugging assistant.

# Your job is to explain Python error messages clearly for beginners, suggest a fix, and provide a relevant documentation link.

# Always respond with a raw JSON object in the following format (no markdown, no code blocks):

# {
#   "error_type": "...",
#   "explanation": "...",
#   "suggested_fix": "...",
#   "relevant_link": "..."
# }

# Think through the problem step-by-step before responding, but only output the final JSON.

# """

#     query_block = f"""Now explain this error:

# Input:
# {error}
# """

#     if any(keyword in model_to_use.lower() for keyword in ["deepseek", "gemini"]):
#         return instruction_block + few_shot_block + query_block
#     else:
#         return instruction_block + query_block


# def explain_error(error_msg: str, retries: int = 3) -> dict:
#     prompt = build_prompt(error_msg)
#     model_to_use = "deepseek/deepseek-chat-v3-0324:free"
#     for i in range(retries):
#         try:
#             resp = client.chat.completions.create(
#                 model=model_to_use,
#                 messages=[{"role": "user", "content": prompt}],
#             )
#             content = resp.choices[0].message.content.strip()
#             # strip code fences
#             if content.startswith("```"):
#                 content = re.sub(r"^```(?:json)?", "", content).strip().rstrip("```").strip()
#             data = json.loads(content)
#             # ensure all fields
#             return {
#                 "error_type": data.get("error_type", "UnknownError"),
#                 "explanation": data.get("explanation", "No explanation available."),
#                 "suggested_fix": data.get("suggested_fix", "No fix available."),
#                 "relevant_link": data.get("relevant_link", "")
#             }
#         except InternalServerError:
#             if i < retries - 1:
#                 time.sleep(2 ** i)
#                 continue
#             return {
#                 "error_type": "ModelUnavailable",
#                 "explanation": "Model temporarily unavailable—try again later.",
#                 "suggested_fix": "",
#                 "relevant_link": "https://openrouter.ai/docs"
#             }
#         except Exception as e:
#             if i < retries - 1:
#                 time.sleep(2 ** i)
#                 continue
#             return {
#                 "error_type": "InternalError",
#                 "explanation": "Internal error occurred.",
#                 "suggested_fix": str(e),
#                 "relevant_link": ""
#             }