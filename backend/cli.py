# backend/cli.py
import argparse
from app.core import explain_error

def main():
    parser = argparse.ArgumentParser(description="StackExplain CLI")
    parser.add_argument("error", help="Error message to explain (in quotes)")
    args = parser.parse_args()

    result = explain_error(args.error)
    print("\n🧠 StackExplain Result:")
    print(f"• Error Type:    {result['error_type']}")
    print(f"• Explanation:   {result['explanation']}")
    print(f"• Suggested Fix: {result['suggested_fix']}")
    print(f"• More Info:     {result['relevant_link']}\n")

if __name__ == "__main__":
    main()
