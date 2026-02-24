import pandas as pd

def check_for_alerts(input_file="data/analyzed_signals.csv"):
    """
    Evaluates risk and triggers an alert if thresholds are met.
    """
    df = pd.read_csv(input_file)
    
    # Count how many 'HIGH' risk signals we found
    high_risk_count = len(df[df['risk_level'] == 'HIGH'])
    
    print(f"🕵️ Agent Evaluation: Found {high_risk_count} high-risk signals.")

    if high_risk_count >= 1:
        # In a real system, this would send an Email, SMS, or WhatsApp
        trigger_notification(high_risk_count, df[df['risk_level'] == 'HIGH'])
        return True
    
    return False

def trigger_notification(count, high_risk_df):
    """Simulates sending an alert."""
    print("\n" + "!"*30)
    print("🚨 RED ALERT: VACCINE RUMORS DETECTED 🚨")
    print(f"Total High-Risk Signals: {count}")
    print("Top Concerns Found:")
    for _, row in high_risk_df.head(3).iterrows():
        print(f"- {row['source']}: {row['rumor_tags']}")
    print("!"*30 + "\n")