import socket
import json
import tkinter as tk
import threading
import random

HOST = '127.0.0.1'
PORT = 5000

vehicles = {}

# ---------------- SOCKET ----------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("📡 Map dashboard connected")

# ---------------- COLLISION ----------------
def smart_collision(v1, v2):
    if v2["distance"] < 20:
        return "CRITICAL"
    elif v2["distance"] < 50:
        return "WARNING"
    else:
        return "SAFE"

# ---------------- RECEIVE ----------------
def receive():
    while True:
        try:
            data = json.loads(client.recv(1024).decode())

            # Add position if new
            if data["vehicle"] not in vehicles:
                vehicles[data["vehicle"]] = {
                    "x": random.randint(50, 550),
                    "y": random.randint(50, 350),
                    "data": data
                }
            else:
                vehicles[data["vehicle"]]["data"] = data

        except:
            break

threading.Thread(target=receive, daemon=True).start()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🚗 V2V Map Simulation")
root.geometry("700x500")

canvas = tk.Canvas(root, width=650, height=400, bg="lightgray")
canvas.pack()

alert_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
alert_label.pack()

# ---------------- UPDATE ----------------
def update():
    canvas.delete("all")

    critical = False

    for vid, info in vehicles.items():
        x = info["x"]
        y = info["y"]

        # Random movement
        x += random.randint(-10, 10)
        y += random.randint(-10, 10)

        # Keep inside bounds
        x = max(20, min(630, x))
        y = max(20, min(380, y))

        vehicles[vid]["x"] = x
        vehicles[vid]["y"] = y

        data = info["data"]

        # Calculate risk
        risk = "SAFE"
        for other_id, other_info in vehicles.items():
            if vid != other_id:
                r = smart_collision(data, other_info["data"])
                if r == "CRITICAL":
                    risk = "CRITICAL"
                    critical = True
                    break
                elif r == "WARNING":
                    risk = "WARNING"

        # Color based on risk
        color = "green"
        if risk == "CRITICAL":
            color = "red"
        elif risk == "WARNING":
            color = "orange"

        # Draw vehicle
        canvas.create_oval(x-10, y-10, x+10, y+10, fill=color)

        # Label
        canvas.create_text(x, y-15, text=vid)

    # Alert
    if critical:
        alert_label.config(text="🚨 COLLISION ALERT!", fg="red")
    else:
        alert_label.config(text="All vehicles safe", fg="green")

    root.after(1000, update)

update()
root.mainloop()