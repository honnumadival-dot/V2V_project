import socket
import json
import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

HOST = '127.0.0.1'
PORT = 65432

# Data storage for graph
distance_data = []
speed_data = []
time_data = []
t = 0

def smart_collision(my_data, other_data):
    speed_diff = abs(my_data["speed"] - other_data["speed"])

    if my_data["distance"] < 20 and speed_diff > 30:
        return "CRITICAL"
    elif my_data["distance"] < 50 or other_data["distance"] < 50:
        return "WARNING"
    else:
        return "SAFE"

# -------- SOCKET --------
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print("🚗 Server started...")
conn, addr = server.accept()
print("✅ Connected!")

# -------- GUI --------
root = tk.Tk()
root.title("Vehicle A Dashboard")
root.geometry("600x500")

title = tk.Label(root, text="🚗 Vehicle A", font=("Arial", 18))
title.pack()

my_label = tk.Label(root, text="")
my_label.pack()

other_label = tk.Label(root, text="")
other_label.pack()

risk_label = tk.Label(root, text="", font=("Arial", 14))
risk_label.pack()

# -------- GRAPH SETUP --------
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

def update_graph():
    ax.clear()
    ax.plot(time_data, distance_data, label="Distance")
    ax.plot(time_data, speed_data, label="Speed")
    ax.legend()
    ax.set_title("Vehicle Data Over Time")
    canvas.draw()

# -------- MAIN LOOP --------
def update():
    global t

    try:
        data_A = {
            "vehicle": "A",
            "distance": random.randint(5, 100),
            "speed": random.randint(20, 80)
        }

        conn.send(json.dumps(data_A).encode())
        received = json.loads(conn.recv(1024).decode())

        risk = smart_collision(data_A, received)

        # Update labels
        my_label.config(text=f"My: {data_A}")
        other_label.config(text=f"Other: {received}")
        risk_label.config(text=f"Risk: {risk}")

        if risk == "CRITICAL":
            risk_label.config(fg="red")
        elif risk == "WARNING":
            risk_label.config(fg="orange")
        else:
            risk_label.config(fg="green")

        # Store data
        distance_data.append(data_A["distance"])
        speed_data.append(data_A["speed"])
        time_data.append(t)
        t += 1

        # Limit size
        if len(time_data) > 20:
            time_data.pop(0)
            distance_data.pop(0)
            speed_data.pop(0)

        update_graph()

    except Exception as e:
        print("Waiting...")

    root.after(2000, update)

update()
root.mainloop()

conn.close()
server.close()