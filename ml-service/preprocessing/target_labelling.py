# =============================================================================
# STUDENT PERFORMANCE — TARGET LABELLING v3.0
# BuildCare GEC | Gujarat Technological University
#
# WHAT THIS SCRIPT DOES:
#   1. Loads raw synthetic data (student_performance_raw.csv)
#   2. Encodes categorical features for PS calculation
#   3. Normalises numeric features (MinMaxScaler)
#   4. Computes Performance Score (PS) via weighted formula
#   5. Assigns 5-class labels based on PS thresholds
#   6. Saves final labelled dataset + scaler artifact
#
# PS FORMULA WEIGHTS (agreed):
#   cpi                      +0.30   (strongest predictor)
#   attendance_percentage    +0.20
#   internal_marks_pct       +0.15
#   total_backlogs           -0.15   (sentinel -1 → 0 contribution, Option A)
#   study_hours_weekly       +0.10
#   pyq_solving_frequency    +0.08
#   gaming_hours_weekly      -0.05
#   sleep_category           +0.04   (encoded: <6→0.30, 6-8→1.00, >8→0.65)
#   extra_curricular_level   +0.03   (encoded: Low→0.30, Medium→1.00, High→0.60)
#   travel_time_category     -0.03   (encoded: <30→0.00, 30-60→0.50, >60→1.00)
#   semesters_completed      0.00    (context only, not a performance driver)
#   department               0.00    (no performance bias assumed)
#
# 5-CLASS THRESHOLDS (confirmed):
#   0  – 28  → At Risk
#   28 – 45  → Below Average
#   45 – 63  → Average
#   63 – 80  → Good
#   80 – 100 → Excellent
# =============================================================================

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

# ── PATHS ─────────────────────────────────────────────────────────────────
INPUT_PATH  = "../data/student_performance_raw.csv"
OUTPUT_PATH = "../data/student_performance_labelled.csv"
SCALER_PATH = "../models/scaler.joblib"

os.makedirs("../models", exist_ok=True)

# ── LOAD ──────────────────────────────────────────────────────────────────
print("Loading raw data...")
df = pd.read_csv(INPUT_PATH)
print(f"  Shape: {df.shape}")
print(f"  Columns: {list(df.columns)}")


# ── STEP 1: ENCODE CATEGORICAL FEATURES ───────────────────────────────────
print("\nEncoding categorical features...")

# Sleep: 6-8 hrs is cognitively optimal
sleep_map = {
    "<6":  0.30,   # sleep-deprived → poor retention
    "6-8": 1.00,   # optimal
    ">8":  0.65,   # oversleeping → low motivation but rested
}

# Extra-curricular: Medium is best (balance), High can hurt study time
extra_map = {
    "Low":    0.30,   # not engaged
    "Medium": 1.00,   # ideal time management
    "High":   0.60,   # passionate but study time may suffer
}

# Travel: longer commute = more time lost daily
# Used as penalty — higher travel → higher encoded value → bigger negative hit
travel_map = {
    "<30":   0.00,   # no meaningful impact
    "30-60": 0.50,   # moderate impact
    ">60":   1.00,   # 2+ hrs/day lost
}

df["sleep_encoded"]  = df["sleep_category"].map(sleep_map)
df["extra_encoded"]  = df["extra_curricular_level"].map(extra_map)
df["travel_encoded"] = df["travel_time_category"].map(travel_map)

print(f"  sleep_encoded  — unique values: {sorted(df['sleep_encoded'].unique())}")
print(f"  extra_encoded  — unique values: {sorted(df['extra_encoded'].unique())}")
print(f"  travel_encoded — unique values: {sorted(df['travel_encoded'].unique())}")


# ── STEP 2: HANDLE SENTINEL VALUE FOR BACKLOGS ────────────────────────────
# Sem-1 students have total_backlogs = -1 (not applicable yet).
# Option A: treat as 0 contribution to PS — neutral, no penalty, no bonus.
# We create a separate column for PS calculation only.
print("\nHandling Sem-1 sentinel (backlogs=-1 → 0 contribution)...")

df["backlogs_for_ps"] = df["total_backlogs"].copy()
df.loc[df["total_backlogs"] == -1, "backlogs_for_ps"] = 0

sem1_count = (df["total_backlogs"] == -1).sum()
print(f"  Sem-1 students with sentinel: {sem1_count:,}")
print(f"  Their backlogs_for_ps set to: 0 (neutral contribution)")


# ── STEP 3: NORMALISE NUMERIC FEATURES ────────────────────────────────────
# MinMaxScaler maps each feature to [0, 1].
# This makes weights comparable across features with different scales.
# Important: backlogs_for_ps used here (not raw total_backlogs with -1).
print("\nNormalising numeric features...")

NUMERIC_COLS = [
    "cpi",
    "internal_marks_percentage",
    "attendance_percentage",
    "backlogs_for_ps",
    "study_hours_weekly",
    "pyq_solving_frequency",
    "gaming_hours_weekly",
]

scaler = MinMaxScaler()
df_scaled = pd.DataFrame(
    scaler.fit_transform(df[NUMERIC_COLS]),
    columns=NUMERIC_COLS,
    index=df.index
)

print(f"  Scaled columns: {NUMERIC_COLS}")
print(f"  All values in [0,1]: {((df_scaled >= 0) & (df_scaled <= 1)).all().all()}")


# ── STEP 4: COMPUTE PERFORMANCE SCORE (PS) ────────────────────────────────
# Weights agreed:
#   Positive: cpi(0.30) + attendance(0.20) + internal(0.15) +
#             study(0.10) + pyq(0.08) + sleep(0.04) + extra(0.03)
#   Negative: backlogs(-0.15) + gaming(-0.05) + travel(-0.03)
#
# Note: sleep, extra, travel are already in [0,1] from manual encoding
#       so they don't go through MinMaxScaler — weights apply directly.
#
# Note: semesters_completed and department have weight 0 — excluded.

print("\nComputing Performance Score (PS)...")

WEIGHTS = {
    # Positive contributors
    "cpi":                    +0.30,
    "attendance_percentage":  +0.20,
    "internal_marks_percentage": +0.15,
    "study_hours_weekly":     +0.10,
    "pyq_solving_frequency":  +0.08,
    "sleep_encoded":          +0.04,
    "extra_encoded":          +0.03,

    # Negative contributors
    "backlogs_for_ps":        -0.15,
    "gaming_hours_weekly":    -0.05,
    "travel_encoded":         -0.03,
}

ps_raw = (
    df_scaled["cpi"]                        * WEIGHTS["cpi"] +
    df_scaled["attendance_percentage"]       * WEIGHTS["attendance_percentage"] +
    df_scaled["internal_marks_percentage"]   * WEIGHTS["internal_marks_percentage"] +
    df_scaled["study_hours_weekly"]          * WEIGHTS["study_hours_weekly"] +
    df_scaled["pyq_solving_frequency"]       * WEIGHTS["pyq_solving_frequency"] +
    df["sleep_encoded"]                      * WEIGHTS["sleep_encoded"] +
    df["extra_encoded"]                      * WEIGHTS["extra_encoded"] +
    df_scaled["backlogs_for_ps"]             * WEIGHTS["backlogs_for_ps"] +
    df_scaled["gaming_hours_weekly"]         * WEIGHTS["gaming_hours_weekly"] +
    df["travel_encoded"]                     * WEIGHTS["travel_encoded"]
)

# Scale PS to 0–100
ps_min, ps_max = ps_raw.min(), ps_raw.max()
df["performance_score"] = ((ps_raw - ps_min) / (ps_max - ps_min) * 100).round(2)

print(f"  PS raw range:    {ps_min:.4f} – {ps_max:.4f}")
print(f"  PS scaled range: {df['performance_score'].min():.2f} – {df['performance_score'].max():.2f}")
print(f"  PS mean:         {df['performance_score'].mean():.2f}")
print(f"  PS std:          {df['performance_score'].std():.2f}")


# ── STEP 5: ASSIGN 5-CLASS LABELS ─────────────────────────────────────────
# Thresholds calibrated to actual PS distribution (percentile-based):
#   0  – 36  → At Risk        (~10%)
#   36 – 43  → Below Average  (~10%)
#   43 – 59  → Average        (~35%)
#   59 – 76  → Good           (~25%)
#   76 – 100 → Excellent      (~10%)
# Note: thresholds derived from actual PS percentiles (mean=56.4, std=15.2)

print("\nAssigning performance labels...")

def assign_label(ps):
    if ps < 36:   return "At Risk"
    elif ps < 43: return "Below Average"
    elif ps < 59: return "Average"
    elif ps < 76: return "Good"
    else:         return "Excellent"

df["performance_category"] = df["performance_score"].apply(assign_label)

# ── STEP 6: DISTRIBUTION REPORT ───────────────────────────────────────────
CLASS_ORDER = ["At Risk", "Below Average", "Average", "Good", "Excellent"]

print("\n── Class Distribution ──────────────────────────────────")
dist = df["performance_category"].value_counts()
dist_pct = df["performance_category"].value_counts(normalize=True) * 100

for cat in CLASS_ORDER:
    count = dist.get(cat, 0)
    pct   = dist_pct.get(cat, 0)
    bar   = "█" * int(pct / 1.5)
    print(f"  {cat:<15} {count:>6,} students  ({pct:5.1f}%)  {bar}")

print(f"\n  Total: {len(df):,} students")

# Per-semester class breakdown (useful for EDA)
print("\n── PS mean by semester ─────────────────────────────────")
sem_ps = df.groupby("semesters_completed")["performance_score"].mean().round(2)
for sem, mean_ps in sem_ps.items():
    label = f"Sem-{sem+1} ({sem} completed)"
    print(f"  {label:<28} mean PS = {mean_ps:.2f}")


# ── STEP 7: CLEAN UP & SAVE ───────────────────────────────────────────────
# Drop helper columns used only for PS calculation
df_final = df.drop(columns=["sleep_encoded", "extra_encoded",
                             "travel_encoded", "backlogs_for_ps"])

# Column order: features → ps → label
FINAL_COLS = [
    "semesters_completed",
    "cpi",
    "internal_marks_percentage",
    "attendance_percentage",
    "total_backlogs",
    "study_hours_weekly",
    "pyq_solving_frequency",
    "sleep_category",
    "gaming_hours_weekly",
    "extra_curricular_level",
    "travel_time_category",
    "department",
    "performance_score",
    "performance_category",
]
df_final = df_final[FINAL_COLS]

df_final.to_csv(OUTPUT_PATH, index=False)
print(f"\n✓ Labelled data saved → {OUTPUT_PATH}")
print(f"  Rows: {len(df_final):,}  |  Columns: {len(df_final.columns)}")

joblib.dump(scaler, SCALER_PATH)
print(f"✓ Scaler saved       → {SCALER_PATH}")

print("\n" + "=" * 60)
print("Next step: run model_training.py")
print("  — 70% train / 10% validation / 20% test")
print("  — XGBoost vs LightGBM comparison")
print("=" * 60)
