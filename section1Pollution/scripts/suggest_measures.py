import pandas as pd
import joblib
import numpy as np

def suggest_measures(city_name=None): 
    # Load latest pollution data
    df = pd.read_csv("section1Pollution/section1-Pollution/data/pollution_data.csv")

    # ✅ Filter by city if provided 
    if city_name:
        city_name = city_name.strip().lower()
        df_city = df[df["city"].str.lower() == city_name]
        if df_city.empty:
            raise ValueError(f"❌ No data found for city '{city_name}'. Fetch data first.")
        latest = df_city.iloc[-1]
    else:
        latest = df.iloc[-1]

    measures = []
    plantation = None
    mask_required = "No mask required"

    # --- Load trained ML model ---
    model = joblib.load("section1Pollution/section1-Pollution/models/plantation_model.pkl")

    # Features must match training dataset 
    features = pd.DataFrame([{
        "pm2_5": latest["pm2_5"],
        "pm10": latest["pm10"],
        "co": latest["co"],
        "no2": latest["no2"],
        "so2": latest["so2"],
        "o3": latest["o3"]
    }])
    
    predicted_trees = int(model.predict(features)[0])

    # --- Plantation Requirement ---
    if predicted_trees > 50:
        plantation = f"{predicted_trees} trees per sq km needed"
    else:
        plantation = "Not urgent (within safe limits)"

    measures.append(f"🌳 Plantation Requirement (ML): {plantation}")

    # --- Mask recommendation ---
    if latest["pm2_5"] > 37.5:
        mask_required = "Wear mask while going outside"

    measures.append(f"😷 Mask Advisory: {mask_required}")

    # --- Pollution control measures as per WHO Standards ---
    if latest["pm2_5"] > 15:
        measures.append("🌿 Encourage plantation drives to reduce PM2.5")
    if latest["co"] >= 200:
        measures.append("🚗 Reduce vehicle use, promote public transport")
    if latest["so2"] >= 40:
        measures.append("🏭 Control industrial emissions (SO₂ beyond safe limit)")
    if latest["no2"] >= 25:
        measures.append("🚦 Reduce traffic congestion (NO₂ too high)")

    # --- Good condition ---
    if latest["pm2_5"] <= 15:
        measures.append("✅ Air quality is excellent. Maintain greenery!")

    return measures


if __name__ == "__main__":
    for m in suggest_measures():
        print("-", m)
