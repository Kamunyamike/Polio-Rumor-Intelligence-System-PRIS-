import streamlit as st
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_classic.memory import ConversationBufferMemory
from modules.agent_tools import collection_tool, analysis_tool, alert_tool

# --- 1. PRE-FLIGHT CHECKS ---
# Ensure data directory exists so tools don't crash when saving CSVs
if not os.path.exists("data"):
    os.makedirs("data")

# --- 2. SECURE KEY HYBRID LOAD ---
# This logic checks Streamlit Secrets first (Cloud), then .env (Local)
api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

# --- 3. SETUP BRAIN ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=api_key,
    temperature=0.1,
    # 2026 Feature: Gives the agent extra 'thinking space' for reasoning
    thinking_budget=1024 
)

# --- 4. BUNDLE TOOLS ---
tools = [collection_tool, analysis_tool, alert_tool]

# --- 5. MEMORY SETUP ---
memory = ConversationBufferMemory(memory_key="chat_history")

# --- 6. PROMPT TEMPLATE ---
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Previous conversation history:
{chat_history}

Begin!
Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# --- 7. BUILD AGENT & EXECUTOR ---
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    memory=memory, 
    handle_parsing_errors=True,
    max_iterations=10 
)

# --- 8. LOCAL TESTING LOGIC ---
if __name__ == "__main__":
    print("🚀 2026 AGENT ONLINE (Phase 3: Finalized)")
    try:
        # Note: In the Streamlit app, this is triggered by the sidebar button
        mission = "Investigate polio vaccine rumors in Kenya and alert if risk is high."
        agent_executor.invoke({"input": mission})
    except Exception as e:
        print(f"❌ Execution Error: {e}")
