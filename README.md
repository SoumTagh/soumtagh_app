# Lab 2 – Data Applications with Streamlit

## Competitor Analysis App

I built a multi-page Streamlit app for competitor analysis of mobile apps on the Google Play Store.

### Project Structure
```
soumtagh_app/
├── Home.py
├── utils.py
├── pages/
│   ├── 1_Results_Table.py
│   └── 2_Visualizations.py
├── requirements.txt
└── .streamlit/
    └── config.toml
```

### Home.py
I created a homepage describing the project, its key features, how to use it, and possible future improvements.

### utils.py
I refactored the Google Play scraper code into reusable functions:
- search_apps(query, n_hits) — searches Google Play and returns a dataframe of results
- get_app_details(app_id) — fetches full details for a single app
- get_reviews(app_id, count) — fetches user reviews across three sort modes (Most Relevant, Newest, Rating) and deduplicates them

### Results Table (1_Results_Table.py)
I built a search interface where the user types a search term, chooses the number of results, and clicks Search. The app calls search_apps() live from the Google Play API and displays a filterable dataframe. Results are stored in st.session_state to be shared with other pages. The sidebar allows filtering by app type, minimum rating, and genre.

### Visualizations (2_Visualizations.py)
I read the search results from st.session_state and created 6 interactive Plotly visualizations:
- Ratings distribution histogram
- Top apps by rating (horizontal bar chart)
- Free vs Paid apps (pie chart)
- Genre distribution (bar chart)
- Top apps by installs (horizontal bar chart)
- Word cloud from app summaries

I added a sidebar filter to narrow down results by App ID.

## Sentiment Analysis (3_Sentiment_Analysis.py)

I added a third page to the app that runs sentiment analysis on user reviews using a pre-trained model from HuggingFace.

### Model Choice
I used cardiffnlp/twitter-roberta-base-sentiment, a RoBERTa-based model fine-tuned for sentiment classification into three categories: Positive, Neutral, and Negative. I chose this model because it is widely used for short, informal user-generated text, which matches the style of app reviews.

### Here is how it works :
1. It fetches 50 reviews per app using get_reviews() from utils.py
2. It runs each review through the HuggingFace pipeline (truncated to 512 characters to avoid token limit issues)
3. It computes a sentiment score per app as the percentage of positive reviews
4. It displays the results across three visualizations:
   - A horizontal bar chart showing the sentiment score per app
   - A pie chart breaking down positive/neutral/negative for a selected app
   - A filterable table of sample reviews with their sentiment label and confidence score

I used @st.cache_resource to load the model only once and avoid reloading it on every interaction.

### Requirements

```
streamlit==1.43.2
pandas==2.2.3
google-play-scraper==1.2.7
plotly==5.22.0
matplotlib==3.10.0
wordcloud==1.9.4
transformers==4.40.0
torch==2.3.0
```

## App deployement
Here is the link to the deployed version of the data application :

https://soumtaghapp-b7mug5z99rbbr8fdf6n8w9.streamlit.app/
