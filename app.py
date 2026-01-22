 
import streamlit as st

st.title("Tamil Nadu Flood Alert System")
place = st.text_input("📍Enter a place in Tamil Nadu", "")
if place:
    st.success(f"You entered: {place}")

!pip install folium geopy pandas requests gTTS
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import folium
import requests
from geopy.geocoders import Nominatim
import pandas as pd

data = pd.read_csv('/content/tamilnadu_water_resources_with_coords.csv')

user_location = input("Enter a place in Tamil Nadu: ")
geolocator = Nominatim(user_agent="geoapi")
location = geolocator.geocode(user_location + ", Tamil Nadu, India")
user_coords = (location.latitude, location.longitude)
print(f"
📍 User location coordinates: {user_coords}")


#nearest dam locator

# Re-load your DataFrame again
data = pd.read_csv('/content/tamilnadu_water_resources_with_coords.csv')

# Now safely apply
data['Distance_km'] = data.apply(
    lambda row: great_circle(user_coords, (row['Latitude'], row['Longitude'])).km if not pd.isnull(row['Latitude']) else None,
    axis=1
)


nearest = data.nsmallest(3, 'Distance_km')

print("
Nearest water bodies:")
print(nearest[['Name', 'River', 'District', 'Distance_km']])

#folium map visualizer

m = folium.Map(location=user_coords, zoom_start=8)
folium.Marker(user_coords, tooltip="User Location", icon=folium.Icon(color='blue')).add_to(m)

for _, row in nearest.iterrows():
    folium.Marker(
        [row['Latitude'], row['Longitude']],
        tooltip=f"{row['Name']} ({row['River']}) - {row['Distance_km']:.2f} km",
        icon=folium.Icon(color='red')
    ).add_to(m)

m



#Rainfall code


API_KEY = "d8f4890b961a82c525d6e63685d4f9ef"

place = user_location


geolocator = Nominatim(user_agent="rain_checker")
location = geolocator.geocode(place + ", Tamil Nadu, India")

if location:
    lat, lon = location.latitude, location.longitude
    print(f"📍 Coordinates of {place}: ({lat}, {lon})")

    # ---- Current Weather ----
    url_now = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    now = requests.get(url_now).json()
    rain_now = now.get('rain', {}).get('1h', 0)
    print(f"Current Rainfall in {place}: {rain_now} mm (last 1 hour)")

    # ---- 3-Hour Forecast (next 5 days) ----
    url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    forecast = requests.get(url_forecast).json()

    data = []
    for entry in forecast['list']:
        time = entry['dt_txt']
        rain = entry.get('rain', {}).get('3h', 0)
        data.append({'Time': time, 'Rainfall_mm': rain})

    df = pd.DataFrame(data)
    total_rain = df['Rainfall_mm'].sum()
    print(f"5-Day Total Forecast Rainfall: {total_rain:.2f} mm")
    #rain risk prediction
    if total_rain < 35:
      risk = "Low Risk"
    elif total_rain > 35 & total_rain < 65:
      risk = "Medium Risk"
    else:
      risk = "High Risk"
    print(risk)

    # ---- Plot Rainfall ----
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,4))
    plt.plot(df['Time'], df['Rainfall_mm'], color='blue', marker='o')
    plt.xticks(rotation=45)
    plt.title(f"Rainfall Forecast for {place} (next 5 days)")
    plt.xlabel("Date / Time")
    plt.ylabel("Rainfall (mm)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("Place not found.")



from gtts import gTTS
from IPython.display import Audio, display

def speak_alert_colab(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("alert.mp3")
    display(Audio("alert.mp3", autoplay=True))




if total_rain < 35:
  risk = "Low Risk"
  alert_text = "Light rain expected. No flood risk at the moment."
elif total_rain < 65:
  risk = "Medium Risk"
  alert_text = "Moderate to heavy rain expected. Please stay alert and avoid low-lying areas."
else:
  risk = "High Risk"
  alert_text = "Extreme rainfall alert! Flooding is very likely. Stay indoors and stay safe."
print(risk)
print("🔊", alert_text)
speak_alert_colab(alert_text)



