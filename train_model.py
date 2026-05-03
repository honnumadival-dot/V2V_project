from sklearn.tree import DecisionTreeClassifier
import joblib

X = [
    [10, 20],
    [15, 30],
    [40, 10],
    [70, 5]
]

y = [2,2,1,0]  # CRITICAL, WARNING, SAFE

model = DecisionTreeClassifier()
model.fit(X, y)

joblib.dump(model, "collision_model.pkl")
print("Model trained")