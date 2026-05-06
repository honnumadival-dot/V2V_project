import time
import threading
from config import VEHICLE_ID
from modules import communication as comm
from modules import decision
from modules import logging_system
from modules import ai_module
from gui.dashboard import Dashboard

print(f"🚗 Vehicle {VEHICLE_ID} STARTED")

other_vehicles = {}
distance_history = {}

dashboard = Dashboard()

# ---------------- SEND ----------------
def sender():
    distance = 100
    speed = 30

    while True:
        data = {
            "id": VEHICLE_ID,
            "distance": distance,
            "speed": speed
        }

        comm.send(data)
        print(f"[TX] {data}")

        distance -= 1
        time.sleep(1)

# ---------------- RECEIVE ----------------
def receiver():
    while True:
        msg = comm.receive()

        if msg and msg["id"] != VEHICLE_ID:
            vid = msg["id"]
            other_vehicles[vid] = msg

            # store history
            if vid not in distance_history:
                distance_history[vid] = []

            distance_history[vid].append(msg["distance"])
            if len(distance_history[vid]) > 5:
                distance_history[vid].pop(0)

            print(f"[RX] {msg}")

        time.sleep(0.1)

# ---------------- COLLISION + AI ----------------
def system():
    my_speed = 30

    while True:
        for vid, data in other_vehicles.items():

            distance = data["distance"]
            other_speed = data["speed"]

            ttc = decision.calculate_ttc(distance, my_speed, other_speed)
            risk = decision.risk_level(distance, ttc)

            ai_status = ai_module.predict_risk(distance_history.get(vid, []))

            msg = f"Vehicle {vid} | Dist={distance} | TTC={round(ttc,2)} | Risk={risk} | AI={ai_status}"

            if risk == "CRITICAL":
                print(f"🚨 {msg}")
            elif risk == "WARNING":
                print(f"⚠️ {msg}")
            else:
                print(f"✅ {msg}")

            logging_system.log_event(msg)

            # update GUI
            dashboard.update_vehicle(vid, distance, risk)

        dashboard.run()
        time.sleep(0.5)

# ---------------- THREADS ----------------
threading.Thread(target=sender, daemon=True).start()
threading.Thread(target=receiver, daemon=True).start()
threading.Thread(target=system, daemon=True).start()

while True:
    pass