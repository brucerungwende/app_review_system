import streamlit as st
import pandas as pd
from google_play_scraper import app, reviews
from textblob import TextBlob
# import matplotlib.pyplot as plt

# Note:
# matplotlib is not needed because Streamlit's st.bar_chart handles charts easily.
# Included only for reference.

# -------------------------------
# Helper functions
# -------------------------------

# Multi-country fallback for app info
def fetch_app_info(package_name):
    countries = ["us", "gb", "ca", "au", "in", "de", "fr", "jp"]
    for country in countries:
        try:
            info = app(package_name, lang='en', country=country)
            return info, country
        except:
            continue
    return None, None

# Fetch reviews with fallback
def fetch_reviews(package_name, country, count=200):
    try:
        result, _ = reviews(package_name, lang='en', country=country, count=count)
        return result
    except:
        # fallback to smaller batch
        result, _ = reviews(package_name, lang='en', country=country, count=50)
        return result

# Sentiment analysis
def analyze_sentiment(text):
    tb = TextBlob(text)
    if tb.sentiment.polarity > 0.1:
        return "positive"
    elif tb.sentiment.polarity < -0.1:
        return "negative"
    else:
        return "neutral"

# -------------------------------
# Streamlit Page Setup
# -------------------------------

st.set_page_config(page_title="App Review Analyzer", layout="wide")

# Session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "welcome"

def go_to(page_name):
    st.session_state.page = page_name

# -------------------------------
# Sidebar Navigation
# -------------------------------
with st.sidebar:
    st.header("🔎 Navigation")
    choice = st.radio(
        "Go to page:",
        ["Welcome", "Analyzer", "About / Help"],
        index=["welcome", "analyzer", "about"].index(st.session_state.page)
    )
    if choice == "Welcome":
        go_to("welcome")
    elif choice == "Analyzer":
        go_to("analyzer")
    else:
        go_to("about")
    st.markdown("---")
    if st.button("❌ Exit App"):
        st.stop()

# -------------------------------
# Welcome Page
# -------------------------------
if st.session_state.page == "welcome":
    st.title("👋 Welcome to App Review Analyzer")
    st.markdown(
        """
        Analyze Google Play Store reviews and get smart recommendations.

        **Features:**
        - Fetch real user reviews instantly.
        - Run sentiment analysis (positive, negative, neutral).
        - View charts and statistics.
        - Get recommendations based on review trends.
        """
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➡️ Next"):
            go_to("analyzer")
    with col2:
        if st.button("ℹ️ About / Help"):
            go_to("about")
    with col3:
        if st.button("❌ Exit"):
            st.stop()

# -------------------------------
# Analyzer Page
# -------------------------------
elif st.session_state.page == "analyzer":
    st.title("📱 App Review Analyzer")
    st.info("💡 Need guidance? Go to the **About / Help** page for instructions.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Previous"):
            go_to("welcome")
    with col2:
        if st.button("ℹ️ About / Help"):
            go_to("about")
    with col3:
        if st.button("❌ Exit"):
            st.stop()

    # User input
    app_package = st.text_input("Enter Google Play package name (e.g., com.telegram.android):")

    if app_package:
        info, country = fetch_app_info(app_package)
        if info is None:
            st.error(f"❌ App '{app_package}' not found in common countries.")
        else:
            st.success(f"✅ App found in {country.upper()} store!")
            st.subheader(info['title'])
            st.image(info['icon'], width=100)
            st.markdown(f"**Developer:** {info['developer']}")
            st.markdown(f"**Rating:** {info['score']} ⭐")
            st.markdown(f"**Installs:** {info['installs']}")
            st.markdown(f"**Description:** {info['description'][:300]}...")

            review_data = fetch_reviews(app_package, country)
            df = pd.DataFrame(review_data)[['content']]
            df['sentiment'] = df['content'].apply(analyze_sentiment)

            # Sentiment distribution
            st.subheader("📊 Sentiment Distribution")
            st.bar_chart(df['sentiment'].value_counts())

            # Recommendation
            st.subheader("📌 Recommendation")
            total_reviews = len(df)
            positive = df[df['sentiment']=="positive"].shape[0]
            negative = df[df['sentiment']=="negative"].shape[0]
            positive_ratio = positive / total_reviews if total_reviews>0 else 0
            negative_ratio = negative / total_reviews if total_reviews>0 else 0

            if positive_ratio > 0.7:
                st.success("✅ This app is well-rated. You should consider downloading it.")
            elif negative_ratio > 0.5:
                st.error("❌ Mostly negative reviews. Be cautious.")
            else:
                st.warning("⚠️ Mixed reviews. Read more before deciding.")

            with st.expander("📃 See Sample Reviews"):
                st.write(df.head(10))

# -------------------------------
# About / Help Page
# -------------------------------
elif st.session_state.page == "about":
    st.title("ℹ️ About & Help")
    st.markdown(
        """
        **App Review Analyzer** allows you to explore Google Play Store reviews.

        **How to use:**
        1. Go to the Analyzer page.
        2. Enter a Google Play package name (e.g., com.whatsapp).
        3. View reviews, sentiment analysis, charts, and recommendations.

        **Navigation:**
        - Next / Previous buttons move between pages.
        - Sidebar menu can also navigate directly.
        - Press Exit to quit anytime.
        """
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Back to Welcome"):
            go_to("welcome")
    with col2:
        if st.button("⬅️ Back to Analyzer"):
            go_to("analyzer")
    with col3:
        if st.button("❌ Exit"):
            st.stop()
