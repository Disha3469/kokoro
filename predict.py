import joblib
import numpy as np

# Example ML Model for Predictions (Train and Save)
from sklearn.linear_model import LinearRegression

# Dummy Training Data
X = np.array([[5000, 7], [6000, 6], [7000, 8]])  # Steps, Sleep Hours
y = np.array([2000, 2500, 3000])  # Calories Burned

model = LinearRegression()
model.fit(X, y)

# Save the model
joblib.dump(model, "calories_predictor.pkl")

# Load and Predict
def predict_calories(steps, sleep_hours):
    model = joblib.load("calories_predictor.pkl")
    prediction = model.predict([[steps, sleep_hours]])
    return prediction[0]

# Example usage
calories = predict_calories(6500, 7)
print(f"Predicted Calories: {calories}")
