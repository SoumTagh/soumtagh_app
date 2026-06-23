import streamlit as st

st.set_page_config(
    page_title="Competitor Analysis",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Competitor Analysis App")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Overview")
    st.write(
        "This app lets you search for mobile apps on the Google Play Store "
        "and perform a competitor analysis based on the results. "
        "Data is retrieved live using the Google Play Scraper API."
    )

    st.subheader("Key Features")
    st.markdown("""
    - Search for apps by keyword
    - Browse and filter search results
    - Data visualizations for competitor analysis
    - Sentiment analysis on user reviews
    """)

with col2:
    st.subheader("How to Use")
    st.markdown("""
    1. Go to **Search & Results** — enter a search term to retrieve apps
    2. Go to **Visualizations** — explore charts based on the search results
    3. Go to **Sentiment Analysis** — analyze user reviews sentiment per app
    """)


    st.subheader("Improvements")
    st.markdown("""
    - Adding data from ProductHunt and GitHub
    - Richer visualizations (heatmaps, box plots)
    - LLM-based feature summaries
    - Exporting results to CSV
    """)