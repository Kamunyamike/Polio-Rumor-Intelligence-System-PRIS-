from fastapi import FastAPI, BackgroundTasks
from main import agent_executor
import pandas as pd
import os

app = FastAPI(title="PRIS API Gateway")

@app.get("/status")
def get_status():
    return {"status": "online", "agent": "Gemini 2.5 Flash"}

@app.post("/run-mission")
async def run_mission(background_tasks: BackgroundTasks):
    """Triggers the agent to run in the background so the UI doesn't freeze."""
    def execute_agent():
        mission = "Investigate polio vaccine rumors in Kenya and update analyzed_signals.csv."
        agent_executor.invoke({"input": mission})
    
    background_tasks.add_task(execute_agent)
    return {"message": "Mission started in background."}

@app.get("/latest-alerts")
def get_alerts():
    if os.path.exists("data/analyzed_signals.csv"):
        df = pd.read_csv("data/analyzed_signals.csv")
        return df.to_dict(orient="records")
    return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)