
from gemini_classifier import validate_gemini_response

# Test 1: Valid response
valid_response = {
    "room": "A105",
    "issue": "electrical",
    "urgent": True,
    "summary": "Sparks coming from switchboard"
}

try:
    result = validate_gemini_response(valid_response)

    print("TEST 1: PASSED")
    print("Validated response:", result)

except ValueError as error:
    print("TEST 1: FAILED")
    print(error)


# Test 2: Invalid issue category
invalid_response = {
    "room": "A105",
    "issue": "mechanical",
    "urgent": False,
    "summary": "Fan making noise"
}

try:
    validate_gemini_response(invalid_response)

    print("TEST 2: FAILED")

except ValueError as error:
    print("\nTEST 2: PASSED")
    print("Error detected:", error)

# Test 3: Invalid urgency value
invalid_urgency = {
    "room": "A105",
    "issue": "electrical",
    "urgent": "yes",
    "summary": "Sparks from switchboard"
}

try:
    validate_gemini_response(invalid_urgency)
    print("\nTEST 3: FAILED")
except ValueError as error:
    print("\nTEST 3: PASSED")
    print("Error detected:", error)


# Test 4: Summary exceeds 10 words
long_summary = {
    "room": "A105",
    "issue": "electrical",
    "urgent": True,
    "summary": "There are several electrical sparks coming from the main switchboard in the hostel room"
}

try:
    validate_gemini_response(long_summary)
    print("\nTEST 4: FAILED")
except ValueError as error:
    print("\nTEST 4: PASSED")
    print("Error detected:", error)
