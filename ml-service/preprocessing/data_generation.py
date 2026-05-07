# =============================================================================
# STUDENT PERFORMANCE — SYNTHETIC DATA GENERATOR v3.0
# BuildCare GEC | Gujarat Technological University
#
# FINAL AGREED FEATURES (12 input + 1 target):
#   1.  semesters_completed       — 0 (Sem-1) to 7
#   2.  cpi                       — GTU CPI; for Sem-1: 12th % scaled via (pct/10)+0.5
#   3.  internal_marks_percentage — internal assessment standardised to 0-100
#   4.  attendance_percentage     — 40-100 (GTU bars below 40%)
#   5.  total_backlogs            — 0-8; -1 for Sem-1 students (sentinel: not applicable)
#   6.  study_hours_weekly        — 3-40
#   7.  pyq_solving_frequency     — 0-5 (times/week)
#   8.  sleep_category            — <6 / 6-8 / >8
#   9.  gaming_hours_weekly       — 0-20
#   10. extra_curricular_level    — Low / Medium / High
#   11. travel_time_category      — <30 / 30-60 / >60 (mins one-way)
#   12. department                — CE / IT / EC / ME / ICT / EE
#
# DESIGN DECISIONS (document for professor):
#   - All features are realistically correlated via a hidden "ability" variable
#   - Sem-1 students: backlogs=-1 (sentinel), cpi derived from 12th percentage
#   - internal_marks_percentage standardised so branch differences don't bias model
#   - travel_time retained — real-world factor; model learns its effect from data
#   - Removed: assignment_delay_count (no denominator context), library_visits,
#               lab_hours (curriculum-mandated not behaviour), peer_study_group
#   - 50,000 rows for robust training (70% train / 10% val / 20% test)
# =============================================================================

import numpy as np
import pandas as pd

np.random.seed(42)
N = 50_000

print(f"Generating {N:,} synthetic student records...")
print("=" * 60)

# ── HIDDEN ABILITY VARIABLE ────────────────────────────────────────────────
# Represents each student's underlying academic capability + dedication.
# This single variable drives realistic correlation across all features.
# Real students are not random — a hardworking student shows it across
# multiple dimensions simultaneously.
ability = np.random.normal(loc=0, scale=1, size=N)  # standard normal


# ── FEATURE 1: semesters_completed ────────────────────────────────────────
# GTU BE = 8 semesters. semesters_completed = how many are DONE.
# Sem-1 student currently IN sem-1 → semesters_completed = 0
# Distribute realistically: more students in middle semesters
sem_weights = [0.10, 0.11, 0.13, 0.14, 0.14, 0.13, 0.13, 0.12]  # sums to 1.0
semesters_completed = np.random.choice(range(8), size=N, p=sem_weights)


# ── FEATURE 2: cpi ────────────────────────────────────────────────────────
# For semesters_completed > 0: GTU CPI (credit-weighted avg of all SPIs)
# For semesters_completed == 0 (Sem-1): 12th percentage scaled via (pct/10)+0.5
#
# CPI distribution: normal around 6.5, std 1.2 (real GTU batch)
# Higher ability → higher CPI. Noise added for realism.
# CPI also gets more stable (less noisy) as semesters increase.

cpi_values = np.zeros(N)

sem1_mask = (semesters_completed == 0)
sem_plus_mask = ~sem1_mask

# Sem-1 students: scale from 12th percentage
# 12th percentage: normal around 70%, std 12% for engineering students
twelfth_pct = np.clip(
    np.random.normal(loc=70, scale=12, size=N),
    45.0, 99.0  # realistic 12th range for GTU engineering admissions
)
# GTU official formula: CPI = (percentage / 10) + 0.5
cpi_from_12th = np.clip(np.round((twelfth_pct / 10) + 0.5, 2), 1.0, 10.0)
cpi_values[sem1_mask] = cpi_from_12th[sem1_mask]

# Sem 2+ students: real GTU CPI
# Noise decreases as semesters increase (CPI stabilises over time)
stability = np.clip(semesters_completed / 7.0, 0.1, 1.0)  # 0.1 for sem1, 1.0 for sem7
noise_scale = 0.8 * (1 - stability * 0.6)  # more noise early, less later

cpi_raw = 6.5 + ability * 1.2 + np.random.normal(0, noise_scale, N)
cpi_real = np.clip(np.round(cpi_raw, 2), 1.0, 10.0)
cpi_values[sem_plus_mask] = cpi_real[sem_plus_mask]


# ── FEATURE 3: internal_marks_percentage ──────────────────────────────────
# Standardised to 0-100 regardless of branch (some have /20, some /30)
# Strongly correlated with CPI and ability.
# Internal marks: 70% of marks from exams + 30% internal in GTU
internal_raw = 60 + ability * 12 + np.random.normal(0, 8, N)
internal_marks_percentage = np.clip(np.round(internal_raw, 1), 20.0, 100.0)


# ── FEATURE 4: attendance_percentage ──────────────────────────────────────
# GTU minimum: 75% required, bars from exam if below.
# We set floor at 40% (some students still attend despite being at risk).
# Strong positive correlation with ability.
att_raw = 75 + ability * 8 + np.random.normal(0, 7, N)
attendance_percentage = np.clip(np.round(att_raw, 1), 40.0, 100.0)


# ── FEATURE 5: total_backlogs ─────────────────────────────────────────────
# SENTINEL VALUE: -1 for Sem-1 students (backlogs not applicable yet)
# For Sem 2+: Poisson distribution, inversely correlated with ability
# Higher ability → fewer backlogs. Mean backlog count decreases with ability.

total_backlogs = np.full(N, -1, dtype=int)  # default -1 (Sem-1 sentinel)

# For Sem 2+ students, compute actual backlogs
backlog_mean = np.clip(2.5 - ability * 1.8, 0.05, 7.0)
backlogs_real = np.array([
    np.random.poisson(lam) for lam in backlog_mean
]).clip(0, 8)

total_backlogs[sem_plus_mask] = backlogs_real[sem_plus_mask]

# Consistency check: very high CPI students shouldn't have many backlogs
# (CPI > 8.5 → max 1 backlog realistically)
high_cpi_mask = sem_plus_mask & (cpi_values > 8.5)
total_backlogs[high_cpi_mask] = np.minimum(total_backlogs[high_cpi_mask], 1)


# ── FEATURE 6: study_hours_weekly ─────────────────────────────────────────
# Positive correlation with ability. Range: 3–40 hrs/week.
# Average engineering student: ~15 hrs/week outside class.
study_raw = 15 + ability * 5 + np.random.normal(0, 4, N)
study_hours_weekly = np.clip(np.round(study_raw, 1), 3.0, 40.0)


# ── FEATURE 7: pyq_solving_frequency ──────────────────────────────────────
# Times per week student solves previous year question papers (0–5).
# Good exam strategy indicator — correlated with ability and study hours.
pyq_raw = 2.0 + ability * 1.2 + np.random.normal(0, 0.8, N)
pyq_solving_frequency = np.clip(np.round(pyq_raw).astype(int), 0, 5)


# ── FEATURE 8: sleep_category ─────────────────────────────────────────────
# <6 hrs: sleep-deprived (common in stressed/low-performing students)
# 6-8 hrs: optimal for learning and memory consolidation
# >8 hrs: oversleeping (sometimes indicates low motivation or depression)
# Probabilities shift with ability level.
sleep_options = ["<6", "6-8", ">8"]

# Base probabilities shift with ability
p_less6  = np.clip(0.35 - ability * 0.08, 0.05, 0.65)
p_gt8    = np.clip(0.15 - ability * 0.04, 0.03, 0.35)
p_6to8   = np.clip(1.0 - p_less6 - p_gt8, 0.10, 0.85)

# Renormalise rows to sum to 1
total_p = p_less6 + p_6to8 + p_gt8
p_less6 /= total_p
p_6to8  /= total_p
p_gt8   /= total_p

sleep_category = np.array([
    np.random.choice(sleep_options, p=[pl, p6, pg])
    for pl, p6, pg in zip(p_less6, p_6to8, p_gt8)
])


# ── FEATURE 9: gaming_hours_weekly ────────────────────────────────────────
# Negatively correlated with study hours and ability.
# Realistic cap at 20 hrs/week (≈ 2.8 hrs/day — heavy but possible).
gaming_raw = 8 - ability * 3 + np.random.normal(0, 3, N)
gaming_hours_weekly = np.clip(np.round(gaming_raw, 1), 0.0, 20.0)


# ── FEATURE 10: extra_curricular_level ────────────────────────────────────
# Low / Medium / High involvement in sports, clubs, events.
# Medium is healthy (time management). High can hurt academics.
# Weakly correlated — many toppers are highly involved in extra-curriculars.
extra_curricular_level = np.random.choice(
    ["Low", "Medium", "High"],
    size=N,
    p=[0.35, 0.45, 0.20]
)


# ── FEATURE 11: travel_time_category ──────────────────────────────────────
# One-way commute time. Retained as a real-world contextual factor.
# Long commute (>60 min) = 2+ hrs/day lost — affects study time and fatigue.
# Effect is indirect: let the model learn it from data correlations.
# Slight tendency: higher-ability students may live closer (hostels near college)
# but this is weak — we keep it mostly random.
travel_options = ["<30", "30-60", ">60"]
travel_time_category = np.random.choice(
    travel_options,
    size=N,
    p=[0.40, 0.40, 0.20]
)


# ── FEATURE 12: department ────────────────────────────────────────────────
# No performance bias assumed across departments.
# Department context helps model understand curriculum differences.
department = np.random.choice(
    ["CE", "IT", "EC", "ME", "ICT", "EE"],
    size=N
)


# ── ASSEMBLE DATAFRAME ────────────────────────────────────────────────────
df = pd.DataFrame({
    "semesters_completed":      semesters_completed,
    "cpi":                      cpi_values,
    "internal_marks_percentage": internal_marks_percentage,
    "attendance_percentage":    attendance_percentage,
    "total_backlogs":           total_backlogs,
    "study_hours_weekly":       study_hours_weekly,
    "pyq_solving_frequency":    pyq_solving_frequency,
    "sleep_category":           sleep_category,
    "gaming_hours_weekly":      gaming_hours_weekly,
    "extra_curricular_level":   extra_curricular_level,
    "travel_time_category":     travel_time_category,
    "department":               department,
})


# ── SANITY CHECKS ─────────────────────────────────────────────────────────
print("\n── Semester distribution ──")
sem_dist = df["semesters_completed"].value_counts().sort_index()
for sem, count in sem_dist.items():
    label = f"Sem-{sem+1}" if sem < 7 else "Sem-8"
    completed_label = f"({sem} completed)"
    bar = "█" * (count // 400)
    print(f"  {label} {completed_label:<18} {count:>5} students  {bar}")

print(f"\n── Sem-1 students (semesters_completed=0) ──")
sem1_df = df[df["semesters_completed"] == 0]
print(f"  Count:              {len(sem1_df):,}")
print(f"  All backlogs = -1:  {(sem1_df['total_backlogs'] == -1).all()}")
print(f"  CPI range:          {sem1_df['cpi'].min():.2f} – {sem1_df['cpi'].max():.2f}  (from 12th %)")
print(f"  CPI mean:           {sem1_df['cpi'].mean():.2f}")

print(f"\n── Correlation check (Sem 2+ students only) ──")
sem_plus_df = df[df["semesters_completed"] > 0]
print(f"  CPI ↔ Attendance:         {sem_plus_df['cpi'].corr(sem_plus_df['attendance_percentage']):.2f}  (expect +0.5 to +0.7)")
print(f"  CPI ↔ Backlogs:           {sem_plus_df['cpi'].corr(sem_plus_df['total_backlogs']):.2f}  (expect -0.5 to -0.7)")
print(f"  CPI ↔ Internal marks:     {sem_plus_df['cpi'].corr(sem_plus_df['internal_marks_percentage']):.2f}  (expect +0.6 to +0.8)")
print(f"  CPI ↔ Study hours:        {sem_plus_df['cpi'].corr(sem_plus_df['study_hours_weekly']):.2f}  (expect +0.4 to +0.6)")
print(f"  Study ↔ Gaming:           {sem_plus_df['study_hours_weekly'].corr(sem_plus_df['gaming_hours_weekly']):.2f}  (expect -0.3 to -0.5)")

print(f"\n── Feature ranges (full dataset) ──")
print(f"  CPI:                      {df['cpi'].min():.2f} – {df['cpi'].max():.2f}  (mean={df['cpi'].mean():.2f})")
print(f"  Internal marks %:         {df['internal_marks_percentage'].min():.1f} – {df['internal_marks_percentage'].max():.1f}")
print(f"  Attendance %:             {df['attendance_percentage'].min():.1f} – {df['attendance_percentage'].max():.1f}")
print(f"  Total backlogs:           {df['total_backlogs'].min()} (sentinel) – {df['total_backlogs'].max()}")
print(f"  Study hrs/week:           {df['study_hours_weekly'].min():.1f} – {df['study_hours_weekly'].max():.1f}")
print(f"  Gaming hrs/week:          {df['gaming_hours_weekly'].min():.1f} – {df['gaming_hours_weekly'].max():.1f}")

print(f"\n── Categorical distributions ──")
print(f"  Sleep: {dict(pd.Series(sleep_category).value_counts(normalize=True).round(2))}")
print(f"  Extra: {dict(pd.Series(extra_curricular_level).value_counts(normalize=True).round(2))}")
print(f"  Travel:{dict(pd.Series(travel_time_category).value_counts(normalize=True).round(2))}")
print(f"  Dept:  {dict(pd.Series(department).value_counts(normalize=True).round(2))}")

# ── SAVE ──────────────────────────────────────────────────────────────────
output_path = "../data/student_performance_raw.csv"
df.to_csv(output_path, index=False)

print(f"\n{'='*60}")
print(f"✓ Data saved → {output_path}")
print(f"  Rows: {len(df):,}  |  Columns: {len(df.columns)}")
print(f"  Next step: Open EDA.ipynb and explore the data")
print(f"  Then run target_labelling.py to compute PS and labels")
print(f"{'='*60}")
