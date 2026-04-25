import streamlit as st
from src.predict import predict_news
from api.news_api import get_news
from api.free_news_search import search_articles
from datetime import datetime

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Fake News AI Pro", layout="wide")

# -------------------------
# VERIFY FUNCTION (🔥 CORE LOGIC)
# -------------------------
def verify_with_articles(headline, articles):
    headline_words = set(headline.lower().split())
    match_count = 0

    for art in articles:
        title_words = set(art["title"].lower().split())
        overlap = headline_words.intersection(title_words)

        if len(overlap) >= 3:
            match_count += 1

    if match_count >= 2:
        return "Verified", 0.9
    elif match_count == 1:
        return "Partially Verified", 0.7
    else:
        return "Not Verified", 0.4

# -------------------------
# PREMIUM CSS
# -------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}

.title {
    font-size: 32px;
    font-weight: bold;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.real { color:#00ff9d; font-weight:bold; }
.fake { color:#ff4b4b; font-weight:bold; }
.warn { color:#ffaa00; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("⚙️ Controls")

category = st.sidebar.selectbox(
    "Category",
    ["general","business","technology","sports"]
)

show_fake_only = st.sidebar.checkbox("Show only Fake News")

# -------------------------
# HEADER
# -------------------------
st.markdown('<p class="title">🧠 Fake News AI Dashboard</p>', unsafe_allow_html=True)
st.caption("AI + Real News Verification + Live Matching Articles")

# -------------------------
# TABS
# -------------------------
tab1, tab2, tab3 = st.tabs(["🔍 Check", "📡 Live", "📊 Analytics"])

# =========================
# 🔍 CHECK TAB
# =========================
with tab1:
    st.subheader("Check News")

    user_input = st.text_input("Enter headline:")

    if st.button("Analyze") and user_input:

        label, prob, explain = predict_news(user_input)

        st.markdown(f"""
        <div class="card">
            <h3>{user_input}</h3>
            <p class="{ 'real' if label=='Real' else 'fake' if label=='Fake' else 'warn' }">
            {label} ({round(prob*100,2)}%)
            </p>
            <p>🧠 {explain}</p>
        </div>
        """, unsafe_allow_html=True)

        st.metric("AI Confidence", f"{round(prob*100,2)}%")
        st.progress(int(prob * 100))

        # 🔎 VERIFY LINKS
        query = user_input.replace(" ", "+")
        st.info("🔎 Verify manually:")
        st.markdown(f"""
- [Google News](https://news.google.com/search?q={query})
- [Reuters](https://www.reuters.com/search/news?blob={query})
- [BBC](https://www.bbc.com/news)
""")

        # 📰 MATCHING ARTICLES
        st.subheader("📰 Real Matching Articles")

        articles = search_articles(user_input)

        if articles:
            for art in articles:
                st.markdown(f"- [{art['title']}]({art['link']})")

            # 🔥 VERIFY STATUS
            status, score = verify_with_articles(user_input, articles)

            st.subheader("🔍 Verification Result")

            if status == "Verified":
                st.success(f"✅ {status}")
            elif status == "Partially Verified":
                st.warning(f"⚠️ {status}")
            else:
                st.error(f"❌ {status}")

            st.progress(int(score * 100))

        else:
            st.warning("No matching articles found")

# =========================
# 📡 LIVE TAB
# =========================
with tab2:
    st.subheader("Live News Feed")

    news_list = get_news(category)

    for title, link in news_list[:6]:

        label, prob, explain = predict_news(title, link)

        if show_fake_only and label != "Fake":
            continue

        st.markdown(f"""
        <div class="card">
            <h4><a href="{link}" target="_blank">{title}</a></h4>
            <p class="{ 'real' if label=='Real' else 'fake' if label=='Fake' else 'warn' }">
            {label} ({round(prob*100,2)}%)
            </p>
            <p>🧠 {explain}</p>
        </div>
        """, unsafe_allow_html=True)

        st.metric("Confidence", f"{round(prob*100,2)}%")
        st.progress(int(prob * 100))

        # 🔎 MATCH ARTICLES
        articles = search_articles(title)

        if articles:
            st.markdown("🔎 Related Articles:")
            for art in articles[:3]:
                st.markdown(f"- [{art['title']}]({art['link']})")

            status, score = verify_with_articles(title, articles)

            if status == "Verified":
                st.success("✅ Verified by sources")
            elif status == "Partially Verified":
                st.warning("⚠️ Partially Verified")
            else:
                st.error("❌ Not Verified")

            st.progress(int(score * 100))

# =========================
# 📊 ANALYTICS TAB
# =========================
with tab3:
    st.subheader("Analytics")

    news_list = get_news(category)

    fake_count = 0
    real_count = 0

    for title, link in news_list[:10]:
        label, _, _ = predict_news(title, link)

        if label == "Real":
            real_count += 1
        elif label == "Fake":
            fake_count += 1

    col1, col2 = st.columns(2)

    col1.metric("Real News", real_count)
    col2.metric("Fake News", fake_count)

    st.bar_chart({
        "Real": [real_count],
        "Fake": [fake_count]
    })

# -------------------------
# FOOTER
# -------------------------
st.caption(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")