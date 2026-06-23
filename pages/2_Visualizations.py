import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Visualizations", page_icon="📈", layout="wide")

st.title("📈 Visualizations")
st.divider()

# check session state
if "results_df" not in st.session_state:
    st.warning("No data found. Please run a search on the Results page first.")
    st.stop()

df = st.session_state["results_df"].copy()

# sidebar filter by app ID
st.sidebar.title("Filter")
all_ids = df["appId"].tolist()
selected_ids = st.sidebar.multiselect("Filter by App ID:", all_ids, default=all_ids)
df = df[df["appId"].isin(selected_ids)]

if df.empty:
    st.warning("No apps match the current filter.")
    st.stop()

# row 1 : ratings distribution + top apps by rating
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ratings Distribution")
    fig = px.histogram(df, x="score", nbins=10, labels={"score": "Rating"}, color_discrete_sequence=["#FF5E00"])
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top Apps by Rating")
    top = df.nlargest(10, "score")[["title", "score"]].sort_values("score")
    fig2 = px.bar(top, x="score", y="title", orientation="h", labels={"score": "Rating", "title": ""},
                  color="score", color_continuous_scale="Reds")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# row 2 : free vs paid + genre distribution 
col3, col4 = st.columns(2)

with col3:
    st.subheader("Free vs Paid Apps")
    type_counts = df["free"].map({True: "Free", False: "Paid"}).value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]
    fig3 = px.pie(type_counts, names="Type", values="Count", color_discrete_sequence=["#FF5E00", "#5E5C5C"])
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Genre Distribution")
    genre_counts = df["genre"].value_counts().reset_index()
    genre_counts.columns = ["Genre", "Count"]
    fig4 = px.bar(genre_counts, x="Genre", y="Count", color_discrete_sequence=["#FF5E00"])
    fig4.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# row 3 : top apps by installs + word cloud
col5, col6 = st.columns(2)

with col5:
    st.subheader("Top Apps by Installs")
    df_installs = df.dropna(subset=["installs"]).copy()
    # installs comes as a string like "10,000+" so we clean it
    df_installs["installs_clean"] = (
        df_installs["installs"]
        .astype(str)
        .str.replace(",", "")
        .str.replace("+", "")
        .str.extract(r"(\d+)")[0]
        .astype(float)
    )
    top_installs = df_installs.nlargest(10, "installs_clean")[["title", "installs_clean"]].sort_values("installs_clean")
    fig5 = px.bar(top_installs, x="installs_clean", y="title", orientation="h",
                  labels={"installs_clean": "Installs", "title": ""},
                  color="installs_clean", color_continuous_scale="Reds")
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("Word Cloud from Descriptions")
    if "summary" in df.columns:
        text = " ".join(df["summary"].dropna().tolist())
        if text.strip():
            wc = WordCloud(width=800, height=400, background_color="white", colormap="Reds").generate(text)
            fig6, ax = plt.subplots(figsize=(8, 4))
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig6)
        else:
            st.info("No description text available.")
    else:
        st.info("No summary column found.")