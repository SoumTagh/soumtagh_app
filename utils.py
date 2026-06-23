import time
import pandas as pd
from google_play_scraper import search, app, reviews, Sort


def search_apps(query, n_hits=20):
    """Search Google Play for apps matching a query, returns a dataframe."""
    results = search(query, lang="en", country="us", n_hits=n_hits)
    app_ids_seen = set()
    unique_results = []
    for r in results:
        if r["appId"] not in app_ids_seen:
            app_ids_seen.add(r["appId"])
            unique_results.append(r)
    df = pd.DataFrame(unique_results)
    cols = ["title", "appId", "score", "ratings", "installs", "free", "genre", "developer", "summary", "url"]
    cols = [c for c in cols if c in df.columns]
    return df[cols]


def get_app_details(app_id):
    """Fetch full details for a single app by app ID."""
    details = app(app_id, lang="en", country="us")
    return details


def get_reviews(app_id, count=100):
    """Fetch user reviews for an app, returns a dataframe."""
    all_reviews = []
    seen_ids = set()

    for sort_mode in [Sort.MOST_RELEVANT, Sort.NEWEST, Sort.RATING]:
        try:
            result, _ = reviews(
                app_id,
                lang="en",
                country="us",
                sort=sort_mode,
                count=count,
            )
            for r in result:
                if r["reviewId"] not in seen_ids:
                    seen_ids.add(r["reviewId"])
                    all_reviews.append(r)
            time.sleep(0.5)
        except Exception as e:
            print(f"Review fetch failed ({sort_mode}): {e}")

    df = pd.DataFrame(all_reviews)
    if df.empty:
        return df
    cols = ["reviewId", "userName", "content", "score", "thumbsUpCount", "at"]
    cols = [c for c in cols if c in df.columns]
    return df[cols]