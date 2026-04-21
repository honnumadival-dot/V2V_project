import socket
import json
import random
import time

# Configuration
HOST = "127.0.0.1"
PORT = 5000

# Smart Collision Function
def smart_collision(my_data, other_data):
    speed_diff = abs(my_data["speed"] - other_data["speed"])

    if my_data["distance"] < 20 and speed_diff > 30:
        return "🚨 CRITICAL COLLISION"
    elif my_data["distance"] < 50 or other_data["distance"] < 50:
        return "⚠️ WARNING"
    else:
        return "✅ SAFE"

# Socket setup (Client)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("🚗 Vehicle B connected!")

count = 0

try:
    while True:
        count += 1

        # Receive data from Vehicle A
        received = json.loads(client.recv(1024).decode())

        # Generate Vehicle B data
        data_B = {
            "vehicle": "B",
            "distance": random.randint(5, 100),
            "speed": random.randint(20, 80)
        }

        # Send data to Vehicle A
        client.send(json.dumps(data_B).encode())

        # Collision logic
        risk = smart_collision(data_B, received)

        # Display output
        print(f"""
🚗 VEHICLE B REPORT
---------------------------
My Data       : {data_B}
Other Vehicle : {received}
Risk Level    : {risk}
---------------------------
""")

        # Save log
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"B: {data_B} | A: {received} | {risk}\n")

        # Stop after 10 iterations (optional)
        if count == 10:
            print("🛑 Vehicle B stopping...")
            break

        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped manually")

finally:
    client.close()