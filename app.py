import streamlit as st
from api.news_api import get_news
from src.predict import predict_news
from datetime import datetime
import pandas as pd

# -------------------------------
# 🎨 CUSTOM CSS
# -------------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #1c1f26;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

.title {
    font-size: 28px;
    font-weight: bold;
    color: #00d4ff;
}

.news {
    font-size: 18px;
    color: white;
}

.real {
    color: #00ff9d;
    font-weight: bold;
}

.fake {
    color: #ff4b4b;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧠 SESSION STATE
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# 🚀 PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Fake News Detector", layout="wide")

# -------------------------------
# 📌 HEADER
# -------------------------------
st.markdown('<p class="title">📰 Fake News Detection Dashboard</p>', unsafe_allow_html=True)
st.caption("AI-powered real-time analysis system")

# -------------------------------
# ⚙️ SIDEBAR
# -------------------------------
st.sidebar.markdown("## ⚙️ Controls")
st.sidebar.markdown("---")

category = st.sidebar.selectbox(
    "📂 Category",
    ["general", "business", "technology", "sports"]
)

st.sidebar.markdown("### ℹ️ About")
st.sidebar.info("Detect fake news using AI + NLP model")

# -------------------------------
# 🧭 TABS
# -------------------------------
tab1, tab2, tab3 = st.tabs(["🔍 Check News", "📡 Live Feed", "📊 Analytics"])

# ===============================
# 🔍 TAB 1: CHECK NEWS
# ===============================
with tab1:
    st.subheader("Check Custom News")

    user_input = st.text_input("Enter headline:")

    if st.button("🔍 Analyze") and user_input:
        pred, prob = predict_news(user_input)

        if pred == 1:
            result = "Real News ✅"
            color_class = "real"
        else:
            result = "Fake News ❌"
            color_class = "fake"

        st.markdown(f"""
        <div class="card">
            <p class="news">{user_input}</p>
            <p class="{color_class}">{result} ({round(prob*100,2)}%)</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(int(prob * 100))

        if prob < 0.6:
            st.warning("⚠️ Low confidence prediction")

        if pred == 0 and prob > 0.8:
            st.warning("🚨 High Risk Fake News!")

        st.session_state.history.append({
            "News": user_input,
            "Prediction": "Real" if pred == 1 else "Fake",
            "Confidence": round(prob * 100, 2)
        })

    st.markdown("### 🕘 History")

    if st.session_state.history:
        for item in st.session_state.history[::-1]:
            st.write(f"• {item['News']} → {item['Prediction']} ({item['Confidence']}%)")
    else:
        st.write("No history yet")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.download_button("📥 Download Report", df.to_csv(index=False), "report.csv")

# ===============================
# 📡 TAB 2: LIVE NEWS
# ===============================
with tab2:
    st.subheader("Live News Feed")

    news_list = get_news(category)

    fake_count = 0
    real_count = 0

    if not news_list:
        st.error("No news available")
    else:
        for title, link in news_list[:5]:
            pred, prob = predict_news(title)

            if pred == 1:
                result = "Real News ✅"
                color_class = "real"
                real_count += 1
            else:
                result = "Fake News ❌"
                color_class = "fake"
                fake_count += 1

            st.markdown(f"""
            <div class="card">
                <p class="news"><a href="{link}" target="_blank">{title}</a></p>
                <p class="{color_class}">{result} ({round(prob*100,2)}%)</p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(prob * 100))

# ===============================
# 📊 TAB 3: ANALYTICS
# ===============================
with tab3:
    st.subheader("Prediction Summary")

    col1, col2 = st.columns(2)

    col1.markdown(f"""
    <div class="card">
        <h3 style='color:#00ff9d;'>Real News</h3>
        <h2>{real_count}</h2>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
        <h3 style='color:#ff4b4b;'>Fake News</h3>
        <h2>{fake_count}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.bar_chart({
        "Real": [real_count],
        "Fake": [fake_count]
    })

# -------------------------------
# ⏱ FOOTER
# -------------------------------
st.caption(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")