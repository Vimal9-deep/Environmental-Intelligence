# main.py-ENV-Int_Project

from section1Pollution.scripts.fetch_pollution import fetch_air_quality
from section1Pollution.scripts.analyze_pollution import analyze_latest
from section1Pollution.scripts.suggest_measures import suggest_measures

# --- Section 2 imports ---
from section2_Bioknowledge.scripts2.fetch_bioknowledge import fetch_bioknowledge
from section2_Bioknowledge.scripts2.analyze_bioknowledge import analyze_city_health

if __name__ == "__main__":
    city = input("Enter city name: ").strip()
    print("\n=== Environmental Health Analyzer: Section 1 ===\n")

    # 🏭 SECTION 1 — Pollution
    print("📡 Fetching pollution data...")
    data = fetch_air_quality(city)

    if not data:
        print(f"\n❌ No pollution data available for '{city}'.")
        print("➡️ Try a nearby major city (e.g., Kanpur, Lucknow, Delhi).")
    else:
        print("✅ Latest Data Fetched Successfully:")
        print(data)

        print("\n📊 Analyzing air quality (AQICN Scale)...")
        try:
            analysis = analyze_latest(city)
            print(f"City: {analysis['city']}")
            print(f"Time: {analysis['time']}")
            print(f"AQI: {analysis['aqi']} ({analysis['status']})")

            print("\n💡 Suggested Measures:")
            for m in suggest_measures(city):
                print("-", m)
        except Exception as e:
            print(f"\n⚠️ Error during analysis: {e}")
            print("Please check if the CSV has valid and complete data.")

# 🧬 SECTION 2 — Bioknowledge
print("\n=== Environmental Health Analyzer: Section 2 — (Bioknowledge) ===\n")

try:
    df = fetch_bioknowledge(city)
    if df is None or df.empty:
        print(f"⚠️ No bioknowledge data available for '{city}'.")
        print("➡️ Please add this region in health_dataset.csv under section2_Bioknowledge/data/")
    else:
        analyze_city_health(city)
except Exception as e:
    print(f"\n⚠️ Error analyzing bioknowledge data: {e}")


# === SECTION 3 — Life Expectancy Analysis ===
from section3_LE.scripts3.correlate_life_expectancy import correlate_life_expectancy

print("\n=== Environmental Health Analyzer: Section 3 — (Life Expectancy evaluation) ===\n")

try:
    correlate_life_expectancy(city)
except Exception as e:
    print(f"⚠️ Error analyzing life expectancy: {e}")



# --- Section 4 imports -------------
from section4_SoilFertility.scripts4.predict_soil_fertility import predict_soil_fertility

print("\n=== Environmental Health Analyzer: Section 4 — (Soil Fertility Prediction) ===\n")

try:
    predict_soil_fertility(city)
except Exception as e:
    print(f"⚠️ Error analyzing soil fertility: {e}")

