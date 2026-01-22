
import streamlit as st
import pandas as pd
import folium
import requests
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from streamlit.components.v1 import html

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Tamil Nadu Flood Alert System", layout="wide")

st.title("🌊 Tamil Nadu Flood Alert System")
st.markdown("Green AI based flood awareness using location, dams, and rainfall data")

# ------------------ USER INPUT ------------------
place = st.text_input("📍 Enter a place in Tamil Nadu")

# ------------------ DATA UPLOAD ------------------
uploaded_file = st.file_uploader(
    "Upload Tamil Nadu Water Resources CSV",
    type="csv"
)

# ------------------ API KEY ------------------
API_KEY = "d8f4890b961a82c525d6e63685d4f9ef"  # replace if needed

# ------------------ MAIN LOGIC ------------------
if place and uploaded_file:

    # Load dataset
    data = pd.read_csv(uploaded_file)

    geolocator = Nominatim(user_agent="tn_flood_app")
    location = geolocator.geocode(place + ", Tamil Nadu, India")

    if not location:
        st.error("Place not found. Try another location.")
        st.stop()

    user_coords = (location.latitude, location.longitude)

    st.success(f"📍 Location found: {place}")
    st.write("Coordinates:", user_coords)

    # ------------------ NEAREST DAMS ------------------
    data['Distance_km'] = data.apply(
        lambda row: great_circle(
            user_coords, (row['Latitude'], row['Longitude'])
        ).km if pd.notnull(row['Latitude']) else None,
        axis=1
    )

    nearest = data.nsmallest(3, 'Distance_km')

    st.subheader("🏞️ Nearest Water Bodies")
    st.dataframe(nearest[['Name', 'River', 'District', 'Distance_km']])

    # ------------------ MAP ------------------
    m = folium.Map(location=user_coords, zoom_start=8)
    folium.Marker(
        user_coords,
        tooltip="User Location",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    for _, row in nearest.iterrows():
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            tooltip=f"{row['Name']} ({row['River']}) - {row['Distance_km']:.2f} km",
            icon=folium.Icon(color="red")
        ).add_to(m)

    st.subheader("🗺️ Flood Awareness Map")
    html(m._repr_html_(), height=600)

    # ------------------ RAINFALL DATA ------------------
    lat, lon = user_coords

    url_now = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    now = requests.get(url_now).json()
    rain_now = now.get('rain', {}).get('1h', 0)

    url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    forecast = requests.get(url_forecast).json()

    rain_data = []
    for entry in forecast['list']:
        rain = entry.get('rain', {}).get('3h', 0)
        rain_data.append(rain)

    total_rain = sum(rain_data)

    # ------------------ RISK LOGIC ------------------
    if total_rain < 35:
        risk = "Low Risk"
        alert = "Light rain expected. No flood risk."
        color = "green"
    elif total_rain < 65:
        risk = "Medium Risk"
        alert = "Moderate rain expected. Stay alert."
        color = "orange"
    else:
        risk = "High Risk"
        alert = "Extreme rainfall! Flooding likely."
        color = "red"

    # ------------------ DISPLAY RESULTS ------------------
    st.subheader("🌧️ Rainfall Analysis")
    col1, col2, col3 = st.columns(3)

    col1.metric("Current Rain (1 hr)", f"{rain_now} mm")
    col2.metric("5-Day Forecast Rain", f"{total_rain:.2f} mm")
    col3.metric("Flood Risk", risk)

    st.markdown(f"### 🛑 Alert: <span style='color:{color}'>{alert}</span>", unsafe_allow_html=True)

    # ------------------ RAINFALL GRAPH ------------------
    st.subheader("📊 Rainfall Forecast Trend")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(rain_data, marker='o')
    ax.set_title("Rainfall Forecast (Next 5 Days)")
    ax.set_xlabel("Time Interval")
    ax.set_ylabel("Rainfall (mm)")
    ax.grid(True)

    st.pyplot(fig)

else:
    st.info("Enter place and upload dataset to continue.")


