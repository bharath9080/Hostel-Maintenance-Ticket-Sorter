
import re


def classify_with_gemini(complaint):
    """
    Local mock classifier for testing.
    No external API request is made.
    """

    if not complaint or not complaint.strip():
        raise ValueError("Complaint cannot be empty")

    text = complaint.lower()

    # Water near electrical fittings
    if "water" in text and (
        "electrical fittings" in text or "near the switch" in text
    ):
        issue = "electrical"
        urgent = True

    # Electrical complaints
    elif any(word in text for word in [
        "spark", "burning smell", "shock", "fan", "switchboard"
    ]):
        issue = "electrical"
        urgent = any(word in text for word in [
            "spark", "burning smell", "shock"
        ])

    # Plumbing complaints
    elif any(word in text for word in ["leak", "pipe", "tap"]):
        issue = "plumbing"
        urgent = any(word in text for word in [
            "overflowing", "flooding"
        ])

    # Internet complaints
    elif "wifi" in text or "internet" in text:
        issue = "internet"
        urgent = False

    # Cleaning complaints
    elif any(word in text for word in [
        "clean", "housekeeping", "dirty"
    ]):
        issue = "cleaning"
        urgent = False

    # Carpentry complaints
    elif any(word in text for word in [
        "door", "window", "handle"
    ]):
        issue = "carpentry"
        urgent = False

    else:
        issue = "other"
        urgent = False

    # Extract room number exactly as written
    match = re.search(
        r"\b[A-D][1-4](?:0[1-9]|1[0-9]|20)\b",
        complaint.upper()
    )

    response = {
        "room": match.group(0) if match else None,
        "issue": issue,
        "urgent": urgent,
        "summary": " ".join(complaint.split()[:10])
    }

    return validate_gemini_response(response)


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
