def calculate_ttc(distance, my_speed, other_speed):
    relative_speed = my_speed - other_speed

    if relative_speed <= 0:
        return float('inf')  # no collision

    return distance / relative_speed


def risk_level(distance, ttc):
    if distance < 10 or ttc < 2:
        return "CRITICAL"
    elif distance < 30 or ttc < 5:
        return "WARNING"
    else:
        return "SAFE"