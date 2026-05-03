import socket
import json
import threading
import tkinter as tk
import random
import math
import time
import joblib

HOST = "127.0.0.1"
PORT = 5000

vehicle_id = f"V{random.randint(100,999)}"

# ---------------- AI MODEL ----------------
try:
    model = joblib.load("collision_model.pkl")
except:
    model = None

# ---------------- SOCKET ----------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

nearby = {}

# ---------------- SEND DATA ----------------
def send_loop():
    while True:
        data = {
            "id": vehicle_id,
            "x": vehicle["x"],
            "y": vehicle["y"],
            "speed": vehicle["speed"]
        }
        try:
            client.send(json.dumps(data).encode())
        except:
            pass
        time.sleep(0.1)

# ---------------- RECEIVE DATA ----------------
def receive_loop():
    while True:
        try:
            data = json.loads(client.recv(1024).decode())
            nearby[data["id"]] = data
        except:
            break

threading.Thread(target=send_loop, daemon=True).start()
threading.Thread(target=receive_loop, daemon=True).start()

# ---------------- VEHICLE ----------------
vehicle = {
    "x": random.randint(100,700),
    "y": random.randint(100,400),
    "speed": random.uniform(2,5),
    "dir": random.choice(["RIGHT","LEFT","UP","DOWN"])
}

# ---------------- COLLISION ----------------
def predict(v1, v2):
    dist = math.sqrt((v1["x"]-v2["x"])**2 + (v1["y"]-v2["y"])**2)
    speed_diff = abs(v1["speed"]-v2["speed"])

    if model:
        pred = model.predict([[dist, speed_diff]])[0]
        return ["SAFE","WARNING","CRITICAL"][pred]

    if dist < 20:
        return "CRITICAL"
    elif dist < 50:
        return "WARNING"
    return "SAFE"

# ---------------- GUI ----------------
root = tk.Tk()
root.title(f"🚗 Vehicle {vehicle_id}")

canvas = tk.Canvas(root, width=800, height=500, bg="black")
canvas.pack()

alert_text = tk.StringVar()
tk.Label(root, textvariable=alert_text, fg="red").pack()

# ---------------- UPDATE ----------------
def update():
    canvas.delete("all")

    # MOVE SELF
    if vehicle["dir"]=="RIGHT": vehicle["x"]+=vehicle["speed"]
    if vehicle["dir"]=="LEFT": vehicle["x"]-=vehicle["speed"]
    if vehicle["dir"]=="UP": vehicle["y"]-=vehicle["speed"]
    if vehicle["dir"]=="DOWN": vehicle["y"]+=vehicle["speed"]

    # DRAW SELF
    canvas.create_rectangle(vehicle["x"]-10, vehicle["y"]-10,
                            vehicle["x"]+10, vehicle["y"]+10,
                            fill="cyan")

    danger = "SAFE"

    # DRAW NEARBY
    for vid, v in nearby.items():
        canvas.create_rectangle(v["x"]-8, v["y"]-8,
                                v["x"]+8, v["y"]+8,
                                fill="yellow")

        result = predict(vehicle, v)

        if result == "CRITICAL":
            danger = "CRITICAL ⚠️"
            canvas.create_line(vehicle["x"], vehicle["y"], v["x"], v["y"], fill="red")

        elif result == "WARNING" and danger != "CRITICAL ⚠️":
            danger = "WARNING"

    alert_text.set(f"Status: {danger}")

    root.after(100, update)

update()
root.mainloop()