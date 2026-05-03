import socket
import json
from config import UDP_IP, UDP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind receiver
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

def send(data):
    message = json.dumps(data).encode()
    sock.sendto(message, (UDP_IP, UDP_PORT))

def receive():
    try:
        data, _ = sock.recvfrom(1024)
        return json.loads(data.decode())
    except:
        return None