import numpy as np
from sklearn.tree import DecisionTreeClassifier
import joblib

# distance, speed_diff
X = [
    [10, 40],
    [15, 35],
    [30, 10],
    [60, 5],
    [80, 2]
]

y = [
    2,  # CRITICAL
    2,
    1,  # WARNING
    0,  # SAFE
    0
]

model = DecisionTreeClassifier()
model.fit(X, y)

joblib.dump(model, "model.pkl")
print("Model trained")