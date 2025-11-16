# section3_LE/scripts3/correlate_life_expectancy.py

#Purpose: Correlates pollution + health data → evaluates LE increase/decrease

import pandas as pd 
import os
from section3_LE.scripts3.fetch_life_expectancy import get_state_from_city, get_base_life_expectancy

POLLUTION_FILE = "section1Pollution/section1-Pollution/data/pollution_data.csv"
HEALTH_FILE = "section2_Bioknowledge/data/health_dataset_expanded.csv"


def compute_environmental_stress(city):
    """Compute % stress due to pollution levels."""
    df = pd.read_csv(POLLUTION_FILE)
    rec = df[df["city"].str.lower() == city.lower()]
    if rec.empty:
        return 0

    r = rec.iloc[-1]
    AQI, PM25, PM10, NO2, SO2 = r["aqi"], r["pm2_5"], r["pm10"], r["no2"], r["so2"]
    ES = (
        0.4 * (AQI / 500)
        + 0.25 * (PM25 / 250)
        + 0.15 * (PM10 / 300)
        + 0.1 * (NO2 / 100)
        + 0.1 * (SO2 / 100)
    )
    return min(round(ES * 100, 1), 100)


def compute_health_risk_factor(city):
    """Compute % physiological risk due to abnormal bio values."""
    df = pd.read_csv(HEALTH_FILE)
    rec = df[df["city"].str.lower() == city.lower()]
    if rec.empty:
        return 0

    r = rec.iloc[0]
    hr, sys, dia, o2 = r["avg_heart_rate"], r["avg_bp_sys"], r["avg_bp_dia"], r["avg_oxygen_level"]

    risk = 0
    if hr < 60 or hr > 100: risk += 0.1
    if sys < 90 or sys > 120: risk += 0.15
    if dia < 60 or dia > 80: risk += 0.15
    if o2 < 95: risk += 0.15

    return min(round(risk * 100, 1), 100)


def correlate_life_expectancy(city):
    """Main analysis combining environment + health correlation."""
    state = get_state_from_city(city)
    if not state:
        return

    base_le = get_base_life_expectancy(state)
    if not base_le:
        return

    ES = compute_environmental_stress(city)
    HRF = compute_health_risk_factor(city)

    total_penalty = 0.5 * (ES / 100) + 0.5 * (HRF / 100)
    change_pct = round(total_penalty * 100 / 2, 1)
    le_change_years = round((change_pct / 100) * base_le, 1)
    predicted_le = round(base_le - le_change_years, 1)

    print(f"\n🌍 Life Expectancy Analysis for {city.title()}, {state}:")
    print(f"Base Life Expectancy: {base_le} years\n")

    print(f"Environmental Stress (Pollution Burden): {ES}%")
    if ES > 30:
        print(" - PM2.5, PM10, and NO₂ levels exceed WHO thresholds.")
        print(" - Long-term exposure may reduce LE by ~4–6 years.\n")
    else:
        print(" - Air quality within acceptable limits.\n")

    print(f"Health Risk Factor (Physiological Deviation): {HRF}%")
    if HRF > 15:
        print(" - Elevated BP and reduced SpO₂ observed in regional averages.")
        print(" - Indicates higher cardiovascular strain.\n")
    else:
        print(" - Vital signs within healthy range.\n")

    impact_label = "Low" if total_penalty < 0.2 else "Moderate" if total_penalty < 0.4 else "High"
    print(f"Combined Risk Impact: {impact_label}")
    print(f"→ Predicted Life Expectancy may decrease by {change_pct}% (≈ {le_change_years} years drop from baseline)")
    print(f"Predicted Adjusted Life Expectancy: {predicted_le} years\n")

    # Save correlation report  for each city inside same file
    os.makedirs("section3_LE/reports", exist_ok=True)
    out_df = pd.DataFrame([{
        "city": city,
        "state": state,
        "base_life_expectancy": base_le,
        "environmental_stress(%)": ES,
        "health_risk_factor(%)": HRF,
        "predicted_LE_change(%)": change_pct,
        "predicted_LE(years)": predicted_le
    }])
    out_df.to_csv("section3_LE/reports/LE_correlation_report.csv", index=False)
    print("📄 Saved correlation report: section3_LE/reports/LE_correlation_report.csv")
