import pandas as pd
from scraper import scrape_reviews
from analyzer import analyze_reviews, generate_trend_report
from datetime import datetime

def main(target_date):
    print(f"Processing reviews for {target_date}...")
    
    # Step 1: Scrape (or load existing data)
    reviews_df = pd.read_csv("data/reviews.csv")
    
    # Step 2: Analyze
    analyzed_df = analyze_reviews(reviews_df)
    
    # Step 3: Generate report
    report = generate_trend_report(analyzed_df, target_date)
    
    # Step 4: Save
    output_path = f"output/trend_report_{target_date}.csv"
    report.to_csv(output_path)
    
    print(f"Report saved to {output_path}")
    print(f"\nTop trending topics:")
    print(report.sum(axis=1).sort_values(ascending=False).head(10))

if __name__ == "__main__":
    main("2024-06-30")
