import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. SECURE ENVIRONMENT SETUP ---
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

from main import agent_executor

# Page Config
st.set_page_config(page_title="Kenya PRIS | Mission Control", layout="wide", page_icon="🛡️")

# --- 2. CUSTOM UI STYLING ---
st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 12px; border: 1px solid #e9ecef; }
    .mission-box { background-color: #f0f2f6; padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Polio Rumor Intelligence System (PRIS)")
st.markdown("### 2026 Phase 4: Autonomous Monitoring Dashboard")

# --- 3. SIDEBAR: MISSION CONTROL ---
st.sidebar.header("🕹️ Agent Mission Control")

# High-Value Default Prompt for the Demo
default_mission = (
    "Scan for digital signals regarding polio vaccine safety in Marsabit, Garissa, and Turkana. "
    "Identify rumors about 'multiple doses' or 'foreign trials'. "
    "Categorize risk and suggest a fact-check response."
)

mission_input = st.sidebar.text_area(
    "🛰️ Define Agent Mission:",
    value=default_mission,
    height=200,
    help="Direct the Gemini 2.5 Agent to specific regions or rumor types."
)

if st.sidebar.button("🚀 Execute Strategic Mission"):
    try:
        with st.status("📡 Sentinel Agent Active...", expanded=True) as status:
            st.write("🔍 **Scanning:** News, Social Media, and Community Channels...")
            
            # Execute the custom mission from the text area
            response = agent_executor.invoke({"input": mission_input})
            
            st.write("🧠 **Reasoning complete.** Updating Intelligence Logs...")
            # Optional: Display the actual AI response in the status for transparency
            st.write(response["output"])
            
            status.update(label="Mission Accomplished!", state="complete", expanded=False)
        
        st.sidebar.success("Intelligence Report Generated!")
        st.toast("New signals detected and analyzed.")
        st.rerun() 
    except Exception as e:
        st.sidebar.error(f"Agent Connection Error: {e}")

st.sidebar.divider()
st.sidebar.info("System Health: **Optimal** (Gemini 2.5 Flash)")

# --- 4. DATA ARCHITECTURE CHECK ---
if not os.path.exists("data"):
    os.makedirs("data")
    df_empty = pd.DataFrame(columns=['source', 'risk_level', 'collected_at', 'summary', 'location'])
    df_empty.to_csv("data/analyzed_signals.csv", index=False)

DATA_PATH = "data/analyzed_signals.csv"

# --- 5. DASHBOARD VISUALS ---
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    
    # METRICS ROW
    total_rumors = len(df)
    avg_risk = df['risk_level'].value_counts() if 'risk_level' in df.columns else {}
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Signals Logged", total_rumors)
    with m2:
        high_risk_count = avg_risk.get('High', 0)
        st.metric("High Risk Priority", high_risk_count, delta="Immediate Action Required", delta_color="inverse")
    with m3:
        latest = df['collected_at'].iloc[-1] if not df.empty else "No Data"
        st.metric("Last Intelligence Sync", str(latest)[:16])

    # HUMAN-IN-THE-LOOP SECTION
    if high_risk_count > 0:
        st.error("### ⚠️ URGENT: High-Risk Rumors Detected in Priority Counties")
        high_risk_df = df[df['risk_level'] == 'High']
        st.table(high_risk_df[['source', 'collected_at', 'summary']])
        
        btn_col1, btn_col2 = st.columns(2)
        if btn_col1.button("✅ Dispatch Response Teams"):
            st.balloons()
            st.success("MOH Quick Response Teams (QRT) alerted via SMS Gateway.")
        if btn_col2.button("❌ Mark as Controlled"):
            st.info("Signal moved to 'Monitored' archive.")

    st.divider()

    # CHARTS
    c_left, c_right = st.columns(2)
    with c_left:
        st.subheader("📊 Risk Profile")
        fig = px.pie(df, names='risk_level', hole=0.5, 
                     color_discrete_map={'High':'#FF4B4B', 'Medium':'#FFAA00', 'Low':'#00CC96'})
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        st.subheader("📡 Channel Distribution")
        if 'source' in df.columns:
            source_counts = df['source'].value_counts().reset_index()
            fig2 = px.bar(source_counts, x='source', y='count', color='source', template="plotly_white")
            st.plotly_chart(fig2, use_container_width=True)

    # DATA EXPLORER
    st.subheader("🔍 Deep Dive: Intelligence Logs")
    st.dataframe(df.sort_values(by='collected_at', ascending=False), use_container_width=True)

else:
    st.warning("Awaiting system initialization...")
