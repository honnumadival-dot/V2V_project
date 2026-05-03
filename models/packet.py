import time

class VehiclePacket:
    def __init__(self, vid, distance, speed, timestamp=None):
        self.id = vid
        self.distance = distance
        self.speed = speed
        self.timestamp = timestamp or time.time()

    def is_valid(self):
        return self.distance > 0 and self.speed >= 0