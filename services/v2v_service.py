from modules import decision, ai_module, logging_system
from analytics import graph

def process_vehicle(my_speed, vid, data):
    distance = data["distance"]
    other_speed = data["speed"]

    ttc = decision.calculate_ttc(distance, my_speed, other_speed)

    score = ai_module.predict_risk_score(distance, ttc)
    risk = ai_module.classify(score)

    # logging
    logging_system.log_event({
        "id": vid,
        "distance": distance,
        "ttc": round(ttc, 2),
        "risk": risk
    })

    # graph
    graph.update_graph(vid, distance)

    return ttc, risk, score