import socket
import time
import random

HOST = '127.0.0.1'
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    speed = random.randint(20, 100)
    distance = random.randint(10, 100)

    data = str(speed) + "," + str(distance)
    client.send(data.encode())

    print("Sent Speed:", speed, "Distance:", distance)

    time.sleep(2)