import socket
<<<<<<< HEAD
import json
=======
>>>>>>> 1a5c7d875abff1de9f30a03afaf173295784dd35
import random
import time

host = "127.0.0.1"
port = 5000

<<<<<<< HEAD
# Smart Collision Function
def smart_collision(my_data, other_data):
    speed_diff = abs(my_data["speed"] - other_data["speed"])

    if my_data["distance"] < 20 and speed_diff > 30:
        return "🚨 CRITICAL COLLISION"
    elif my_data["distance"] < 50 or other_data["distance"] < 50:
        return "⚠️ WARNING"
    else:
        return "✅ SAFE"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("🚗 Vehicle B connected!")

count = 0

try:
    while True:
        count += 1

        # Receive first
        received = json.loads(client.recv(1024).decode())

        # Generate data
        data_B = {
            "vehicle": "B",
            "distance": random.randint(5, 100),
            "speed": random.randint(20, 80)
        }

        # Send response
        client.send(json.dumps(data_B).encode())

        # Smart collision
        risk = smart_collision(data_B, received)

        # Output
        print(f"""
🚗 VEHICLE B REPORT
---------------------------
My Data       : {data_B}
Other Vehicle : {received}
Risk Level    : {risk}
---------------------------
""")

        # Logging
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"B: {data_B} | A: {received} | {risk}\n")

        if count == 10:
            print("🛑 Vehicle B stopping...")
            break

        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped manually")

finally:
    client.close()
=======
client = socket.socket()
client.connect((host, port))

print("🚗 Vehicle B connected!")

while True:
    # Receive from A
    data = client.recv(1024).decode()
    print(f"\n📡 From Vehicle A: {data}")

    # Simulated data
    distance = random.randint(5, 100)
    speed = random.randint(20, 80)

    # Collision logic
    if distance < 20:
        alert = "DANGER 🚨"
    elif distance < 50:
        alert = "WARNING ⚠️"
    else:
        alert = "SAFE ✅"

    message = f"B | Dist:{distance} | Speed:{speed} | {alert}"
    client.send(message.encode())

    print(f"📤 Sent: {message}")
    print("----------------------")

    time.sleep(2)
>>>>>>> 1a5c7d875abff1de9f30a03afaf173295784dd35
