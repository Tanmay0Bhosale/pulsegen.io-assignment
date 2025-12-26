import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import json
import time
from config import GEMINI_API_KEY, SEED_TOPICS, SIMILARITY_THRESHOLD

# Configure Gemini with correct API
genai.configure(api_key=GEMINI_API_KEY)

# Use the correct model name for the v1beta API
model = genai.GenerativeModel('models/gemini-2.5-flash')


# Embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_topic(review_text):
    """Extract topic using Gemini"""
    prompt = f"""Extract the main issue, request, or feedback from this review in 3-5 words:
    
Review: {review_text}

Return ONLY the topic label, nothing else. Examples:
- "Delivery issue"
- "Food stale"
- "App crashes"
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"API Error: {e}")
        # Fallback to simple keyword extraction
        text = review_text.lower()
        if 'delivery' in text and ('late' in text or 'delay' in text):
            return "Delivery issue"
        elif 'rude' in text or 'misbehave' in text:
            return "Delivery partner rude"
        elif 'crash' in text:
            return "App crashes"
        elif 'stale' in text or 'quality' in text:
            return "Food stale"
        elif 'payment' in text and 'fail' in text:
            return "Payment failed"
        else:
            return "General complaint"

def deduplicate_topic(new_topic, existing_topics):
    """Check if topic already exists using embeddings"""
    if not existing_topics:
        return new_topic
    
    new_emb = embedding_model.encode([new_topic])
    existing_embs = embedding_model.encode(existing_topics)
    
    similarities = cosine_similarity(new_emb, existing_embs)[0]
    max_sim_idx = similarities.argmax()
    
    if similarities[max_sim_idx] > SIMILARITY_THRESHOLD:
        return existing_topics[max_sim_idx]
    return new_topic

def analyze_reviews(reviews_df):
    """Main analysis function"""
    # Load existing topics
    try:
        with open("data/topics.json", "r") as f:
            topic_ontology = json.load(f)
    except:
        topic_ontology = SEED_TOPICS.copy()
    
    results = []
    
    print(f"Analyzing {len(reviews_df)} reviews...")
    
    # Detect date column name
    date_col = None
    for col in ['at', 'date', 'reviewCreatedTime', 'timestamp']:
        if col in reviews_df.columns:
            date_col = col
            break
    
    if date_col is None:
        print(f"Available columns: {reviews_df.columns.tolist()}")
        date_col = reviews_df.columns[2]  # Use 3rd column as date
    
    for idx, row in reviews_df.iterrows():
        try:
            # Extract topic
            topic = extract_topic(row['content'])
            
            # Deduplicate
            final_topic = deduplicate_topic(topic, topic_ontology)
            
            # Add new topic if needed
            if final_topic not in topic_ontology:
                topic_ontology.append(final_topic)
                print(f"New topic discovered: {final_topic}")
            
            results.append({
                'date': row[date_col],
                'review': row['content'],
                'topic': final_topic
            })
            
            if (idx + 1) % 5 == 0:
                print(f"Processed {idx + 1}/{len(reviews_df)} reviews...")
                time.sleep(0.5)  # Rate limiting
                
        except Exception as e:
            print(f"Error processing review {idx}: {e}")
            # Add to results anyway with default topic
            results.append({
                'date': row[date_col] if date_col else '2024-06-01',
                'review': row['content'],
                'topic': 'Unknown issue'
            })
            continue
    
    # Save updated topics
    with open("data/topics.json", "w") as f:
        json.dump(topic_ontology, f, indent=2)
    
    return pd.DataFrame(results)

def generate_trend_report(analyzed_df, target_date, window=31):
    """Generate T-30 to T trend table"""
    from datetime import timedelta
    
    # Handle empty dataframe
    if analyzed_df.empty:
        print("No data to generate report")
        return pd.DataFrame()
    
    # Create pivot table
    analyzed_df['date'] = pd.to_datetime(analyzed_df['date']).dt.date
    trend = analyzed_df.groupby(['date', 'topic']).size().unstack(fill_value=0)
    
    # Filter last 31 days
    end_date = pd.to_datetime(target_date).date()
    start_date = end_date - timedelta(days=window-1)
    trend = trend[(trend.index >= start_date) & (trend.index <= end_date)]
    
    # Transpose so topics are rows
    trend = trend.T
    
    return trend
