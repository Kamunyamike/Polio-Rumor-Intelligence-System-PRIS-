import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def fetch_polio_data(query="polio vaccine Kenya"):
    """
    Tool: Fetches recent articles/posts based on a specific query.
    """
    # Replace 'YOUR_API_KEY' with your actual NewsAPI key in your .env file
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    articles = []
    if data.get("articles"):
        for art in data["articles"]:
            articles.append({
                "source": art["source"]["name"],
                "title": art["title"],
                "description": art["description"],
                "published_at": art["publishedAt"],
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    df = pd.DataFrame(articles)
    
    # Ensure data folder exists and save
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/raw_signals.csv", index=False)
    
    return df