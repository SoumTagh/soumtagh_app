import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline
from utils import get_reviews

st.set_page_config(page_title="Sentiment Analysis", page_icon="🧠", layout="wide")

st.title("🧠 Sentiment Analysis")
st.write("Sentiment analysis on user reviews for each app in the search results.")
st.divider()

# checking session state
if "results_df" not in st.session_state:
    st.warning("No data found. Please run a search on the Results page first.")
    st.stop()

df = st.session_state["results_df"].copy()

# loading model once and cache it
@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment",
        tokenizer="cardiffnlp/twitter-roberta-base-sentiment",
    )

sentiment_pipeline = load_model()

def label_to_sentiment(label):
    mapping = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
    return mapping.get(label, label)

def analyze_reviews(reviews_df):
    """Run sentiment on each review, return dataframe with sentiment column."""
    texts = reviews_df["content"].dropna().tolist()
    # truncates to 512 chars to avoid token limit issues
    texts = [t[:512] for t in texts]
    results = sentiment_pipeline(texts, truncation=True, max_length=128, batch_size=16)
    reviews_df = reviews_df.copy()
    reviews_df["sentiment"] = [label_to_sentiment(r["label"]) for r in results]
    reviews_df["confidence"] = [round(r["score"], 3) for r in results]
    return reviews_df

def compute_score(reviews_df):
    """Compute overall sentiment score for an app (% positive)."""
    counts = reviews_df["sentiment"].value_counts()
    total = len(reviews_df)
    pos = counts.get("Positive", 0)
    return round((pos / total) * 100, 1) if total > 0 else 0

# run analysis
if st.button("Run Sentiment Analysis"):
    app_ids = df["appId"].tolist()
    app_titles = df.set_index("appId")["title"].to_dict()

    scores = []
    all_reviews = []

    progress = st.progress(0, text="Fetching reviews and analyzing sentiment...")

    for i, app_id in enumerate(app_ids):
        try:
            reviews_df = get_reviews(app_id, count=50)
            if not reviews_df.empty:
                reviews_df = analyze_reviews(reviews_df)
                reviews_df["appId"] = app_id
                reviews_df["appTitle"] = app_titles.get(app_id, app_id)
                all_reviews.append(reviews_df)
                score = compute_score(reviews_df)
                scores.append({"appId": app_id, "title": app_titles.get(app_id, app_id), "sentiment_score": score})
        except Exception as e:
            st.warning(f"Could not analyze {app_id}: {e}")

        progress.progress((i + 1) / len(app_ids), text=f"Analyzed {i+1}/{len(app_ids)} apps...")

    st.session_state["sentiment_scores"] = pd.DataFrame(scores)
    st.session_state["all_reviews"] = pd.concat(all_reviews, ignore_index=True) if all_reviews else pd.DataFrame()
    st.success("Sentiment analysis complete!")

# display results 
if "sentiment_scores" in st.session_state:
    scores_df = st.session_state["sentiment_scores"]
    all_reviews_df = st.session_state["all_reviews"]

    st.divider()

    # row 1 : overall sentiment scores bar chart 
    st.subheader("Sentiment Score per App (% Positive Reviews)")
    fig = px.bar(
        scores_df.sort_values("sentiment_score", ascending=True),
        x="sentiment_score", y="title", orientation="h",
        labels={"sentiment_score": "% Positive", "title": ""},
        color="sentiment_score", color_continuous_scale=["#FFE5D0", "#FF5E00"],
        range_color=[0, 100],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # row 2 : per app detailed breakdown
    st.subheader("Detailed Sentiment Breakdown by App")

    col1, col2 = st.columns([1, 2])

    with col1:
        selected_app = st.selectbox("Select an app:", scores_df["title"].tolist())

    app_reviews = all_reviews_df[all_reviews_df["appTitle"] == selected_app]

    with col2:
        sentiment_counts = app_reviews["sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]
        color_map = {"Positive": "#FF5E00", "Neutral": "#FFB380", "Negative": "#FFE5D0"}
        fig2 = px.pie(sentiment_counts, names="Sentiment", values="Count", color="Sentiment", color_discrete_map=color_map)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # row 3 : sample reviews for selected app
    st.subheader(f"Sample Reviews — {selected_app}")

    sentiment_filter = st.radio("Filter by sentiment:", ["All", "Positive", "Neutral", "Negative"], horizontal=True)

    filtered = app_reviews if sentiment_filter == "All" else app_reviews[app_reviews["sentiment"] == sentiment_filter]

    st.dataframe(
        filtered[["userName", "content", "score", "sentiment", "confidence"]].head(20),
        use_container_width=True,
        column_config={
            "score":      st.column_config.ProgressColumn("Rating", min_value=0, max_value=5),
            "confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=1),
        },
    )