def evaluate_risk_trend(today_rumors, yesterday_rumors, sentiment_rate):
    """
    The Decision Engine:
    Compares current data against historical memory to assign a Risk Level.
    """
    # Logic 1: Is the situation getting worse?
    trend_increasing = today_rumors > yesterday_rumors
    
    # Logic 2: Is the sentiment dangerously high? (Threshold > 40% as per guide)
    sentiment_critical = sentiment_rate > 40
    
    if trend_increasing and sentiment_critical:
        return "🔴 CRISIS: Rumors are spiking and sentiment is critical!"
    elif trend_increasing or sentiment_critical:
        return "🟡 WARNING: Potential escalation detected. Monitor closely."
    else:
        return "🟢 STABLE: No significant negative trends detected."

def generate_recommendation(risk_level):
    """Suggests an action based on the decision."""
    actions = {
        "🔴 CRISIS": "Immediate Action: Deploy community engagement teams and clarify misinformation via Radio/SMS.",
        "🟡 WARNING": "Action: Increase frequency of data collection and verify source of rumors.",
        "🟢 STABLE": "Action: Continue routine monitoring."
    }
    # Return the action based on the start of the risk_level string
    for key in actions:
        if key in risk_level:
            return actions[key]
    return "No action required."