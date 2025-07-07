# modules/port_watcher.py

import streamlit as st
import socket
import os
from datetime import datetime

LOG_FILE = "logs/port_alerts.txt"

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP"
}

def is_port_open(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            return result == 0
    except Exception:
        return False

def scan_ports(ip):
    open_ports = []
    for port, service in COMMON_PORTS.items():
        if is_port_open(ip, port):
            open_ports.append((port, service))
    return open_ports

def log_scan(ip, open_ports):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"\n[{datetime.now()}] Scan for {ip}:\n")
        for port, service in open_ports:
            f.write(f" - {port} ({service}) open\n")
        if len(open_ports) > 5:
            f.write("!!! Suspicious: More than 5 common ports open!\n")

def run():
    st.subheader("🕵️ Port Watcher – Service Exposure Detector")

    ip = st.text_input("Enter IP or Domain", value="127.0.0.1")

    if st.button("Scan Ports"):
        with st.spinner("Scanning common ports..."):
            open_ports = scan_ports(ip)

        if open_ports:
            st.success(f"✅ {len(open_ports)} open port(s) found:")
            for port, service in open_ports:
                st.write(f"🔓 Port {port} ({service}) is open")
        else:
            st.info("✅ No open common ports detected.")

        log_scan(ip, open_ports)

        if len(open_ports) > 5:
            st.warning("⚠️ Too many ports are open — this might be a security risk.")
            st.info("Details logged in logs/port_alerts.txt")

    if os.path.exists(LOG_FILE):
        st.markdown("---")
        st.subheader("📝 Scan Logs")
        with open(LOG_FILE, "r") as f:
            st.text(f.read())
