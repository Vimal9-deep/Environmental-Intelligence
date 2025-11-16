import pandas as pd
import os

FILE_PATH = "section1Pollution/section1-Pollution/data/pollution_data.csv"

def classify_air_quality(aqi): 
    """Categorize AQI based on AQICN  website and API standards"""
    if aqi <= 50: return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 150: return "Unhealthy for Sensitive Groups"
    elif aqi <= 200: return "Unhealthy"
    elif aqi <= 300: return "Very Unhealthy"
    else: return "Hazardous" 

def analyze_latest(city_name=None):
    """Analyze the most recent record, optionally filtered by city"""
    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError(f"❌ {FILE_PATH} not found. Run fetch_pollution first.")

    df = pd.read_csv(FILE_PATH)
    if df.empty:
        raise ValueError("❌ pollution_data.csv exists but has no rows. Run fetch_pollution again.")

    required_cols = {"city", "time", "aqi", "co", "no2", "o3", "pm2_5", "pm10", "so2"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(f"❌ CSV columns mismatch. Expected at least: {sorted(required_cols)}")

    if city_name:
        city_name = city_name.strip().lower()
        df_city = df[df["city"].str.lower() == city_name]
        if df_city.empty:
            raise ValueError(f"❌ No data found for city '{city_name}'. Fetch data first.")
        latest = df_city.iloc[-1]
    else:
        latest = df.iloc[-1]

    if pd.isna(latest["aqi"]):
        raise ValueError("❌ Latest row has missing 'aqi' value.")

    aqi = int(latest["aqi"])
    status = classify_air_quality(aqi)

    return {
        "city": latest["city"],
        "time": latest["time"],
        "aqi": aqi,
        "status": status
    }

if __name__ == "__main__":
    city = input("Enter city name (or leave blank for last record): ").strip()
    city = city if city else None
    print(analyze_latest(city))
