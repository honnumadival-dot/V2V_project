import socket
import json
from config import UDP_IP, UDP_PORT

# create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind to this vehicle's port
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

# ---------------- SEND ----------------
def send(data):
    message = json.dumps(data).encode()

    # send to all vehicle ports
    ports = [5005, 5006]

    for port in ports:
        sock.sendto(message, (UDP_IP, port))

# ---------------- RECEIVE ----------------
def receive():
    try:
        data, _ = sock.recvfrom(1024)
        return json.loads(data.decode())
    except:
        return None