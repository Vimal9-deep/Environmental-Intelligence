import pandas as pd
import os

def fetch_bioknowledge(city_name):
    """
    Fetches bio-data (heart rate, BP, O₂) for a given city.
    Reads from local CSV located at section2_Bioknowledge/data/health_dataset_expanded.csv
    """
    data_path = "section2_Bioknowledge/data/health_dataset_expanded.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Dataset not found at {data_path}")

    df = pd.read_csv(data_path)

    # Normalize column names (case-insensitive + strip spaces)
    df.columns = df.columns.str.strip().str.lower()

    # Normalize city names too
    df["city"] = df["city"].str.strip().str.lower() 

    # Filter city (case insensitive) 
    city_data = df[df["city"] == city_name.lower()]

    if city_data.empty:
        print(f"⚠️ No bioknowledge data found for {city_name}.")
        return None

    print(f"✅ Found {len(city_data)} records for {city_name}.")
    return city_data
