import re
import pandas as pd

def clean_text(text):
    """Removes links, special characters, and extra spaces."""
    if not text: return ""
    text = re.sub(r'http\S+', '', text) # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove punctuation/emojis
    return text.lower().strip()

def detect_rumors(text):
    """Flags text if it contains specific 'high-risk' keywords."""
    risk_keywords = ['infertility', 'haram', 'paralysis', 'dangerous', 'fake', 'side effect']
    found = [word for word in risk_keywords if word in text.lower()]
    return ", ".join(found) if found else "None"

def analyze_signals(input_file="data/raw_signals.csv"):
    """Reads the collected data and applies NLP logic."""
    df = pd.read_csv(input_file)
    
    # 1. Clean the descriptions
    df['clean_description'] = df['description'].apply(clean_text)
    
    # 2. Detect Rumors
    df['rumor_tags'] = df['clean_description'].apply(detect_rumors)
    
    # 3. Basic Sentiment Logic (Pseudo-code for now)
    # If rumor_tags exist, we mark it as 'High Risk'
    df['risk_level'] = df['rumor_tags'].apply(lambda x: 'HIGH' if x != "None" else 'LOW')
    
    output_path = "data/analyzed_signals.csv"
    df.to_csv(output_path, index=False)
    return output_path