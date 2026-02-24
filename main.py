import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_classic.memory import ConversationBufferMemory
# Ensure your tools are in modules/agent_tools.py
from modules.agent_tools import collection_tool, analysis_tool, alert_tool

load_dotenv()

# 1. SETUP BRAIN
# Pull from .env for security
api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0,
    # 2026 'Thinking' configuration
    thinking_budget=1024,
    include_reasoning=True 
)

# 2. BUNDLE TOOLS
tools = [collection_tool, analysis_tool, alert_tool]

# 3. MEMORY SETUP
# This allows the agent to remember the 'Thought' chain across multiple steps
memory = ConversationBufferMemory(memory_key="chat_history")

# 4. PROMPT TEMPLATE (Updated to include {chat_history})
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

# 5. BUILD AGENT & EXECUTOR
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    memory=memory, # Memory is now plugged in
    handle_parsing_errors=True,
    max_iterations=10 # Prevents the agent from getting stuck
)

if __name__ == "__main__":
    print("🚀 2026 AGENT ONLINE (Phase 3: Finalized)")
    try:
        mission = "Investigate polio vaccine rumors in Kenya and alert if risk is high."
        agent_executor.invoke({"input": mission})
    except Exception as e:

        print(f"❌ Execution Error: {e}")
