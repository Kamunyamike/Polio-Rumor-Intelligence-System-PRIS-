import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_classic.memory import ConversationBufferMemory
from modules.agent_tools import collection_tool, analysis_tool, alert_tool

# --- 1. PRE-FLIGHT & SECURE KEYS ---
if not os.path.exists("data"):
    os.makedirs("data")

api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

# --- 2. THE INTELLIGENCE ENGINE (Gemini 2.5) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=api_key,
    temperature=0,  # Set to 0 for strict medical accuracy
    thinking_budget=2048 # High budget for translation and filtering logic
)

# --- 3. THE MISSION ARCHITECTURE ---
today = datetime.now().strftime("%Y-%m-%d")

template = f"""
You are the Lead Intelligence Officer for the Polio Rumor Intelligence System (PRIS). 
Today is {today}.

STRICT OPERATING PROTOCOLS:
1. RELEVANCE FILTER: You only care about Polio, Vaccines, and Public Health. 
   - REJECT: Politics, tax havens, colonial history, or general news.
   - If a search result is irrelevant, DO NOT pass it to the analysis_tool. 
   - Instead, refine your search or state "No relevant health signals found."

2. MULTILINGUAL PROCESSING: 
   - You are a universal translator. If you encounter news in Romanian, Swahili, or any other language, you MUST translate it into professional English before summarizing.

3. DYNAMIC INVESTIGATION:
   - Use the collection_tool to find signals.
   - Use the analysis_tool only for RELEVANT health data to save it.
   - Use the alert_tool only if the analyzed risk is 'High'.

Available Tools:
{{tools}}

Format:
Question: {{input}}
Thought: your reasoning (check for health relevance and language here)
Action: the action to take (one of [{{tool_names}}])
Action Input: input to the tool
Observation: result
... (repeat)
Final Answer: Summarize what you found and confirmed.

History:
{{chat_history}}

Begin!
Question: {{input}}
Thought:{{agent_scratchpad}}"""

prompt = PromptTemplate.from_template(template)

# --- 4. EXECUTION LAYER ---
tools = [collection_tool, analysis_tool, alert_tool]
memory = ConversationBufferMemory(memory_key="chat_history")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    memory=memory, 
    handle_parsing_errors=True,
    max_iterations=8 # Enough steps to search, filter, and translate
)

if __name__ == "__main__":
    print("🛰️ PRIS Sentinel Online...")
