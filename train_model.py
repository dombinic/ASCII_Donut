import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Simulated Dataset
# Inputs: speed_input (rotation speed preference), luminance_input (brightness preference)
# Outputs: A_step and B_step (adjustments to rotation speed)
speed_range = np.linspace(0.5, 3.0, 10)  # Speed values from 0.5 to 3.0
luminance_range = np.linspace(1, 5, 10)  # Luminance values from 1 to 5

# Create mesh grid and flatten
speed_input, luminance_input = np.meshgrid(speed_range, luminance_range)
speed_input = speed_input.flatten()
luminance_input = luminance_input.flatten()

# Define outputs (A_step and B_step) using a simple formula
A_step = 0.03 + 0.01 * speed_input - 0.002 * luminance_input
B_step = 0.02 + 0.008 * luminance_input + 0.005 * speed_input

# Combine into a DataFrame
data = {
    "speed_input": speed_input,
    "luminance_input": luminance_input,
    "A_step": A_step,
    "B_step": B_step
}

df = pd.DataFrame(data)
print("Sample Data:")
print(df.head())  # Display the first few rows of the dataset

# Train Model
X = df[['speed_input', 'luminance_input']]
y = df[['A_step', 'B_step']]

model = LinearRegression()
model.fit(X, y)

# Save Trained Model
joblib.dump(model, "Rotation_Model.pkl")
print("✅ Model retrained and saved as 'Rotation_Model.pkl'")
