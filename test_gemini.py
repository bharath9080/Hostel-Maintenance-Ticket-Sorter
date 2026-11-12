
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Say Hello! Gemini API is working."
    )

    print("\nSUCCESS!")
    print(response.text)

except Exception as e:
    print("\nGemini API Error:")
    print(e)
