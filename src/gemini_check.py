import os
from dotenv import load_dotenv
import google.generativeai as genai

# ==============================
# LOAD ENV VARIABLES
# ==============================
load_dotenv()

API_KEY = os.getenv("AIzaSyAuD_a8TwlKtJ0wdkJJ_KNszowU1jCWRrU")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found. Add it in .env file or Render environment.")

# ==============================
# CONFIGURE GEMINI
# ==============================
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-pro")

# ==============================
# GEMINI FACT CHECK FUNCTION
# ==============================
def gemini_verify(news):
    prompt = f"""
You are a fact-checking assistant.

Analyze the following news headline and determine if it is:
- REAL
- FAKE
- UNCERTAIN

Also provide a short reasoning.

Respond STRICTLY in this format:
Label: <Real/Fake/Uncertain>
Reason: <short explanation>

Headline: {news}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # DEBUG (optional)
        print("Gemini response:", text)

        # ==============================
        # PARSE RESPONSE SAFELY
        # ==============================
        label = "Uncertain"
        reason = text

        if "Label:" in text:
            try:
                label_part = text.split("Label:")[1].split("\n")[0].strip()
                reason_part = text.split("Reason:")[1].strip()

                label = label_part.capitalize()
                reason = reason_part
            except:
                pass

        # ==============================
        # CONFIDENCE LOGIC
        # ==============================
        if label == "Real":
            prob = 0.85
        elif label == "Fake":
            prob = 0.85
        else:
            prob = 0.5

        return label, prob, f"Gemini: {reason}"

    except Exception as e:
        print("Gemini error:", e)
        return None