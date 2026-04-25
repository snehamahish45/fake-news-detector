import pandas as pd
import os
import pickle

from preprocess import clean_text
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# 📁 PATH SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(BASE_DIR, "..", "data")
model_path = os.path.join(BASE_DIR, "..", "models")

os.makedirs(model_path, exist_ok=True)

# -----------------------------
# 📥 LOAD DATA
# -----------------------------
fake = pd.read_csv(os.path.join(data_path, "Fake.csv"))
true = pd.read_csv(os.path.join(data_path, "True.csv"))

fake["label"] = 0
true["label"] = 1

df = pd.concat([fake, true], ignore_index=True)

# -----------------------------
# 🔍 CHECK COLUMN
# -----------------------------
if "title" not in df.columns:
    raise Exception("Column 'title' not found in dataset")

# -----------------------------
# 🔥 USE ONLY TITLE (IMPORTANT)
# -----------------------------
df["title"] = df["title"].apply(clean_text)

X = df["title"]
y = df["label"]

# -----------------------------
# 🔀 TRAIN-TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 📊 TF-IDF VECTORIZATION
# -----------------------------
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -----------------------------
# 🤖 MODEL TRAINING (BALANCED)
# -----------------------------
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_vec, y_train)

# -----------------------------
# 📈 EVALUATION
# -----------------------------
y_pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Accuracy: {accuracy:.4f}\n")

print("📊 Classification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# 💾 SAVE MODEL
# -----------------------------
pickle.dump(model, open(os.path.join(model_path, "model.pkl"), "wb"))
pickle.dump(vectorizer, open(os.path.join(model_path, "vectorizer.pkl"), "wb"))

print("\n🚀 Model trained and saved successfully!")