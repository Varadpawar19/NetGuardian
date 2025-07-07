# modules/speed_monitor.py

import streamlit as st
import speedtest
import pandas as pd
import os
from datetime import datetime

LOG_FILE = "logs/speed_logs.csv"

# Run the internet speed test
def run_speed_test():
    try:
        stest = speedtest.Speedtest()
        stest.get_best_server()
        download = round(stest.download() / 1_000_000, 2)  # Mbps
        upload = round(stest.upload() / 1_000_000, 2)
        ping = round(stest.results.ping, 2)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = {
            "Time": timestamp,
            "Download (Mbps)": download,
            "Upload (Mbps)": upload,
            "Ping (ms)": ping
        }

        save_result(result)
        return result

    except Exception as e:
        st.error(f"Speed test failed: {e}")
        return None

# Save the result to CSV with header only if file doesn't exist
def save_result(result):
    os.makedirs("logs", exist_ok=True)
    df = pd.DataFrame([result])
    write_header = not os.path.exists(LOG_FILE)
    df.to_csv(LOG_FILE, mode='a', header=write_header, index=False)

# Load the log file safely
def load_logs():
    if os.path.exists(LOG_FILE):
        # This handles BOM and bad encoding
        df = pd.read_csv(LOG_FILE, encoding="utf-8-sig")
        df.columns = df.columns.str.strip()  # removes any whitespace
        return df
    else:
        return pd.DataFrame(columns=["Time", "Download (Mbps)", "Upload (Mbps)", "Ping (ms)"])


# Main Streamlit UI
def run():
    st.subheader("🚀 Internet Speed Monitor")

    if st.button("Run Speed Test"):
        with st.spinner(f"Running Speed Test... please wait ⏳"):
            result = run_speed_test()
        if result:
            st.success("✅ Test Completed")
            st.write(result)

    st.markdown("---")
    st.subheader("📊 Speed Test History")

    logs = load_logs()
    st.write("📋 Columns Detected:", logs.columns.tolist())

    if not logs.empty and "Time" in logs.columns:
        try:
            logs["Time"] = pd.to_datetime(logs["Time"])
            logs.set_index("Time", inplace=True)

            st.line_chart(logs[["Download (Mbps)", "Upload (Mbps)"]])
            st.bar_chart(logs[["Ping (ms)"]])
            st.dataframe(logs.tail(10), use_container_width=True)

        except Exception as e:
            st.error(f"Error while plotting: {e}")
    else:
        st.warning("⚠️ 'Time' column not found. Please delete the CSV or run a fresh test.")
