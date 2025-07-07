# modules/traceroute_geo.py

import streamlit as st
import subprocess
import platform
import re
import geoip2.database
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import os

DB_PATH = "assets/GeoLite2-City.mmdb"

def traceroute(domain):
    system = platform.system().lower()
    if system == "windows":
        command = ["tracert", "-d", domain]
    else:
        command = ["traceroute", "-n", domain]

    try:
        output = subprocess.check_output(command, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return str(e)

def extract_ips(traceroute_output):
    ip_pattern = r"(\d{1,3}(?:\.\d{1,3}){3})"
    return re.findall(ip_pattern, traceroute_output)

def geolocate_ips(ip_list):
    coords = []
    if not os.path.exists(DB_PATH):
        st.error("GeoLite2 database not found. Download and place in assets/ folder.")
        return coords

    with geoip2.database.Reader(DB_PATH) as reader:
        for ip in ip_list:
            try:
                response = reader.city(ip)
                lat = response.location.latitude
                lon = response.location.longitude
                city = response.city.name
                country = response.country.name
                coords.append({
                    "ip": ip,
                    "city": city or "Unknown",
                    "country": country or "Unknown",
                    "lat": lat,
                    "lon": lon
                })
            except:
                continue
    return coords

def plot_map(hops):
    if not hops:
        st.warning("No hops to plot.")
        return

    m = folium.Map(location=[20.0, 0.0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(m)

    for hop in hops:
        folium.Marker(
            location=[hop["lat"], hop["lon"]],
            popup=f"{hop['ip']} - {hop['city']}, {hop['country']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(marker_cluster)

    st_folium(m, width=700, height=500)

def run():
    st.subheader("🌍 Traceroute Geo Visualizer")

    domain = st.text_input("Enter domain to trace", value="google.com")

    if st.button("Run Traceroute"):
        with st.spinner(f"Tracing route to {domain}... please wait ⏳"):
            output = traceroute(domain)

        if output:
            st.success("✅ Traceroute completed!")
            st.text_area("Traceroute Output", output, height=250)

            ips = extract_ips(output)
            st.info(f"🔍 {len(ips)} hop(s) found.")

            hops = geolocate_ips(ips)
            if hops:
                st.success("📍 Mapping route...")
                plot_map(hops)
            else:
                st.warning("No geolocations found for the hops.")
        else:
            st.error("❌ Traceroute failed or returned no output.")
