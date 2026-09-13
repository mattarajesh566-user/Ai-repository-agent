import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Load .env from the project folder
project_folder = Path(__file__).resolve().parent
env_file = project_folder / ".env"
load_dotenv(dotenv_path=env_file)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. Check your .env file."
    )

client = genai.Client(api_key=api_key)


def analyze_test_results(results):
    """
    Sends regression-testing results to Gemini
    and returns an AI-generated analysis.
    """

    prompt = f"""
You are an expert software testing engineer.

Analyze the following regression-testing results.

Testing results:
{json.dumps(results, indent=2, default=str)}

Provide a clear report containing:

1. Overall test summary
2. Passed tests
3. Failed tests
4. Possible bugs
5. Severity of each possible bug:
   - Low
   - Medium
   - High
   - Critical
6. Recommended next steps

Important:
- Do not claim that a failed test is definitely a real bug.
- Use the phrase "possible bug" when the evidence is not conclusive.
- Keep the explanation simple and professional.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text