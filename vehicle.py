import socket
import json
import random
import time
import threading

HOST = '127.0.0.1'
PORT = 5000

vehicle_id = input("Enter Vehicle ID (A/B/C/...): ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print(f"🚗 Vehicle {vehicle_id} connected!")

# ---------------- SMART COLLISION ----------------
def smart_collision(my_data, other_data):
    speed_diff = abs(my_data["speed"] - other_data["speed"])

    if other_data["distance"] < 20 and speed_diff > 30:
        return "🚨 CRITICAL"
    elif other_data["distance"] < 50:
        return "⚠️ WARNING"
    else:
        return "✅ SAFE"

# ---------------- GLOBAL DATA ----------------
my_data = {}

# ---------------- RECEIVE THREAD ----------------
def receive():
    global my_data

    while True:
        try:
            received = json.loads(client.recv(1024).decode())

            # Ignore own message
            if received["vehicle"] == vehicle_id:
                continue

            # Calculate risk
            risk = smart_collision(my_data, received)

            print(f"\n📡 Received from {received['vehicle']}: {received}")
            print(f"🧠 Risk Level: {risk}")

        except:
            break

threading.Thread(target=receive, daemon=True).start()

# ---------------- SEND LOOP ----------------
while True:
    my_data = {
        "vehicle": vehicle_id,
        "distance": random.randint(5, 100),
        "speed": random.randint(20, 80)
    }

    client.send(json.dumps(my_data).encode())
    print(f"📤 Sent: {my_data}")

    time.sleep(2)