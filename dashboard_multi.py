import socket
import json
import tkinter as tk
from tkinter import ttk
import threading

HOST = '127.0.0.1'
PORT = 5000

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
            print("⚠️ Connection lost")
            break

threading.Thread(target=receive, daemon=True).start()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🚦 Smart Traffic Dashboard")
root.geometry("650x450")

title = tk.Label(root, text="V2V Multi Vehicle Monitor", font=("Arial", 18))
title.pack(pady=10)

# ALERT LABEL
alert_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
alert_label.pack()

# TABLE
columns = ("Vehicle", "Distance", "Speed", "Risk")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True)

# ---------------- COLOR TAGS ----------------
tree.tag_configure("SAFE", background="lightgreen")
tree.tag_configure("WARNING", background="orange")
tree.tag_configure("CRITICAL", background="red")

# FLASH CONTROL
flash = False

# ---------------- UPDATE FUNCTION ----------------
def update_table():
    global flash

    tree.delete(*tree.get_children())

    critical_found = False

    for vid, data in vehicles.items():
        risk = "SAFE"

        for other_id, other_data in vehicles.items():
            if vid != other_id:
                r = smart_collision(data, other_data)

                if r == "CRITICAL":
                    risk = "CRITICAL"
                    critical_found = True
                    break

                elif r == "WARNING":
                    risk = "WARNING"

        # INSERT WITH COLOR TAG
        tree.insert("", "end", values=(
            vid,
            data["distance"],
            data["speed"],
            risk
        ), tags=(risk,))

    # ---------------- ALERT SYSTEM ----------------
    if critical_found:
        flash = not flash
        if flash:
            alert_label.config(text="🚨 CRITICAL COLLISION RISK!", fg="red")
        else:
            alert_label.config(text="")
    else:
        alert_label.config(text="✅ All vehicles safe", fg="green")

    root.after(1000, update_table)

# START LOOP
update_table()
root.mainloop()