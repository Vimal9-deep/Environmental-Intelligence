# section1_pollution/train_plantation_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# 1. Load dataset
file_path = "section1Pollution/section1-Pollution/data/plantation_training_data.csv"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ Dataset not found at {file_path}. Please place it inside 'section1_pollution/'.")

df = pd.read_csv(file_path)

# 2. Features & Target
X = df[["pm2_5", "pm10", "co", "no2", "so2", "o3"]]   
y = df["trees_needed"]

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Train model (Random Forest for accuracy & interpretability)
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# 5. Save model
model_path = "section1-Pollution/models/plantation_model.pkl"
os.makedirs(os.path.dirname(model_path), exist_ok=True) 

joblib.dump(model, model_path)

# 6. Optional: Evaluate accuracy
score = model.score(X_test, y_test)
print(f"✅ Model trained successfully | Saved at {model_path} | R² Score: {score:.2f}")


