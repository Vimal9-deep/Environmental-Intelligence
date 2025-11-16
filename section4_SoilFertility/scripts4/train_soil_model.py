# section4_SoilFertility/scripts4/train_soil_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

def train_soil_model():
    """Train an ML model to predict soil fertility based on nutrient composition."""

    data_path = "section4_SoilFertility/data/soil_fertility.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Dataset not found at {data_path}")

    df = pd.read_csv(data_path) 

    # ✅ Normalize and clean column names
    df.columns = [c.strip().lower().replace(" ", "") for c in df.columns]

    # Feature selection
    X = df[["zn%", "fe%", "cu%", "mn%", "b%", "s%"]]

    # Create synthetic target: fertile if ≥ 4 nutrients > 70%
    df["fertile"] = ((X > 70).sum(axis=1) >= 4).astype(int)
    y = df["fertile"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ✅ Scaling and model training
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train) 

    # Save model and scaler
    os.makedirs("section4_SoilFertility/models", exist_ok=True)
    joblib.dump(model, "section4_SoilFertility/models/soil_fertility_model.pkl")
    joblib.dump(scaler, "section4_SoilFertility/models/scaler.pkl")

    print("✅ Soil Fertility Model trained and saved successfully!")

if __name__ == "__main__":
    train_soil_model()
