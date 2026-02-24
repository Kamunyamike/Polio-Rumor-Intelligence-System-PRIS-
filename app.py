import streamlit as st
import pandas as pd
import plotly.express as px
import os
from main import agent_executor 

# Page Config
st.set_page_config(page_title="Kenya Polio Rumor Tracker", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 10px; border-radius: 10px; border: 1px solid #e9ecef; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Polio Rumor Intelligence System (PRIS)")
st.markdown("### 2026 Phase 4: Autonomous Monitoring Dashboard")

# --- SIDEBAR & CONTROL PANEL ---
st.sidebar.header("🕹️ Agent Control Center")

# DIRECT MISSION TRIGGER (No requests/localhost needed)
if st.sidebar.button("🚀 Run Agent Mission Now"):
    try:
        with st.sidebar.status("Gemini 2.5 is investigating...", expanded=True) as status:
            st.write("🔍 Searching Kenyan news & social feeds...")
            
            # The exact mission we want the agent to execute
            mission = "Identify and analyze new polio vaccine rumors in Kenya. Focus on source credibility and risk level."
            
            # RUN THE AGENT DIRECTLY
            agent_executor.invoke({"input": mission})
            
            status.update(label="Mission Complete!", state="complete", expanded=False)
        
        st.toast("Intelligence report updated!")
        st.rerun() # Refresh the page to show the new CSV data
    except Exception as e:
        st.sidebar.error(f"Agent Error: {e}")

st.sidebar.divider()
st.sidebar.info("System Status: Online (Integrated Mode)")

# --- 1. LOAD DATA ---
DATA_PATH = "data/analyzed_signals.csv"

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    
    # --- 2. TOP LEVEL METRICS ---
    total_rumors = len(df)
    avg_risk = df['risk_level'].value_counts() if 'risk_level' in df.columns else {}
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Signals", total_rumors)
    with col2:
        high_risk_count = avg_risk.get('High', 0)
        st.metric("High Risk Detected", high_risk_count, delta=int(high_risk_count), delta_color="inverse")
    with col3:
        latest = df['collected_at'].iloc[-1] if 'collected_at' in df.columns else "N/A"
        # Convert timestamp to a cleaner format if it exists
        st.metric("Latest Scan", str(latest)[:16])

    # --- 3. HUMAN-IN-THE-LOOP (Approval Section) ---
    st.divider()
    if high_risk_count > 0:
        with st.expander("⚠️ ACTION REQUIRED: Review High Risk Rumors", expanded=True):
            high_risk_df = df[df['risk_level'] == 'High']
            st.write("The AI identifies these rumors as high-threat. Approve to trigger alerts:")
            st.table(high_risk_df[['source', 'collected_at', 'summary'] if 'summary' in df.columns else ['source', 'collected_at']])
            
            c1, c2 = st.columns(2)
            if c1.button("✅ Approve & Send Alert"):
                st.balloons()
                st.success("Alerts dispatched to Ministry of Health & WHO Kenya.")
            if c2.button("❌ Dismiss as False Positive"):
                st.warning("Risk cleared from dashboard.")

    # --- 4. VISUALIZATIONS ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Risk Distribution")
        if 'risk_level' in df.columns:
            fig = px.pie(df, names='risk_level', hole=0.4, 
                         color_discrete_map={'High':'#FF4B4B', 'Medium':'#FFAA00', 'Low':'#00CC96'})
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Source Breakdown")
        if 'source' in df.columns:
            source_counts = df['source'].value_counts().reset_index()
            fig2 = px.bar(source_counts, x='source', y='count', color='source')
            st.plotly_chart(fig2, use_container_width=True)

    # --- 5. DATA EXPLORER ---
    st.subheader("🔍 Deep Dive: Intelligence Logs")
    st.dataframe(df.sort_values(by='collected_at', ascending=False), use_container_width=True)

else:
    st.warning("⚠️ Awaiting Initial Data. Click 'Run Agent Mission Now' to start.")
