# modules/wifi_doctor.py

import streamlit as st
import subprocess
import platform
import socket
import json
import os
from datetime import datetime

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "4", host]
    try:
        output = subprocess.check_output(command, universal_newlines=True)
        return output
    except subprocess.CalledProcessError:
        return "Ping failed."

def dns_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        return f"{domain} resolved to {ip}"
    except Exception as e:
        return f"DNS resolution failed: {str(e)}"

def scan_local_network():
    st.info("Scanning network... may take a few seconds.")
    try:
        # Change this subnet according to your network (e.g., 192.168.0.0/24)
        result = subprocess.check_output(["nmap", "-sn", "255.255.255.0/24"], universal_newlines=True)
        devices = []
        lines = result.split("\n")
        current_device = {}
        for line in lines:
            if "Nmap scan report for" in line:
                ip = line.split("for")[1].strip()
                current_device = {"IP": ip}
            elif "MAC Address:" in line:
                mac = line.split("MAC Address:")[1].strip()
                current_device["MAC"] = mac
                devices.append(current_device)
        return devices
    except Exception as e:
        return f"Scan failed: {e}"

def save_device_logs(devices):
    os.makedirs("logs", exist_ok=True)
    with open("logs/device_logs.json", "w") as f:
        json.dump(devices, f, indent=4)

def run():
    st.subheader("📶 WiFi Doctor – Network Health Check")

    with st.expander("🔄 Ping Tests"):
        router_ip = st.text_input("Enter Router IP", "192.168.1.1")
        if st.button("Ping Router"):
            st.code(ping(router_ip))
        if st.button("Ping Google DNS (8.8.8.8)"):
            st.code(ping("8.8.8.8"))

    with st.expander("🌐 DNS Test"):
        domain = st.text_input("Enter Domain to Resolve", "nutanix.com")
        if st.button("Test DNS"):
            st.success(dns_lookup(domain))

    with st.expander("🖥️ Device Scanner"):
        if st.button("Scan Devices on Network"):
            devices = scan_local_network()
            if isinstance(devices, str):
                st.error(devices)
            else:
                st.success(f"{len(devices)} device(s) found.")
                st.table(devices)
                save_device_logs(devices)
