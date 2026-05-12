import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

def gemini_verify(text):
    prompt = f"""
    Check whether this news is real or fake.
    Give a short explanation.

    News:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text