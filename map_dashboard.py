import socket
import json
import tkinter as tk
import threading
import random
from PIL import Image, ImageTk

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

# ---------------- LOAD IMAGE SAFELY ----------------
try:
    base_img = Image.open("Assets/car.png").resize((40, 20))
except Exception as e:
    print("⚠️ Image error:", e)
    base_img = Image.new("RGB", (40, 20), "blue")  # fallback

# Rotations for directions
car_images = {
    "H": ImageTk.PhotoImage(base_img),
    "V": ImageTk.PhotoImage(base_img.rotate(90, expand=True))
}

# Keep references (IMPORTANT)
image_refs = []

signal_state = "GREEN"
timer = 0

# ---------------- DRAW MAP ----------------
def draw_map():
    canvas.create_rectangle(0, 180, 750, 260, fill="gray")
    canvas.create_rectangle(320, 0, 420, 450, fill="gray")

    # lane lines
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
    global signal_state, timer, image_refs

    canvas.delete("all")
    image_refs = []  # reset references

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
            if not (signal_state == "RED" and 300 < x < 380):
                x += speed
                if 320 < x < 400 and turn != "STRAIGHT":
                    v["dir"] = "V"

        else:  # Vertical
            if not (signal_state == "RED" and 180 < y < 260):
                y += speed
                if 180 < y < 260 and turn != "STRAIGHT":
                    v["dir"] = "H"

        # LOOP BACK
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

        # ---------------- DRAW CAR ----------------
        img = car_images.get(v["dir"], car_images["H"])
        Image.open("assets/car.png").resize((40, 20))
        image_refs.append(img)  # prevent garbage collection

        canvas.create_rectangle(x-10, y-5, x+10, y+5, fill="blue")
        canvas.create_text(x, y-12, text=vid, fill="white")

    root.after(800, update)

# ---------------- RUN ----------------
update()
root.mainloop()