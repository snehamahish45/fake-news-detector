import pickle
import os
from src.preprocess import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "..", "models", "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "..", "models", "vectorizer.pkl"), "rb"))

def keyword_check(text):
    fake_keywords = [
        "earn money", "₹", "per day", "guaranteed",
        "no risk", "secret", "click here", "100%",
        "trick", "instant", "free money"
    ]

    for word in fake_keywords:
        if word in text.lower():
            return True
    return False


def predict_news(news):
    cleaned = clean_text(news)
    vec = vectorizer.transform([cleaned])

    prob = model.predict_proba(vec)[0][1]
    pred = model.predict(vec)[0]

    # keyword override
    if keyword_check(news):
        return 0, prob

    return pred, prob