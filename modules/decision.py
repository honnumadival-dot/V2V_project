def calculate_ttc(distance, my_speed, other_speed):

    relative_speed = abs(my_speed - other_speed)

    if relative_speed == 0:
        return 999

    return distance / relative_speed


def risk_level(distance, ttc):

    if distance < 10 or ttc < 2:
        return "CRITICAL"

    elif distance < 30 or ttc < 5:
        return "WARNING"

    return "SAFE"