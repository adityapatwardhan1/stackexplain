#!/usr/bin/python3

import argparse
import sys
import pyperclip
import platform
from stackexplain.app.core import explain_error

MODEL_MAP = {
    "deepseek": "deepseek/deepseek-chat-v3-0324:free",
    "gemini": "google/gemini-2.0-flash-exp:free",
    "mistral": "mistralai/mistral-small-3.2-24b-instruct:free",
}

def get_error_input():
    if not sys.stdin.isatty():
        # Reading from stdin (e.g., pasted multiline input)
        return sys.stdin.read()
    else:
        # Prompt user
        ending_hint = "Ctrl+D" if platform.system() != "Windows" else "Ctrl+Z then Enter"
        print(f"Paste your error below (end with {ending_hint}), or leave empty to use clipboard:")
        error_input = sys.stdin.read()
        if error_input.strip():
            return error_input
        else:
            try:
                clipboard_text = pyperclip.paste()
                if clipboard_text.strip():
                    print("[Using clipboard contents as error input]\n")
                    return clipboard_text
                else:
                    print("❌ Clipboard is empty. Please paste an error or type one.")
                    sys.exit(1)
            except pyperclip.PyperclipException:
                print("⚠️ Could not access clipboard.")
                os_name = platform.system()
                if os_name == "Linux":
                    print("Try installing a clipboard tool: `sudo apt install xclip`")
                elif os_name == "Darwin":
                    print("Ensure `pbpaste` is available in your PATH.")
                elif os_name == "Windows":
                    print("Try running in a full Windows terminal.")
                else:
                    print("Unknown OS. Clipboard may not be supported.")
                sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Application CLI")
    parser.add_argument("error", nargs="?", help="Error message (optional: use stdin or clipboard)")
    parser.add_argument(
        "--model",
        choices=MODEL_MAP.keys(),
        default="deepseek",
        help="Choose model to use: deepseek (default), gemini, or mistral"
    )
    args = parser.parse_args()

    if args.error:
        error = args.error
    else:
        error = get_error_input()

    model_full_name = MODEL_MAP.get(args.model, MODEL_MAP["deepseek"])

    print("Reasoning...")
    result = explain_error(error, model_to_use=model_full_name)

    print(f"• Error Type:    {result['error_type']}")
    print(f"• Explanation:   {result['explanation']}")
    print(f"• Suggested Fix: {result['suggested_fix']}")

    if len(result.get('relevant_links', [])) > 0:
        print(f"• More Info:")
        for link in result['relevant_links']:
            print(f"    • {link}")

if __name__ == "__main__":
    main()


# #!/usr/bin/python3

# import argparse
# import sys
# import pyperclip
# import platform
# from stackexplain.app.core import explain_error

# def get_error_input():
#     if not sys.stdin.isatty():
#         # Reading from stdin (e.g., pasted multiline input)
#         return sys.stdin.read()
#     else:
#         # Prompt user
#         ending_hint = "Ctrl+D" if platform.system() != "Windows" else "Ctrl+Z then Enter"
#         print(f"Paste your error below (end with {ending_hint}), or leave empty to use clipboard:")
#         error_input = sys.stdin.read()
#         if error_input.strip():
#             return error_input
#         else:
#             try:
#                 clipboard_text = pyperclip.paste()
#                 if clipboard_text.strip():
#                     print("[Using clipboard contents as error input]\n")
#                     return clipboard_text
#                 else:
#                     print("❌ Clipboard is empty. Please paste an error or type one.")
#                     sys.exit(1)
#             except pyperclip.PyperclipException:
#                 print("⚠️ Could not access clipboard.")
#                 os_name = platform.system()
#                 if os_name == "Linux":
#                     print("Try installing a clipboard tool: `sudo apt install xclip`")
#                 elif os_name == "Darwin":
#                     print("Ensure `pbpaste` is available in your PATH.")
#                 elif os_name == "Windows":
#                     print("Try running in a full Windows terminal.")
#                 else:
#                     print("Unknown OS. Clipboard may not be supported.")
#                 sys.exit(1)

# def main():
#     parser = argparse.ArgumentParser(description="StackExplain CLI")
#     parser.add_argument("error", nargs="?", help="Error message (optional: use stdin or clipboard)")
#     args = parser.parse_args()

#     if args.error:
#         error = args.error
#     else:
#         error = get_error_input()

#     result = explain_error(error)

#     print("\n🧠 StackExplain Result:")
#     print(f"• Error Type:    {result['error_type']}")
#     print(f"• Explanation:   {result['explanation']}")
#     print(f"• Suggested Fix: {result['suggested_fix']}")
#     print(f"• More Info:")
#     for link in result['relevant_links']:
#         print(f"    • {link}")

# if __name__ == "__main__":
#     main()

