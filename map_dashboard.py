import socket
import json
import tkinter as tk
import threading
import random
import os
import time
import requests
import joblib
from io import BytesIO
from collections import deque
from PIL import Image, ImageTk

# ---------------- OPTIONAL GRAPH ----------------
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_PLOT = True
except:
    HAS_PLOT = False

HOST = '127.0.0.1'
PORT = 5000

vehicles = {}

# ---------------- ML MODEL ----------------
try:
    model = joblib.load("model.pkl")
except:
    model = None

# ---------------- LANES ----------------
horizontal_lanes = [230, 270]
vertical_lanes = [400, 440]

# ---------------- MULTI INTERSECTION ----------------
intersections = [
    (350,200,450,300),
    (550,350,650,450)
]

# ---------------- MAP ----------------
def load_map():
    try:
        url = "https://tile.openstreetmap.org/15/18200/11800.png"
        r = requests.get(url, timeout=5)
        img = Image.open(BytesIO(r.content))
        return ImageTk.PhotoImage(img.resize((850,550)))
    except:
        return None

# ---------------- SOCKET ----------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except:
    print("Simulation mode")

def receive():
    while True:
        try:
            data = json.loads(client.recv(1024).decode())
            vid = data.get("vehicle", f"V{random.randint(100,999)}")

            if vid not in vehicles:
                direction = random.choice(["RIGHT","LEFT","UP","DOWN"])

                if direction in ["RIGHT","LEFT"]:
                    x = random.randint(0,800)
                    y = random.choice(horizontal_lanes)
                else:
                    x = random.choice(vertical_lanes)
                    y = random.randint(0,450)

                # 🧠 Behavior
                behavior = random.choice(["AGGRESSIVE","NORMAL","SAFE"])
                if behavior == "AGGRESSIVE":
                    base_speed = random.uniform(4,6)
                elif behavior == "SAFE":
                    base_speed = random.uniform(1,2)
                else:
                    base_speed = random.uniform(2,4)

                vehicles[vid] = {
                    "x": x,
                    "y": y,
                    "dir": direction,
                    "speed": base_speed,
                    "base_speed": base_speed,
                    "behavior": behavior,
                    "wait": 0,
                    "crashed": False,
                    "type": data.get("type","normal")
                }

        except:
            break

threading.Thread(target=receive, daemon=True).start()

# ---------------- COLLISION ----------------
def predict_collision(v1, v2):
    dist = ((v1["x"]-v2["x"])**2 + (v1["y"]-v2["y"])**2)**0.5

    if dist < 10:
        v1["crashed"] = True
        v2["crashed"] = True
        return "CRASH"

    if model:
        speed_diff = abs(v1["speed"]-v2["speed"])
        pred = model.predict([[dist, speed_diff]])[0]
        return ["SAFE","WARNING","CRITICAL"][pred]
    else:
        if dist < 40: return "CRITICAL"
        elif dist < 80: return "WARNING"
        return "SAFE"

# ---------------- LOG ----------------
def log_event(msg):
    with open("events.log","a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")

# ---------------- SIGNAL ----------------
signal_state = "GREEN"

def has_emergency():
    return any(v["type"]=="emergency" for v in vehicles.values())

def smart_signal():
    global signal_state

    if has_emergency():
        signal_state = "GREEN"
        return

    h_wait = sum(v["wait"] for v in vehicles.values() if v["dir"] in ["LEFT","RIGHT"])
    v_wait = sum(v["wait"] for v in vehicles.values() if v["dir"] in ["UP","DOWN"])

    signal_state = "GREEN" if h_wait >= v_wait else "RED"

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🚗 FINAL ULTRA PRO SYSTEM")
root.geometry("1200x620")

left = tk.Frame(root)
left.pack(side="left")

canvas = tk.Canvas(left, width=850, height=550)
canvas.pack()

right = tk.Frame(root, bg="#111")
right.pack(side="right", fill="y")

stats = tk.Label(right, fg="white", bg="#111")
stats.pack()

# ---------------- GRAPH ----------------
if HAS_PLOT:
    fig = Figure(figsize=(3,2))
    ax = fig.add_subplot(111)
    xdata = deque(maxlen=60)
    ydata = deque(maxlen=60)
    plot = FigureCanvasTkAgg(fig, master=right)
    plot.get_tk_widget().pack()

# ---------------- MAP ----------------
map_img = load_map()

# ---------------- UPDATE ----------------
tick = 0

def update():
    global tick

    canvas.delete("all")

    # MAP
    if map_img:
        canvas.create_image(0,0,image=map_img,anchor="nw")
    else:
        canvas.create_rectangle(0,0,850,550,fill="green")

    smart_signal()

    # DRAW SIGNALS
    for (x1,y1,x2,y2) in intersections:
        color = "green" if signal_state=="GREEN" else "red"
        canvas.create_oval(x1+40,y1+40,x1+60,y1+60,fill=color)

    # create vehicles if none
    if not vehicles:
        for i in range(6):
            vehicles[f"V{i}"] = {
                "x": random.randint(0,800),
                "y": random.randint(0,450),
                "dir": random.choice(["RIGHT","LEFT","UP","DOWN"]),
                "speed": 3,
                "base_speed": 3,
                "behavior": "NORMAL",
                "wait": 0,
                "crashed": False,
                "type": "normal"
            }

    # BRAKING
    for id1,v1 in vehicles.items():
        if v1["crashed"]: continue

        v1["speed"] = v1["base_speed"]

        for id2,v2 in vehicles.items():
            if id1!=id2:
                r = predict_collision(v1,v2)
                if r=="CRASH":
                    log_event(f"Crash {id1}-{id2}")
                elif r=="CRITICAL":
                    v1["speed"]=0
                elif r=="WARNING":
                    v1["speed"]=v1["base_speed"]*0.5

    warning = 0
    critical = 0

    # MOVE + DRAW
    for vid,v in vehicles.items():
        x,y = v["x"],v["y"]

        if v["crashed"]:
            canvas.create_text(x,y,text="💥",fill="red")
            continue

        stop = False
        for (x1,y1,x2,y2) in intersections:
            if x1<x<x2 and y1<y<y2:
                if (v["dir"] in ["LEFT","RIGHT"] and signal_state=="RED") or \
                   (v["dir"] in ["UP","DOWN"] and signal_state=="GREEN"):
                    stop = True

        if stop:
            v["wait"] += 1
        else:
            v["wait"] = 0

            if v["dir"]=="RIGHT": x+=v["speed"]
            elif v["dir"]=="LEFT": x-=v["speed"]
            elif v["dir"]=="UP": y-=v["speed"]
            elif v["dir"]=="DOWN": y+=v["speed"]

        if x>850: x=0
        if x<0: x=850
        if y>550: y=0
        if y<0: y=550

        v["x"],v["y"]=x,y

        # count risks
        for oid,other in vehicles.items():
            if vid==oid: continue
            r = predict_collision(v,other)
            if r=="CRITICAL": critical+=1
            elif r=="WARNING": warning+=1

        # COLOR BY BEHAVIOR
        color_map = {
            "AGGRESSIVE":"red",
            "NORMAL":"blue",
            "SAFE":"green"
        }
        color = color_map.get(v["behavior"],"blue")

        canvas.create_rectangle(x-10,y-5,x+10,y+5,fill=color)

        label = vid + ("🚑" if v["type"]=="emergency" else "")
        canvas.create_text(x,y-12,text=label,fill="white")

    avg_speed = sum(v["speed"] for v in vehicles.values())/len(vehicles)

    stats.config(text=f"""
Vehicles: {len(vehicles)}
Avg Speed: {avg_speed:.2f}
Warnings: {warning}
Critical: {critical}
Signal: {signal_state}
""")

    # GRAPH
    if HAS_PLOT:
        tick+=1
        xdata.append(tick)
        ydata.append(avg_speed)

        ax.clear()
        ax.plot(list(xdata), list(ydata))
        plot.draw()

    root.after(100, update)

# ---------------- RUN ----------------
update()
root.mainloop()