import streamlit as st
from modules import wifi_doc, speed_mon, traceroute_geo, port_mon
from modules import traceroute_geo

st.set_page_config(page_title="NetGuardian Suite", layout="wide")

st.title("🛡️ NetGuardian - Real-Time Network Dashboard")
st.markdown("Your personal assistant for monitoring, debugging, and visualizing your network.")

# Sidebar for module selection
option = st.sidebar.radio(
    "Choose a Module",
    (
        "📶 WiFi Doctor",
        "🚀 Speed Monitor",
        "🌍 Traceroute Geo Map",
        "🕵️ Port Watcher"
    )
)

# Load modules dynamically
if option == "📶 WiFi Doctor":
    wifi_doc.run()

elif option == "🚀 Speed Monitor":
    speed_mon.run()

elif option == "🌍 Traceroute Geo Map":
    traceroute_geo.run()

elif option == "🕵️ Port Watcher":
    port_mon.run()

st.sidebar.markdown("---")
st.sidebar.markdown("🔧 Built with ❤️ by Varad")

