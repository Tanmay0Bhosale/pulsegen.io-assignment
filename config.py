import os
from dotenv import load_dotenv

load_dotenv()

# App settings
APP_ID = "in.swiggy.android"  # Swiggy
START_DATE = "2024-06-01"

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Similarity threshold for deduplication
SIMILARITY_THRESHOLD = 0.85

# Seed topics
SEED_TOPICS = [
    "Delivery issue",
    "Food stale",
    "Delivery partner rude",
    "Maps not working properly",
    "Instamart should be open all night",
    "Bring back 10 minute bolt delivery",
    "App crashes",
    "Payment failed",
    "Refund not received",
    "Customer support unhelpful"
]
