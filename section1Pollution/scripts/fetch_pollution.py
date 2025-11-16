import requests
import pandas as pd
import os
import time

DATA_DIR = "section1Pollution/section1-Pollution/data"
os.makedirs(DATA_DIR, exist_ok=True)
FILE_PATH = os.path.join(DATA_DIR, "pollution_data.csv") 

AQICN_KEY = "1cc134e1fd66d2ebe3f9ed6027daf3c3e95fa705"      # replace with your aqicn key
OWM_KEY = "90b06d1c012d5ac9a9eb54eabab330db"                # replace with your key


# ==========================================================
# 🔹 AQICN API
# ==========================================================
def fetch_from_aqicn(city):
    url = f"https://api.waqi.info/feed/{city}/?token={AQICN_KEY}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if data.get("status") != "ok":
            return None

        iaqi = data["data"].get("iaqi", {})
        def safe_get(p): return iaqi.get(p, {}).get("v", None)

        row = {
            "city": city,
            "time": data["data"]["time"]["s"],
            "co": safe_get("co"),
            "no2": safe_get("no2"),
            "o3": safe_get("o3"),
            "pm2_5": safe_get("pm25"),
            "pm10": safe_get("pm10"),
            "so2": safe_get("so2"),
            "aqi": data["data"].get("aqi"),
            "source": "AQICN"
        }
        return row

    except Exception:
        return None


# ==========================================================
# 🔹 OpenWeatherMap API (Fallback)
# ==========================================================
def fetch_from_openweathermap(city):
    try:
        # --- 1️⃣ Get coordinates ---
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OWM_KEY}"
        geo_resp = requests.get(geo_url, timeout=10).json()
        if not geo_resp:
            return None
        lat, lon = geo_resp[0]["lat"], geo_resp[0]["lon"]

        # --- 2️⃣ Get air pollution data ---
        air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OWM_KEY}"
        air_resp = requests.get(air_url, timeout=10).json()
        air_data = air_resp["list"][0]
        comps = air_data["components"]
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(air_data["dt"]))

        # --- 3️⃣ AQI Conversion (Balanced scale) ---
        # OWM (1–5): 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor
        # Converted to more balanced AQICN-like scale
        owm_aqi_scale = {
            1: 40,     # Good
            2: 85,     # Fair
            3: 120,    # Moderate
            4: 160,    # Poor
            5: 190     # Very Poor
        }
        converted_aqi = owm_aqi_scale.get(air_data["main"]["aqi"], 100)


        row = {
            "city": city,
            "time": timestamp,
            "co": round(comps.get("co", 0), 2),
            "no2": round(comps.get("no2", 0), 2),
            "o3": round(comps.get("o3", 0), 2),
            "pm2_5": round(comps.get("pm2_5", 0), 2),
            "pm10": round(comps.get("pm10", 0), 2),
            "so2": round(comps.get("so2", 0), 2),
            "aqi": converted_aqi,
            "source": "OWM"
        }
        return row

    except Exception:
        return None


# ==========================================================
# 🔹 Save to CSV
# ==========================================================
def save_row(row):
    df_new = pd.DataFrame([row])
    if not os.path.exists(FILE_PATH) or os.stat(FILE_PATH).st_size == 0:
        df_new.to_csv(FILE_PATH, index=False)
        print(f"✅ New CSV created and record added for {row['city']} at {row['time']}")
    else:
        df_existing = pd.read_csv(FILE_PATH)
        duplicate = ((df_existing["city"] == row["city"]) & (df_existing["time"] == row["time"])).any()
        if not duplicate:
            df_new.to_csv(FILE_PATH, mode='a', index=False, header=False)
            print(f"✅ New record appended for {row['city']} at {row['time']}")


# ==========================================================
# 🔹 Master Fetch Function (AQICN → OWM)
# ==========================================================
def fetch_air_quality(city):
    city = city.strip().lower()
    
    # Try AQICN first
    row = fetch_from_aqicn(city)
    if row:
        print(f"Source of data coming: {row['source']},")
        print(f"🌍 Data successfully fetched by {row['source']} for {city}")
        save_row(row)
        return row

    # Fallback
    row = fetch_from_openweathermap(city)
    if row:
        print(f"Source of data coming: {row['source']},")
        print(f"🌍 Data successfully fetched by {row['source']} for {city}")
        save_row(row)
        return row

    print(f"❌ No data available for '{city}' from either API.")
    return None


# ==========================================================
# 🔹 Runner
# ==========================================================
if __name__ == "__main__":
    city = input("Enter city name: ").strip()
    data = fetch_air_quality(city)
    if data:
        print("✅ Latest Data Fetched Successfully:")
        print(data)
