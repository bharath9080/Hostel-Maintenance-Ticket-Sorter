
import json


def classify_with_gemini(complaint):
    """
    Sends a complaint to the Gemini service
    and returns structured classification data.

    Live API connection will be added after
    faculty-managed, age-compliant access is arranged.
    """

    if not complaint or not complaint.strip():
        raise ValueError("Complaint cannot be empty")

    # Placeholder: no API request is made yet.
    raise NotImplementedError(
        "Gemini API connection is not configured yet."
    )


def validate_gemini_response(response):
    """
    Checks whether the classification response
    contains the required fields.
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

    if response["room"] is not None and not isinstance(response["room"], str):
        raise ValueError("Room must be a string or None")

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
        raise ValueError("Summary must contain at most 10 words")

    return response
