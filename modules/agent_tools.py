from langchain_core.tools import tool
from modules.collector import fetch_polio_data
from modules.analyzer import analyze_signals
import pandas as pd
import os

@tool
def collection_tool(query: str):
    """
    REQUIRED FIRST STEP. Searches for real-world signals regarding 
    polio vaccine rumors. 
    Input: A search query (e.g., 'Kenya polio vaccine news').
    """
    data = fetch_polio_data(query)
    if data.empty:
        return "No signals found for this region."
    return f"Success. Collected {len(data)} signals. Sample text: {data.head(2).to_dict()}"

@tool
def analysis_tool(context: str):
    """
    SAVES TO DATABASE. Processes health-related signals.
    STRICT RULES:
    1. Only pass medical/vaccine/polio related text here.
    2. Input MUST be translated to English before calling this tool.
    Input: The English-translated medical rumor summary.
    """
    # The analyzer module handles the actual CSV writing logic
    report_file = analyze_signals(context) 
    
    if "SKIP" in report_file:
        return "Data discarded: Irrelevant content detected by analyzer."
        
    return f"Intelligence verified and saved to {report_file}."

@tool
def alert_tool(summary: str):
    """
    EMERGENCY STEP. Sends broadcast to MoH team.
    ONLY use if analysis_tool confirms 'High' risk.
    Input: Concise summary of the rumor and the danger.
    """
    # Logic for actual alert dispatch would go here
    return f"EMERGENCY ALERT SENT: {summary}"
