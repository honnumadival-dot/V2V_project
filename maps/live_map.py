import folium
import json
import time
import os

MAP_FILE = "maps/live_tracking.html"

DATA_FILE = "data/vehicles.json"

CENTER_LAT = 12.9716
CENTER_LON = 77.5946

def generate_map():

    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r") as file:

        vehicles = json.load(file)

    fmap = folium.Map(
        location=[CENTER_LAT, CENTER_LON],
        zoom_start=14
    )

    for vid, data in vehicles.items():

        lat = data["lat"]
        lon = data["lon"]

        speed = data["speed"]

        risk = data["risk"]

        color = "green"

        if risk == "WARNING":
            color = "orange"

        elif risk == "CRITICAL":
            color = "red"

        folium.Marker(
            [lat, lon],

            popup=f"""
Vehicle: {vid}<br>
Speed: {speed}<br>
Risk: {risk}
""",

            icon=folium.Icon(color=color)
        ).add_to(fmap)

    fmap.save(MAP_FILE)

    print("🗺️ Map Updated")

while True:

    generate_map()

    time.sleep(2)