from config import SAFE_TTC

def calculate_ttc(distance, rel_speed):
    if rel_speed <= 0:
        return float('inf')
    return distance / rel_speed

def risk_score(ttc):
    if ttc < 1:
        return "CRITICAL"
    elif ttc < SAFE_TTC:
        return "HIGH"
    elif ttc < SAFE_TTC * 2:
        return "MEDIUM"
    return "LOW"