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

# ---------------- COLLISION ----------------
def smart_collision(v1, v2):
    if v2["distance"] < 20:
        return "CRITICAL"
    elif v2["distance"] < 50:
        return "WARNING"
    return "SAFE"

# ---------------- RECEIVE ----------------
def receive():
    while True:
        try:
            data = json.loads(client.recv(1024).decode())

            if data["vehicle"] not in vehicles:
                vehicles[data["vehicle"]] = {
                    "x": random.choice([100, 200, 400, 500]),
                    "y": random.choice([100, 200, 300]),
                    "dir": random.choice(["H", "V"]),
                    "lane": random.choice([0, 1]),
                    "speed": random.randint(5, 15),
                    "turn": random.choice(["STRAIGHT", "LEFT", "RIGHT"]),
                    "data": data
                }
            else:
                vehicles[data["vehicle"]]["data"] = data

        except:
            break

threading.Thread(target=receive, daemon=True).start()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🚗 Advanced Traffic Simulation")
root.geometry("800x500")

canvas = tk.Canvas(root, width=750, height=450, bg="green")
canvas.pack()

signal_state = "GREEN"
timer = 0

# ---------------- DRAW MAP ----------------
def draw_map():
    # Roads
    canvas.create_rectangle(0, 180, 750, 260, fill="gray")  # horizontal
    canvas.create_rectangle(320, 0, 420, 450, fill="gray")  # vertical

    # Lane lines
    for i in range(0, 750, 40):
        canvas.create_line(i, 220, i+20, 220, fill="white", width=2)
    for i in range(0, 450, 40):
        canvas.create_line(370, i, 370, i+20, fill="white", width=2)

# ---------------- SIGNAL ----------------
def draw_signal():
    color = "green" if signal_state == "GREEN" else "red"
    canvas.create_oval(360, 200, 380, 220, fill=color)

# ---------------- UPDATE ----------------
def update():
    global signal_state, timer

    canvas.delete("all")
    draw_map()
    draw_signal()

    timer += 1
    if timer % 6 == 0:
        signal_state = "RED" if signal_state == "GREEN" else "GREEN"

    for vid, v in vehicles.items():
        x, y = v["x"], v["y"]
        speed = v["speed"]
        direction = v["dir"]
        turn = v["turn"]

        # ---------------- MOVEMENT ----------------
        if direction == "H":
            if signal_state == "RED" and 300 < x < 380:
                pass
            else:
                x += speed

                # TURN LOGIC
                if 320 < x < 400:
                    if turn == "LEFT":
                        v["dir"] = "V"
                    elif turn == "RIGHT":
                        v["dir"] = "V"

        else:  # Vertical
            if signal_state == "RED" and 180 < y < 260:
                pass
            else:
                y += speed

                if 180 < y < 260:
                    if turn == "LEFT":
                        v["dir"] = "H"
                    elif turn == "RIGHT":
                        v["dir"] = "H"

        # LOOP
        if x > 750: x = 0
        if y > 450: y = 0

        v["x"], v["y"] = x, y

        # ---------------- COLLISION ----------------
        risk = "SAFE"
        for oid, other in vehicles.items():
            if vid != oid:
                r = smart_collision(v["data"], other["data"])
                if r == "CRITICAL":
                    risk = "CRITICAL"
                    break
                elif r == "WARNING":
                    risk = "WARNING"

        color = {"SAFE": "green", "WARNING": "orange", "CRITICAL": "red"}[risk]

        # ---------------- DRAW CAR ----------------
        canvas.create_rectangle(x-12, y-6, x+12, y+6, fill=color)
        canvas.create_text(x, y-12, text=f"{vid}", fill="white")

    root.after(800, update)

update()
root.mainloop()