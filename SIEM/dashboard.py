# Build SIEM to interact with backend (app.py)
# Create real-time log from suricata
# Streamlit for UI
# Streamlit Autorefresh to refresh every 10 seconds
# Visualized by charts
import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import plotly.express as px

# Page Title "SIEM Dashboard"
# Title ""
st.set_page_config(page_title="🔐 SIEM Dashboard", layout="wide")
st.title("🚨 Cyber Threat Detection & Live SIEM Monitor")

# Refresh
st_autorefresh(interval=10000, key="refresh")

# Upload file Header
st.header("📂 Upload Network Log for Threat Detection")
# Browse csv file
# Send to backend (app.py): http://127.0.0.1:5000/detect
# If status == 200, response => convert JSON on dashboard
# Download the result for the uploaded
# Show IP to block
# Download IP to Block
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file is not None:
    st.success("📄 File uploaded! Running detection...")
    # During uploading the file
    with st.spinner("🔍 Detecting..."):
        try:
            response = requests.post(
                "http://127.0.0.1:5000/detect",
                files={"file": uploaded_file}
            )

            if response.status_code == 200:
                alerts = response.json()
                if alerts:
                    df_alerts = pd.DataFrame(alerts)
                    # Show subheader for the uploaded file
                    st.subheader(f"✅ Detected {len(df_alerts)} Threat(s)")
                    st.dataframe(df_alerts)

                    st.download_button("⬇ Download Detected Threats", df_alerts.to_csv(index=False), file_name="detected_alerts.csv")

                    blocked_ips = df_alerts["src_ip"].dropna().unique()
                    if len(blocked_ips) > 0:
                        st.subheader("⛔ IPs to Block (Detection)")
                        st.code("\n".join(blocked_ips))
                        ip_df = pd.DataFrame(blocked_ips, columns=["Blocked IP"])
                        st.download_button("⬇ Download IP Blocklist", ip_df.to_csv(index=False), file_name="ip_blocklist_detect.csv")

                else:
                    st.success("✅ No threats detected.")
            else:
                st.error(f"❌ Detection failed: {response.json().get('error', 'Unknown error')}")

        except Exception as e:
            st.error(f"❌ Error: {e}")

# Separate Uploading and Real Time
st.divider()

# Real-time from log
# Read from Alerts.log file 
st.header("📡 Real-Time SIEM Feed (Suricata & Stream)")

log_path = "alerts.log"
if os.path.exists(log_path):
    try:
        with open(log_path, "r") as f:
            lines = f.readlines()

        alerts = []
        for line in lines:
            try:
                # Split Timestamp
                # Prediction, source IP, and Destination IP
                ts, msg = line.split("] ALERT - ")
                ts = ts.strip("[")
                pred, rest = msg.split(" from ")
                src, dst = rest.split(" to ")
                alerts.append({
                    "Timestamp": ts,
                    "Threat Type": pred.strip(),
                    "Source IP": src.strip(),
                    "Destination IP": dst.strip()
                })
            except:
                continue
        # Convert Alerts into DataFrame
        # Subheader for the alerts
        df_log = pd.DataFrame(alerts)
        st.subheader(f"📈 Real-Time Threats: {len(df_log)} alerts")
        st.dataframe(df_log)
        # If log is not empty
        # Count the amount of threat type 
        if not df_log.empty:
            threat_counts = df_log["Threat Type"].value_counts().reset_index()
            threat_counts.columns = ["Threat Type", "Count"]

            # Show bar charts and pie charts
            col1, col2 = st.columns(2)
            with col1:
                fig_bar = px.bar(threat_counts, x="Threat Type", y="Count", color="Threat Type", title="📊 Real-Time Threat Count")
                st.plotly_chart(fig_bar, use_container_width=True)

            with col2:
                fig_pie = px.pie(threat_counts, names="Threat Type", values="Count", title="📌 Real-Time Threat Distribution")
                st.plotly_chart(fig_pie, use_container_width=True)

            # Download real-time alerts
            st.download_button("⬇ Download Real-Time Alerts", df_log.to_csv(index=False), file_name="realtime_alerts.csv")

            # Real-time IP Blocklist
            live_blocked_ips = df_log["Source IP"].dropna().unique()
            if len(live_blocked_ips) > 0:
                st.subheader("🚫 IPs to Block (Real-Time)")
                st.code("\n".join(live_blocked_ips))
                ip_df = pd.DataFrame(live_blocked_ips, columns=["Blocked IP"])
                st.download_button("⬇ Download Real-Time IP Blocklist", ip_df.to_csv(index=False), file_name="ip_blocklist_realtime.csv")

    except Exception as e:
        st.error(f"❌ Failed to load alerts.log: {e}")
else:
    st.warning("📭 Waiting for alerts.log to be generated...")
