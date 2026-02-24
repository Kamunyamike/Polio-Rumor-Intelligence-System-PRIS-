import sqlite3
from datetime import datetime

def init_db():
    """Creates the database and table if they don't exist."""
    conn = sqlite3.connect('data/polio_memory.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            sentiment_rate REAL,
            rumor_count INTEGER,
            top_topic TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_daily_summary(sentiment_rate, rumor_count, top_topic):
    """Stores the agent's findings for today."""
    conn = sqlite3.connect('data/polio_memory.db')
    cursor = conn.cursor()
    date_today = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute('''
        INSERT INTO daily_summaries (date, sentiment_rate, rumor_count, top_topic)
        VALUES (?, ?, ?, ?)
    ''', (date_today, sentiment_rate, rumor_count, top_topic))
    
    conn.commit()
    conn.close()
    print(f"💾 Memory Updated: Today's data saved to database.")

def get_yesterday_stats():
    """Fetches the previous entry to allow comparison."""
    conn = sqlite3.connect('data/polio_memory.db')
    cursor = conn.cursor()
    # Get the second to last entry (yesterday)
    cursor.execute('SELECT sentiment_rate, rumor_count FROM daily_summaries ORDER BY id DESC LIMIT 2')
    rows = cursor.fetchall()
    conn.close()
    
    if len(rows) > 1:
        return rows[1] # Return the older record
    return None