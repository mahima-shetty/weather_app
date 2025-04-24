import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_weather_data(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "models": "metno_seamless",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def plot_temperature_chart(times, temps):
    times_dt = [datetime.fromisoformat(t) for t in times[:24]]
    temps_24 = temps[:24]
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(times_dt, temps_24, marker='o', color='orange')
    ax.set_title("Hourly Temperature (Next 24 Hours)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(fig)

# --- Streamlit UI ---
st.set_page_config(page_title="Mumbai Weather Forecast", layout="centered")
st.title("🌤️ Mumbai Weather Forecast")

city = "Mumbai"
lat, lon = 19.0760, 72.8777

with st.spinner(f"Fetching latest weather data for {city}..."):
    data = fetch_weather_data(lat, lon)
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

st.subheader(f"Next 10 Hours Forecast for {city}")
for i in range(10):
    st.write(f"{times[i]} - 🌡️ {temps[i]}°C")

st.subheader("📊 Temperature Chart (24 Hours)")
plot_temperature_chart(times, temps)
