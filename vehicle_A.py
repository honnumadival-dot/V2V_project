import socket
import json
import random
import tkinter as tk

# Configuration
HOST = "127.0.0.1"
PORT = 5000

# Smart collision logic
def smart_collision(my_data, other_data):
    speed_diff = abs(my_data["speed"] - other_data["speed"])

    if my_data["distance"] < 20 and speed_diff > 30:
        return "CRITICAL"
    elif my_data["distance"] < 50 or other_data["distance"] < 50:
        return "WARNING"
    else:
        return "SAFE"

# GUI Setup
root = tk.Tk()
root.title("Vehicle A Dashboard")
root.geometry("400x300")

title = tk.Label(root, text="🚗 Vehicle A", font=("Arial", 18))
title.pack(pady=10)

my_label = tk.Label(root, text="")
my_label.pack()

other_label = tk.Label(root, text="")
other_label.pack()

risk_label = tk.Label(root, text="", font=("Arial", 14))
risk_label.pack(pady=10)

# Socket Setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("🚗 Vehicle A waiting for connection...")
conn, addr = server.accept()
print(f"Connected to {addr}")

# Update function
def update():
    try:
        # Generate Vehicle A data
        data_A = {
            "vehicle": "A",
            "distance": random.randint(5, 100),
            "speed": random.randint(20, 80)
        }

        # Send data to Vehicle B
        conn.send(json.dumps(data_A).encode())

        # Receive data from Vehicle B
        received = json.loads(conn.recv(1024).decode())

        # Risk calculation
        risk = smart_collision(data_A, received)

        # Update GUI
        my_label.config(text=f"My Data: {data_A}")
        other_label.config(text=f"Other: {received}")
        risk_label.config(text=f"Risk: {risk}")

        # Color indication
        if risk == "CRITICAL":
            risk_label.config(fg="red")
        elif risk == "WARNING":
            risk_label.config(fg="orange")
        else:
            risk_label.config(fg="green")

    except Exception as e:
        print("Error:", e)

    root.after(2000, update)

# Start loop
update()
root.mainloop()