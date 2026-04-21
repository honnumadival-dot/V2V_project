import socket
import json
import tkinter as tk
from tkinter import ttk
import threading

HOST = '127.0.0.1'
PORT = 5000

# Store all vehicles data
vehicles = {}

# ---------------- SOCKET CLIENT ----------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("📡 Dashboard connected to server")

# ---------------- COLLISION LOGIC ----------------
def smart_collision(v1, v2):
    speed_diff = abs(v1["speed"] - v2["speed"])

    if v2["distance"] < 20 and speed_diff > 30:
        return "CRITICAL"
    elif v2["distance"] < 50:
        return "WARNING"
    else:
        return "SAFE"

# ---------------- RECEIVE DATA ----------------
def receive():
    while True:
        try:
            data = json.loads(client.recv(1024).decode())

            vehicles[data["vehicle"]] = data

        except:
            break

# Start receiving thread
threading.Thread(target=receive, daemon=True).start()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🚦 Multi-Vehicle Dashboard")
root.geometry("600x400")

title = tk.Label(root, text="V2V Multi Vehicle System", font=("Arial", 18))
title.pack(pady=10)

# Table
columns = ("Vehicle", "Distance", "Speed", "Risk")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True)

# ---------------- UPDATE GUI ----------------
def update_table():
    tree.delete(*tree.get_children())

    for vid, data in vehicles.items():
        # Calculate risk vs others
        risk = "SAFE"
        for other_id, other_data in vehicles.items():
            if vid != other_id:
                r = smart_collision(data, other_data)
                if r == "CRITICAL":
                    risk = "CRITICAL"
                    break
                elif r == "WARNING":
                    risk = "WARNING"

        tree.insert("", "end", values=(
            vid,
            data["distance"],
            data["speed"],
            risk
        ))

    root.after(1000, update_table)

update_table()
root.mainloop()
