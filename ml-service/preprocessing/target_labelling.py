# ========================================== WARNING! ======================================== #
# Run data_generation.py once, then run this file. Also check for data loading and saving path
# ============================================================================================ #

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib


path = "../data/student_performance_data_synthetic.csv"
df = pd.read_csv(path)


# ---------- STEP 1: Encode ordinal / categorical features for PS ----------
sleep_map = {"<6": 0.3, "6-8": 1.0, ">8": 0.8}
travel_map = {"<30": 1.0, "30-60": 0.7, ">60": 0.4}
extra_map = {"Low": 0.3, "Medium": 0.7, "High": 1.0}

df["sleep_score"] = df["sleep_category"].map(sleep_map)
df["travel_score"] = df["travel_time_category"].map(travel_map)
df["extra_score"] = df["extra_curricular_level"].map(extra_map)


# ---------- STEP 2: Normalize numeric features ----------
numeric_cols = [
    "last_sem_spi",
    "internal_assessment_avg",
    "attendance_percentage",
    "total_backlogs",
    "pyq_solving_frequency",
    "study_hours_weekly",
    "gaming_hours_weekly",
    "assignment_delay_count"
]

scaler = MinMaxScaler()
df_scaled = pd.DataFrame(
    scaler.fit_transform(df[numeric_cols]),
    columns=numeric_cols
)


# ---------- STEP 3: Define PS formula ----------
weights = {
    "last_sem_spi": 0.25,
    "internal_assessment_avg": 0.20,
    "attendance_percentage": 0.15,
    "total_backlogs": -0.15,
    "pyq_solving_frequency": 0.10,
    "study_hours_weekly": 0.10,
    "sleep_score": 0.05,
    "assignment_delay_count": -0.10,
    "gaming_hours_weekly": -0.05,
    "travel_score": -0.03,
    "extra_score": 0.03
}

df["ps"] = (
    df_scaled["last_sem_spi"] * weights["last_sem_spi"] +
    df_scaled["internal_assessment_avg"] * weights["internal_assessment_avg"] +
    df_scaled["attendance_percentage"] * weights["attendance_percentage"] +
    df_scaled["total_backlogs"] * weights["total_backlogs"] +
    df_scaled["pyq_solving_frequency"] * weights["pyq_solving_frequency"] +
    df_scaled["study_hours_weekly"] * weights["study_hours_weekly"] +
    df["sleep_score"] * weights["sleep_score"] +
    df_scaled["assignment_delay_count"] * weights["assignment_delay_count"] +
    df_scaled["gaming_hours_weekly"] * weights["gaming_hours_weekly"] +
    df["travel_score"] * weights["travel_score"] +
    df["extra_score"] * weights["extra_score"]
)

df["ps"] = (df["ps"] - df["ps"].min()) / (df["ps"].max() - df["ps"].min()) * 100
df["ps"] = df["ps"].round(2)


# ---------- STEP 4: Generate labels ----------
def label_ps(ps):
    if ps < 40:
        return "At Risk"
    elif ps < 70:
        return "Average"
    return "Good"


df["performance_category"] = df["ps"].apply(label_ps)
print("Labels generated and added to data")

# Saving the final dataset
final_path = "../data/student_performance_with_PS_and_labels.csv"
df.to_csv(final_path, index=False)
print(f"Data saved to {final_path}")

scaler_path = "../models/scaler.joblib"
joblib.dump(scaler, scaler_path)
print(f"Scaler saved to {scaler_path}")
