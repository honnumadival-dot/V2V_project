def predict_risk(history):

    if len(history) < 3:
        return "NORMAL"

    decreasing = 0

    for i in range(len(history)-1):

        if history[i+1] < history[i]:
            decreasing += 1

    if decreasing >= 3:
        return "HIGH COLLISION CHANCE"

    elif decreasing >= 1:
        return "APPROACHING"

    return "STABLE"