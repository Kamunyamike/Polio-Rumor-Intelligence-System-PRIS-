from langchain_core.tools import tool
from modules.collector import fetch_polio_data
from modules.analyzer import analyze_signals
import pandas as pd
import os

@tool
def collection_tool(query: str):
    """
    REQUIRED FIRST STEP. Searches for real-world signals and news regarding 
    polio vaccine rumors in a specific region. 
    Input: A search query (e.g., 'Kenya polio vaccine rumors').
    """
    data = fetch_polio_data(query)
    if data.empty:
        return "No signals found for this region."
    return f"Success. Collected {len(data)} signals. Sample: {data.head(2).to_dict()}"

@tool
def analysis_tool(context: str):
    """
    CRITICAL STEP: Processes collected signals with a Multi-stage Filter.
    1. FILTER: Discards any text NOT related to health/polio (e.g., politics, taxes).
    2. TRANSLATE: Converts any non-English signals into clear English.
    3. SCORE: Calculates risk (High/Medium/Low).
    Input: The raw summary or context from the collection_tool.
    """
    # The 'context' passed here now contains the raw search results.
    # We pass it to the analyzer, which now has a strict System Instruction:
    # "If text is irrelevant to Polio/Health, return 'SKIP'. If non-English, translate."
    
    report_file = analyze_signals(context) 
    
    return f"Intelligence scrubbed, translated, and analyzed. Results appended to {report_file}."

@tool
def alert_tool(summary: str):
    """
    CONDITIONAL FINAL STEP. Sends an emergency broadcast to the health team.
    ONLY use this tool if the analysis_tool has returned a 'High' risk status.
    Input: A concise summary of the identified rumor and why it is dangerous.
    """
    # Logic for actual alert (SMS/Email/Console)

    return f"EMERGENCY ALERT SENT: {summary}"

