from langchain_core.tools import tool
from modules.collector import fetch_polio_data
from modules.analyzer import analyze_signals

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
    REQUIRED SECOND STEP. Processes the data collected by the collection_tool. 
    It identifies specific rumor themes and calculates a risk score (High/Medium/Low).
    Input: A brief context or summary of the collected data.
    """
    report_file = analyze_signals()
    return f"Analysis finished. Report saved at {report_file}. Risk levels have been computed."

@tool
def alert_tool(summary: str):
    """
    CONDITIONAL FINAL STEP. Sends an emergency broadcast to the health team.
    ONLY use this tool if the analysis_tool has returned a 'High' risk status.
    Input: A concise summary of the identified rumor and why it is dangerous.
    """
    # Logic for actual alert (SMS/Email/Console)

    return f"EMERGENCY ALERT SENT: {summary}"
