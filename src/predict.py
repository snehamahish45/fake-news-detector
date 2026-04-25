import os
import pickle

from src.preprocess import clean_text
from src.gemini_check import gemini_verify

# -----------------------------
# LOAD MODEL + VECTORIZER
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "..", "models")

model = pickle.load(open(os.path.join(model_path, "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(model_path, "vectorizer.pkl"), "rb"))
def predict_news(news, url=None):

    news_lower = news.lower()

    # -----------------------------
    # 🔥 0️⃣ SMART REALITY FILTER
    # -----------------------------
    if any(word in news_lower for word in ["announced", "launched", "released", "officially"]):
        return "Possible Real", 0.65, "Likely recent news — verify with trusted sources"

    # -----------------------------
    # 1️⃣ GEMINI AI (PRIMARY)
    # -----------------------------
    result = gemini_verify(news)

    if result:
        label, prob, explain = result

        if label == "Real":
            return "Real", prob, explain

        elif label == "Fake":
            return "Fake", prob, explain

        else:
            return "Possible Real", 0.6, "AI uncertain — may be real"

    # -----------------------------
    # 2️⃣ TRUSTED SOURCE CHECK
    # -----------------------------
    if url:
        trusted = ["bbc", "cnn", "reuters", "ndtv"]
        if any(t in url.lower() for t in trusted):
            return "Real", 0.9, "Trusted news source"

    # -----------------------------
    # 3️⃣ ML MODEL (LOW PRIORITY)
    # -----------------------------
    cleaned = clean_text(news)
    vec = vectorizer.transform([cleaned])

    prob = model.predict_proba(vec)[0][1]

    if prob > 0.8:
        return "Real", prob, "ML prediction"
    elif prob < 0.2:
        return "Fake", 1 - prob, "ML prediction"
    else:
        return "Possible Real", prob, "Low confidence — likely real"