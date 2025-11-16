import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from section2_Bioknowledge.scripts2.fetch_bioknowledge import fetch_bioknowledge

def analyze_city_health(city):
    """Compares regional bio-data against healthy ranges, prints results, saves report & visualizes."""
    df = fetch_bioknowledge(city)
    if df is None or df.empty:
        return

    # Load healthy reference values
    with open("section2_Bioknowledge/utils/health_ranges.json", "r") as f:
        health_ranges = json.load(f)

    print(f"\n🩺 Health Analysis for {city}:\n")

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Rename according to your dataset columns
    df = df.rename(columns={
        "avg_bp_sys": "blood_pressure_sys",
        "avg_bp_dia": "blood_pressure_dia",
        "avg_heart_rate": "heart_rate",
        "avg_oxygen_level": "oxygen_level"
    })

    report_rows = []

    for _, row in df.iterrows():
        heart_rate = row["heart_rate"]
        sys = row["blood_pressure_sys"]
        dia = row["blood_pressure_dia"]
        o2 = row["oxygen_level"]

        checks = {
            "heart_rate": (heart_rate, health_ranges["heart_rate"]),
            "blood_pressure_systolic": (sys, health_ranges["blood_pressure_systolic"]),
            "blood_pressure_diastolic": (dia, health_ranges["blood_pressure_diastolic"]),
            "oxygen_level": (o2, health_ranges["oxygen_level"])
        }

        summary = {"city": city}

        for key, (value, ref) in checks.items():
            healthy_min, healthy_max = ref["healthy_min"], ref["healthy_max"]
            if value < healthy_min:
                status = "LOW"
            elif value > healthy_max:
                status = "HIGH"
            else:
                status = "NORMAL"
            summary[key] = f"{round(value, 2)} ({status})"

        report_rows.append(summary)

    # Create dataframe from summaries
    result_df = pd.DataFrame(report_rows)

    # ✅ 1️⃣ Show the summary clearly in terminal
    print(result_df.to_string(index=False))

    # ✅ 2️⃣ Save the same data to CSV report
    os.makedirs("section2_Bioknowledge/reports", exist_ok=True)
    output_path = f"section2_Bioknowledge/reports/{city}_health_summary.csv"
    result_df.to_csv(output_path, index=False)
    print(f"\n📄 Summary saved at: {output_path}")

    # ✅ 3️⃣ Visualization section
    avg_values = df[["heart_rate", "blood_pressure_sys", "blood_pressure_dia", "oxygen_level"]].mean()
    healthy_means = [
        health_ranges["heart_rate"]["healthy_max"],
        health_ranges["blood_pressure_systolic"]["healthy_max"],
        health_ranges["blood_pressure_diastolic"]["healthy_max"],
        health_ranges["oxygen_level"]["healthy_max"]
    ] 

    plt.figure(figsize=(7, 5))
    plt.bar(avg_values.index, avg_values.values, alpha=0.7, label=f"{city.capitalize()} Avg")
    plt.plot(avg_values.index, healthy_means, "r--", label="Healthy Limit")
    plt.title(f"Average Bioknowledge vs Healthy Standards ({city.capitalize()})")
    plt.ylabel("Values")
    plt.legend()
    plt.tight_layout()
    plt.show()
