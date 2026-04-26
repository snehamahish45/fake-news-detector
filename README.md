# 🧠 Fake News Detection System (Pro)

AI-powered fake news detection system with real-time news verification, smart NLP model, and modern Streamlit UI.

---

## 🚀 Live Features

* 🔍 **Headline Analysis** – Detect whether news is Real, Fake, or Uncertain
* 🧠 **Machine Learning Model** – Trained on real + fake news datasets
* 🤖 **Gemini AI Verification** – Adds intelligent reasoning (Real / Fake explanation)
* 📡 **Live News Feed** – Fetch latest news automatically
* 🔗 **Source Matching** – Suggest trusted sites for verification
* 📊 **Analytics Dashboard** – Real vs Fake distribution
* 🎨 **Modern UI** – Clean glassmorphism dashboard using Streamlit

---

## 🧰 Tech Stack

* Python 🐍
* Streamlit (Frontend UI)
* Scikit-learn (ML Model)
* NLP (TF-IDF + Linear SVM)
* Google Gemini API (AI verification)
* Feedparser (Live news fetch)

---

## 📂 Project Structure

```
fake-news-detector/
│
├── app.py                 # Main Streamlit app
├── requirements.txt      # Dependencies
├── .gitignore
│
├── models/
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── src/
│   ├── predict.py
│   ├── preprocess.py
│   ├── train.py
│   └── gemini_check.py
│
├── api/
│   ├── news_api.py
│   └── free_news_search.py
│
├── data/
│   ├── Fake.csv
│   └── True.csv
```

---

## ⚙️ Installation (Local Setup)

### 1. Clone repo

```
git clone https://github.com/snehamahish45/fake-news-detector-pro.git
cd fake-news-detector-pro
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Add environment variable

Create `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

OR set manually:

```
export GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Run App

```
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 🌐 Deployment (Render)

### Build Command

```
pip install -r requirements.txt
```

### Start Command

```
streamlit run app.py --server.port 10000 --server.address 0.0.0.0
```

### Environment Variable (Render)

```
GEMINI_API_KEY=your_api_key_here
```

---

## 📊 How it Works

1. User enters news headline
2. Text is cleaned using NLP
3. Converted to vectors using TF-IDF
4. ML model predicts Real / Fake
5. Gemini AI verifies reasoning
6. System shows confidence + explanation

---

## ⚠️ Limitations

* ML model may misclassify new or complex headlines
* Gemini API depends on internet + quota
* Real-time fact checking is approximate (not official fact-check API)

---

## 🔮 Future Improvements

* Improve accuracy using Deep Learning (BERT)
* Add real fact-check APIs
* Add user feedback system
* Multi-language support
* Fake image detection

---

## 👨‍💻 Author

**Sneha Mahish**
GitHub: https://github.com/snehamahish45

---

## ⭐ Support

If you like this project:

⭐ Star the repo
🍴 Fork it
💡 Contribute improvements

---

## 📜 License

This project is for educational purposes.
