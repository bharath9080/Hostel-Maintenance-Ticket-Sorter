
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"

PROMPT_FILE = BASE_DIR / "system_prompt.txt"

# Retry configuration
MAX_ATTEMPTS = 4
RETRY_BASE_SECONDS = 2

RETRYABLE_STATUS_CODES = {
    429,  # Rate limit
    500,  # Internal server error
    502,  # Bad gateway
    503,  # Service unavailable
    504   # Gateway timeout
}


def classify_with_gemini(complaint):
    """
    Classify a hostel maintenance complaint using Gemini.
    Automatically retries temporary API failures.
    Returns a validated dictionary.
    """

    if not complaint or not complaint.strip():
        raise ValueError("Complaint cannot be empty")

    if not PROMPT_FILE.exists():
        raise FileNotFoundError("system_prompt.txt not found")

    system_prompt = PROMPT_FILE.read_text(
        encoding="utf-8"
    )

    response = None

    for attempt in range(1, MAX_ATTEMPTS + 1):

        try:
            print(
                f"Calling Gemini (attempt {attempt}/{MAX_ATTEMPTS})..."
            )

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=complaint,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    temperature=0
                )
            )

            break

        except errors.APIError as error:

            status_code = getattr(error, "code", None)

            if (
                status_code not in RETRYABLE_STATUS_CODES
                or attempt == MAX_ATTEMPTS
            ):
                print("Gemini API request failed:", error)
                raise

            wait_seconds = RETRY_BASE_SECONDS * (
                2 ** (attempt - 1)
            )

            print(
                f"Gemini temporarily unavailable "
                f"(HTTP {status_code}). "
                f"Retrying in {wait_seconds} seconds..."
            )

            time.sleep(wait_seconds)

    if response is None or not response.text:
        raise ValueError("Gemini returned an empty response")

    try:
        result = json.loads(response.text)

    except json.JSONDecodeError as error:
        raise ValueError(
            "Gemini returned invalid JSON"
        ) from error

    return validate_gemini_response(result)


def validate_gemini_response(response):
    """
    Validate Gemini's classification response.
    """

    required_fields = {
        "room",
        "issue",
        "urgent",
        "summary"
    }

    if not isinstance(response, dict):
        raise ValueError("Response must be a dictionary")

    if set(response.keys()) != required_fields:
        raise ValueError("Missing or unexpected fields")

    if response["room"] is not None:
        if not isinstance(response["room"], str):
            raise ValueError("Room must be a string or None")

    if not isinstance(response["issue"], str):
        raise ValueError("Issue must be a string")

    if response["issue"] not in {
        "electrical",
        "plumbing",
        "carpentry",
        "cleaning",
        "internet",
        "other"
    }:
        raise ValueError("Invalid issue category")

    if not isinstance(response["urgent"], bool):
        raise ValueError("Urgent must be True or False")

    if not isinstance(response["summary"], str):
        raise ValueError("Summary must be a string")

    if len(response["summary"].split()) > 10:
        raise ValueError(
            "Summary must contain at most 10 words"
        )

    return response
