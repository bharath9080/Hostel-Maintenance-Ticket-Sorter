
from gemini_classifier import classify_with_gemini

test_complaints = [
    "Sparks coming from the switchboard in A105.",
    "Water leaking from the bathroom tap in C310.",
    "WiFi is not working in B205.",
    "The bathroom is dirty in D110.",
    "Water is leaking near the electrical switch in A115."
]

for complaint in test_complaints:

    print("\nComplaint:", complaint)

    try:
        result = classify_with_gemini(complaint)

        print("Gemini Classification:")
        print(result)

    except Exception as error:
        print("ERROR:", error)
