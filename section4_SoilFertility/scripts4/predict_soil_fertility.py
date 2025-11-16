# section4_SoilFertility/scripts4/predict_soil_fertility.py

import pandas as pd
import joblib
import os

def predict_soil_fertility(region_name): 
    """
    Predicts soil fertility of the entered region (district) using trained ML model.
    """

    data_path = "section4_SoilFertility/data/soil_fertility.csv"
    model_path = "section4_SoilFertility/models/soil_fertility_model.pkl"
    scaler_path = "section4_SoilFertility/models/scaler.pkl"

    # ✅ Load dataset
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Dataset not found at {data_path}")

    df = pd.read_csv(data_path)
    df.columns = [c.strip().lower().replace(" ", "") for c in df.columns]  # normalize

    # ✅ Check if district column exists
    if "district" not in df.columns:
        raise KeyError("⚠️ 'District' column not found. Please verify CSV headers.")

    # ✅ Case-insensitive match for region
    region_data = df[df["district"].str.lower() == region_name.lower()]

    if region_data.empty:
        print(f"⚠️ Sorry, no soil data available for region '{region_name}'.")
        return

    # ✅ Extract nutrient features
    feature_cols = ["zn%", "fe%", "cu%", "mn%", "b%", "s%"]
    X = region_data[feature_cols]

    # ✅ Load model and scaler
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError("⚠️ Model or scaler not found! Train them first using train_soil_model.py")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    # ✅ Predict
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)[0] 

    # ✅ Display result
    print(f"\n🌾 Soil Fertility Analysis for region: {region_name.title()}\n")
    if prediction == 1:
        print("✅ The soil in this region is **FERTILE** — suitable for cultivation and vegetation growth.")
    else:
        print("🚫 The soil in this region is **NOT FERTILE** — needs enrichment and organic treatment.")
