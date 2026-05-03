import threading

vehicle_buffer = {}
lock = threading.Lock()

def update_vehicle(packet):
    with lock:
        vehicle_buffer[packet.id] = packet

def get_all_vehicles():
    with lock:
        return dict(vehicle_buffer)