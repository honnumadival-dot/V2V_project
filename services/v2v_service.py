import time
from models.packet import VehiclePacket
from modules import communication, sensor, decision, alert
from modules.data_processing import DataFilter
from modules.logging_system import log_event
from services.shared import update_vehicle, get_all_vehicles
from config import SEND_INTERVAL, RECEIVE_INTERVAL

filter_obj = DataFilter()

def send_loop(vehicle_id):
    while True:
        dist = sensor.get_distance()
        speed = sensor.get_speed()

        dist = filter_obj.smooth(dist)

        packet = VehiclePacket(vehicle_id, dist, speed)
        communication.send(packet)

        print(f"[TX] Me(ID {vehicle_id}) Dist={dist:.1f} Speed={speed}")
        log_event(f"TX {vehicle_id} {dist:.1f} {speed}")

        time.sleep(SEND_INTERVAL)


def receive_loop(vehicle_id):
    while True:
        packet = communication.receive()

        if packet and packet.id != vehicle_id:
            update_vehicle(packet)
            print(f"[RX] Vehicle {packet.id} Dist={packet.distance}")
            log_event(f"RX {packet.id} {packet.distance}")

        time.sleep(RECEIVE_INTERVAL)


def decision_loop(vehicle_id):
    while True:
        vehicles = get_all_vehicles()
        my_speed = sensor.get_speed()

        for vid, data in vehicles.items():
            rel_speed = abs(my_speed - data.speed)
            ttc = decision.calculate_ttc(data.distance, rel_speed)
            risk = decision.risk_score(ttc)

            print(f"[CHECK] Vehicle {vid} TTC={ttc:.2f} Risk={risk}")
            alert.trigger_alert(vid, risk)

            log_event(f"CHECK {vid} TTC={ttc:.2f} {risk}")

        time.sleep(0.3)