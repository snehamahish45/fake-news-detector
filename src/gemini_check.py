import google.generativeai as genai

API_KEY = "AIzaSyB31H_UkOsdWI1mWcTWxLwnnUrR-7cfFG4"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-pro")

def gemini_verify(news):
    prompt = f"""
    Analyze the following news headline and determine if it is likely REAL, FAKE, or UNCERTAIN.

    Respond ONLY in this format:
    Label: <Real/Fake/Uncertain>
    Reason: <short explanation>

    Headline: {news}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text
        print("Gemini response:", text)
        if "Real" in text:
            return "Real", 0.85, text
        elif "Fake" in text:
            return "Fake", 0.85, text
        else:
            return "Uncertain", 0.5, text

    except:
        return None