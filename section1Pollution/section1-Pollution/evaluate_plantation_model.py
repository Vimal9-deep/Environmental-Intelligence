# section1_pollution/evaluate_plantation_model.py

import pandas as pd
import joblib
import os

MODEL_PATH = "section1_pollution/models/plantation_model.pkl"
DATA_PATH = "section1_pollution/data/pollution_data.csv"

# --- Step 1: Load model and data ---
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model not found at {MODEL_PATH}. Train it first using train_plantation_model.py")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ Pollution data not found at {DATA_PATH}. Fetch pollution data first.")

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

# --- Step 2: Clean and prepare ---
required_cols = ["city", "pm2_5", "pm10", "co", "no2", "so2", "o3"]
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    raise ValueError(f"❌ Missing required columns in CSV: {missing_cols}")

df = df.dropna(subset=["pm2_5", "pm10", "co", "no2", "so2", "o3"])

# --- Step 3: Make predictions for each recent city ---
features = df[["pm2_5", "pm10", "co", "no2", "so2", "o3"]]
df["predicted_trees"] = model.predict(features).astype(int)

# --- Step 4: Show summary ---
print("\n🌿 Plantation Requirement Predictions (Recent Data):\n")
print(df[["city", "time", "pm2_5", "pm10", "co", "no2", "so2", "o3", "predicted_trees"]]
      .sort_values("time", ascending=False)
      .drop_duplicates("city")
      .reset_index(drop=True))

# --- Step 5: Check realistic prediction range ---
mean_trees = df["predicted_trees"].mean()
max_trees = df["predicted_trees"].max()
min_trees = df["predicted_trees"].min()
print("\n📊 Model Health Summary:")
print(f"   ➤ Average predicted trees per sq km: {mean_trees:.1f}")
print(f"   ➤ Range: {min_trees} – {max_trees}")

if max_trees > 500 or mean_trees > 200:
    print("⚠️ Warning: Predictions seem unusually high — consider retraining model with more balanced data.")
else:
    print("✅ Predictions are within realistic limits. Model is performing normally.")
