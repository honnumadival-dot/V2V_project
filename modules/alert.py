def trigger_alert(vehicle_id, level):
    if level == "CRITICAL":
        print(f"🚨 Vehicle {vehicle_id}: IMMEDIATE DANGER")
    elif level == "HIGH":
        print(f"⚠️ Vehicle {vehicle_id}: High Risk")
    elif level == "MEDIUM":
        print(f"⚠️ Vehicle {vehicle_id}: Moderate Risk")