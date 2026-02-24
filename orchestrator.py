from apscheduler.schedulers.blocking import BlockingScheduler
from main import agent_executor # Import your Phase 3 Agent

scheduler = BlockingScheduler()

def autonomous_mission():
    print("🤖 LOG: Autonomous check starting...")
    mission = "Check for new polio vaccine rumors in Kenya. Analyze and alert only if critical."
    try:
        agent_executor.invoke({"input": mission})
        print("✅ LOG: Mission completed successfully.")
    except Exception as e:
        print(f"❌ LOG: Mission failed: {e}")

# Schedule: Run every 6 hours
scheduler.add_job(autonomous_mission, 'interval', hours=6)

if __name__ == "__main__":
    print("📡 PRIS Orchestrator Online. Monitoring every 6 hours...")
    # Run once immediately on startup
    autonomous_mission()
    scheduler.start()