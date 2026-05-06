def predict_risk_score(distance, ttc):
    score = 0

    if distance < 30:
        score += 40
    if distance < 10:
        score += 40

    if ttc < 5:
        score += 30
    if ttc < 2:
        score += 30

    return min(score, 100)


def classify(score):
    if score > 80:
        return "CRITICAL"
    elif score > 50:
        return "WARNING"
    else:
        return "SAFE"