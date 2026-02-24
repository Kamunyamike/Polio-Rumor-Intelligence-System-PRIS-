import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests # Needed to talk to server.py

# Page Config
st.set_page_config(page_title="Kenya Polio Rumor Tracker", layout="wide")

# --- CUSTOM CSS FOR 2026 UI ---
st.markdown("""
    <style>
    .metric-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Polio Rumor Intelligence System (PRIS)")
st.markdown("### 2026 Phase 4: Autonomous Monitoring Dashboard")

# --- SIDEBAR & CONTROL PANEL ---
st.sidebar.header("🕹️ Agent Control Center")

# API Configuration
SERVER_URL = "http://localhost:8000"

if st.sidebar.button("🚀 Run Agent Mission Now"):
    try:
        response = requests.post(f"{SERVER_URL}/run-mission")
        if response.status_code == 200:
            st.sidebar.success("Mission started! Check back in a few seconds.")
            st.toast("Gemini 2.5 is investigating...")
        else:
            st.sidebar.error("Server is offline. Start server.py first.")
    except Exception as e:
        st.sidebar.error(f"Connection Error: {e}")

st.sidebar.divider()
st.sidebar.info("The agent runs automatically every 6 hours via the Orchestrator.")

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
        st.metric("Latest Check", str(latest)[:16])

    # --- 3. HUMAN-IN-THE-LOOP (Approval Section) ---
    st.divider()
    if high_risk_count > 0:
        with st.expander("⚠️ ACTION REQUIRED: Review High Risk Rumors"):
            high_risk_df = df[df['risk_level'] == 'High']
            st.write("The agent suggests sending an alert for the following:")
            st.table(high_risk_df[['source', 'collected_at']])
            
            c1, c2 = st.columns(2)
            if c1.button("✅ Approve & Send Alert"):
                st.success("Public Health teams notified!")
            if c2.button("❌ Dismiss as False Positive"):
                st.warning("Risk dismissed.")

    # --- 4. VISUALIZATIONS ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Risk Distribution")
        if 'risk_level' in df.columns:
            fig = px.pie(df, names='risk_level', hole=0.4, 
                         color_discrete_map={'High':'#FF4B4B', 'Medium':'#FFAA00', 'Low':'#00CC96'})
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Source Analysis")
        if 'source' in df.columns:
            source_counts = df['source'].value_counts().reset_index()
            fig2 = px.bar(source_counts, x='source', y='count', color='source')
            st.plotly_chart(fig2, use_container_width=True)

    # --- 5. DATA EXPLORER ---
    st.subheader("🔍 Deep Dive: Detected Signals")
    st.dataframe(df.sort_values(by='collected_at', ascending=False), use_container_width=True)

else:
    st.warning("⚠️ No data found. Please run your Agent mission to generate reports.")
    st.image("https://via.placeholder.com/800x200?text=System+Ready+-+Awaiting+Data", use_column_width=True)