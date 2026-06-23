import streamlit as st
from utils import search_apps

st.set_page_config(page_title="Search & Results", page_icon="🔍", layout="wide")

st.title("🔍 Search & Results")
st.write("Search for apps on the Google Play Store and browse the results.")
st.divider()

# search input
query = st.text_input("Enter a search term:", placeholder="e.g. mental health AI")
n_hits = st.slider("Number of results:", min_value=5, max_value=50, value=20)

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a search term.")
    else:
        with st.spinner(f"Searching for '{query}'..."):
            try:
                df = search_apps(query, n_hits=n_hits)
                st.session_state["results_df"] = df
                st.session_state["query"] = query
                st.success(f"Found {len(df)} apps for '{query}'")
            except Exception as e:
                st.error(f"Search failed: {e}")

# display results if they exist in session state
if "results_df" in st.session_state:
    df = st.session_state["results_df"]

    st.subheader(f"Results for: *{st.session_state['query']}*")

    # sidebar filters
    st.sidebar.title("Filters")
    free_filter = st.sidebar.radio("App type:", ["All", "Free", "Paid"])
    min_rating = st.sidebar.slider("Minimum rating:", 0.0, 5.0, 0.0, step=0.1)
    genre_options = ["All"] + sorted(df["genre"].dropna().unique().tolist())
    genre_filter = st.sidebar.selectbox("Genre:", genre_options)

    filtered = df.copy()
    if free_filter == "Free":
        filtered = filtered[filtered["free"] == True]
    elif free_filter == "Paid":
        filtered = filtered[filtered["free"] == False]
    if min_rating > 0:
        filtered = filtered[filtered["score"] >= min_rating]
    if genre_filter != "All":
        filtered = filtered[filtered["genre"] == genre_filter]

    st.dataframe(
        filtered,
        use_container_width=True,
        column_config={
            "score":    st.column_config.ProgressColumn("Rating", min_value=0, max_value=5),
            "url":      st.column_config.LinkColumn("Store Link"),
            "free":     st.column_config.CheckboxColumn("Free"),
        },
    )

    st.caption(f"Showing {len(filtered)} of {len(df)} results — go to Visualizations to explore the data.")