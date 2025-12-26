from google_play_scraper import reviews, Sort
import pandas as pd
from datetime import datetime, timedelta
from config import APP_ID

def scrape_reviews(date_str):
    """Scrape reviews for a specific date"""
    result, _ = reviews(
        APP_ID,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=200
    )
    
    df = pd.DataFrame(result)
    df['date'] = pd.to_datetime(df['at']).dt.date
    df = df[df['date'] == pd.to_datetime(date_str).date()]
    
    return df[['reviewId', 'userName', 'at', 'content', 'score']]

if __name__ == "__main__":
    # Scrape and save
    reviews_df = scrape_reviews("2024-06-01")
    reviews_df.to_csv("data/reviews.csv", index=False)
    print(f"Scraped {len(reviews_df)} reviews")
