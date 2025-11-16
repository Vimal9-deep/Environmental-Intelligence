# section3_LE/scripts3/fetch_life_expectancy.py
#Purpose: Finds the state of the entered region (from health dataset) and fetches its base life expectancy.

# section3_LE/scripts3/fetch_life_expectancy.py

import pandas as pd
import os

HEALTH_FILE = "section2_Bioknowledge/data/health_dataset_expanded.csv"
STATEWISE_LE_FILE = "section3_LE/data/state_life_expectancy_2017_21_india.csv"


def get_state_from_city(city_name):
    """Return the state to which the city belongs (case & space insensitive)."""
    if not os.path.exists(HEALTH_FILE):
        raise FileNotFoundError(f"❌ Health dataset not found at {HEALTH_FILE}")

    df = pd.read_csv(HEALTH_FILE)

    # Normalize text — lowercase, strip spaces
    df["city"] = df["city"].astype(str).str.strip().str.lower()
    df["state"] = df["state"].astype(str).str.strip()

    # Normalize input too
    city_name = city_name.strip().lower()

    match = df[df["city"] == city_name]

    if match.empty:
        print(f"⚠️ No state found for city '{city_name}'. Please check the spelling in dataset.")
        print("📘 Tip: Ensure your 'city' column in health_dataset_expanded.csv contains this name.")
        return None

    state_name = match.iloc[0]["state"]
    print(f" City '{city_name.title()}' belongs to state '{state_name}'.")
    return state_name


def get_base_life_expectancy(state_name):
    """Fetch base life expectancy of the state from dataset."""
    if not os.path.exists(STATEWISE_LE_FILE):
        raise FileNotFoundError(f"❌ Statewise LE dataset not found at {STATEWISE_LE_FILE}")

    df = pd.read_csv(STATEWISE_LE_FILE)

    # Normalize column names (make them lowercase)
    df.columns = df.columns.str.strip().str.lower()

    # Standardize the column name that may be 'state' or 'State'
    if "state" not in df.columns: 
        raise KeyError("❌ 'state' column not found in life expectancy dataset. Please check your CSV headers.")

    # Normalize text values
    df["state"] = df["state"].astype(str).str.strip().str.lower()
    state_name = state_name.strip().lower()

    rec = df[df["state"] == state_name]
    if rec.empty:
        print(f"⚠️ No life expectancy record found for '{state_name}'.")
        return None

    # Choose which column to use — 'Total' if available, else average of Male/Female
    if "total" in df.columns:
        return float(rec.iloc[0]["total"])
    elif "total_male" in df.columns and "total_female" in df.columns:
        return float((rec.iloc[0]["total_male"] + rec.iloc[0]["total_female"]) / 2)
    else:
        raise KeyError("⚠️ No valid life expectancy value column found (Expected 'Total' or gender-based columns).")




