# =============================================================================
# STUDENT PERFORMANCE — MODEL TRAINING v3.0
# BuildCare GEC | Gujarat Technological University
#
# PIPELINE:
#   1. Load labelled data
#   2. Encode features (differently for XGB vs LGBM)
#   3. Split: 70% train / 10% validation / 20% test
#   4. Tune XGBoost with Optuna (50 trials) on validation set
#   5. Tune LightGBM with Optuna (50 trials) on validation set
#   6. Evaluate both on TEST set (untouched until this point)
#   7. Compare: accuracy, weighted F1, per-class F1, training time
#   8. SHAP feature importance for both models
#   9. Save the better model + all artifacts
# =============================================================================

import time
import warnings
import numpy as np
import pandas as pd
import joblib
import shap
import optuna
import matplotlib
matplotlib.use("Agg")   # non-interactive backend for saving plots
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, f1_score,
    classification_report, confusion_matrix,
    ConfusionMatrixDisplay
)
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

optuna.logging.set_verbosity(optuna.logging.WARNING)
warnings.filterwarnings("ignore")

# ── PATHS ─────────────────────────────────────────────────────────────────
DATA_PATH    = "../data/student_performance_labelled.csv"
MODELS_DIR   = "../models/"
REPORTS_DIR  = "../reports/"

import os
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# ── CLASS ORDER (fixed — always use this order) ───────────────────────────
CLASS_ORDER = ["At Risk", "Below Average", "Average", "Good", "Excellent"]

print("=" * 65)
print("  STUDENT PERFORMANCE PREDICTION — MODEL TRAINING")
print("=" * 65)

# =============================================================================
# STEP 1: LOAD DATA
# =============================================================================
print("\n[1/9] Loading data...")
df = pd.read_csv(DATA_PATH)
print(f"  Shape: {df.shape}")
print(f"  Class distribution:")
dist = df["performance_category"].value_counts()
for cls in CLASS_ORDER:
    print(f"    {cls:<15} {dist.get(cls, 0):>6,}")


# =============================================================================
# STEP 2: ENCODE TARGET
# =============================================================================
print("\n[2/9] Encoding target...")

le_target = LabelEncoder()
le_target.fit(CLASS_ORDER)
y = le_target.transform(df["performance_category"])

print(f"  Class → integer mapping:")
for cls, idx in zip(le_target.classes_.tolist(), le_target.transform(le_target.classes_).tolist()):
    print(f"    {cls:<15} → {idx}")


# =============================================================================
# STEP 3: FEATURE ENCODING
# =============================================================================
print("\n[3/9] Encoding features...")

# ── Categorical columns ────────────────────────────────────────────────────
CAT_COLS = [
    "sleep_category",
    "extra_curricular_level",
    "travel_time_category",
    "department",
]

# ── Numeric columns (already scaled in target_labelling via MinMaxScaler
#    but we re-scale here on train split only to avoid data leakage) ────────
NUM_COLS = [
    "semesters_completed",
    "cpi",
    "internal_marks_percentage",
    "attendance_percentage",
    "total_backlogs",        # includes -1 sentinel for Sem-1
    "study_hours_weekly",
    "pyq_solving_frequency",
    "gaming_hours_weekly",
]

FEATURE_COLS = NUM_COLS + CAT_COLS

# ── XGBoost encoding: label-encode all categoricals ───────────────────────
df_xgb = df[FEATURE_COLS].copy()
le_encoders: dict[str, LabelEncoder] = {}
for col in CAT_COLS:
    le = LabelEncoder()
    df_xgb[col] = le.fit_transform(df_xgb[col])
    le_encoders[col] = le
    print(f"  XGB label-encoded '{col}': {dict(zip(le.classes_, le.transform(le.classes_)))}")

# ── LightGBM encoding: cast categoricals to pandas Categorical dtype ───────
df_lgbm = df[FEATURE_COLS].copy()
for col in CAT_COLS:
    df_lgbm[col] = pd.Categorical(df_lgbm[col])
print(f"  LGBM: categoricals set to pd.Categorical dtype (native handling)")


# =============================================================================
# STEP 4: TRAIN / VALIDATION / TEST SPLIT  (70 / 10 / 20)
# =============================================================================
print("\n[4/9] Splitting data (70% train / 10% val / 20% test)...")

# First split off 20% test
X_xgb_trainval, X_xgb_test, \
X_lgbm_trainval, X_lgbm_test, \
y_trainval, y_test = train_test_split(
    df_xgb, df_lgbm, y,
    test_size=0.20, random_state=42, stratify=y
)

# Then split remaining 80% into 70% train + 10% val
# 10% of total = 10/80 = 0.125 of trainval
X_xgb_train, X_xgb_val, \
X_lgbm_train, X_lgbm_val, \
y_train, y_val = train_test_split(
    X_xgb_trainval, X_lgbm_trainval, y_trainval,
    test_size=0.125, random_state=42, stratify=y_trainval
)

print(f"  Train : {len(y_train):>6,} rows  ({len(y_train)/len(y)*100:.1f}%)")
print(f"  Val   : {len(y_val):>6,} rows  ({len(y_val)/len(y)*100:.1f}%)")
print(f"  Test  : {len(y_test):>6,} rows  ({len(y_test)/len(y)*100:.1f}%)")
print(f"  ⚠️  Test set is LOCKED — not touched until final evaluation")

# ── Scale numeric features (fit on train only — no leakage) ───────────────
print("\n  Scaling numeric features (fit on train only)...")
scaler = MinMaxScaler()

# .copy() prevents SettingWithCopyWarning and Pylance slice-assignment errors
X_xgb_train  = X_xgb_train.copy()
X_xgb_val    = X_xgb_val.copy()
X_xgb_test   = X_xgb_test.copy()
X_lgbm_train = X_lgbm_train.copy()
X_lgbm_val   = X_lgbm_val.copy()
X_lgbm_test  = X_lgbm_test.copy()

X_xgb_train[NUM_COLS]  = pd.DataFrame(scaler.fit_transform(X_xgb_train[NUM_COLS]),  columns=NUM_COLS, index=X_xgb_train.index)
X_xgb_val[NUM_COLS]    = pd.DataFrame(scaler.transform(X_xgb_val[NUM_COLS]),        columns=NUM_COLS, index=X_xgb_val.index)
X_xgb_test[NUM_COLS]   = pd.DataFrame(scaler.transform(X_xgb_test[NUM_COLS]),       columns=NUM_COLS, index=X_xgb_test.index)
X_lgbm_train[NUM_COLS] = pd.DataFrame(scaler.transform(X_lgbm_train[NUM_COLS]),     columns=NUM_COLS, index=X_lgbm_train.index)
X_lgbm_val[NUM_COLS]   = pd.DataFrame(scaler.transform(X_lgbm_val[NUM_COLS]),       columns=NUM_COLS, index=X_lgbm_val.index)
X_lgbm_test[NUM_COLS]  = pd.DataFrame(scaler.transform(X_lgbm_test[NUM_COLS]),      columns=NUM_COLS, index=X_lgbm_test.index)



# =============================================================================
# STEP 5: TUNE XGBOOST WITH OPTUNA
# =============================================================================
print("\n[5/9] Tuning XGBoost with Optuna (50 trials)...")

def xgb_objective(trial):
    params = {
        "n_estimators":      trial.suggest_int("n_estimators", 100, 800),
        "max_depth":         trial.suggest_int("max_depth", 3, 8),
        "learning_rate":     trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "subsample":         trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree":  trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "min_child_weight":  trial.suggest_int("min_child_weight", 1, 10),
        "gamma":             trial.suggest_float("gamma", 0.0, 1.0),
        "reg_alpha":         trial.suggest_float("reg_alpha", 0.0, 1.0),
        "reg_lambda":        trial.suggest_float("reg_lambda", 0.5, 2.0),
        "objective":         "multi:softprob",
        "num_class":         5,
        "tree_method":       "hist",
        "random_state":      42,
        "n_jobs":            -1,
    }
    model = XGBClassifier(**params)
    model.fit(X_xgb_train, y_train, verbose=False)
    preds = model.predict(X_xgb_val)
    return f1_score(y_val, preds, average="weighted")

xgb_study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42))
t0 = time.time()
xgb_study.optimize(xgb_objective, n_trials=50, show_progress_bar=False)
xgb_tune_time = time.time() - t0

print(f"  Best val weighted-F1: {xgb_study.best_value:.4f}")
print(f"  Tuning time: {xgb_tune_time:.1f}s")
print(f"  Best params: {xgb_study.best_params}")


# =============================================================================
# STEP 6: TUNE LIGHTGBM WITH OPTUNA
# =============================================================================
print("\n[6/9] Tuning LightGBM with Optuna (50 trials)...")

def lgbm_objective(trial):
    params = {
        "n_estimators":      trial.suggest_int("n_estimators", 100, 800),
        "max_depth":         trial.suggest_int("max_depth", 3, 8),
        "learning_rate":     trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "subsample":         trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree":  trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 50),
        "reg_alpha":         trial.suggest_float("reg_alpha", 0.0, 1.0),
        "reg_lambda":        trial.suggest_float("reg_lambda", 0.5, 2.0),
        "num_leaves":        trial.suggest_int("num_leaves", 20, 150),
        "objective":         "multiclass",
        "num_class":         5,
        "random_state":      42,
        "n_jobs":            -1,
        "verbose":           -1,
    }
    model = LGBMClassifier(**params)
    model.fit(
        X_lgbm_train, y_train,
        categorical_feature=CAT_COLS,
    )
    preds = model.predict(X_lgbm_val)
    return f1_score(y_val, preds, average="weighted")

lgbm_study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42))
t0 = time.time()
lgbm_study.optimize(lgbm_objective, n_trials=50, show_progress_bar=False)
lgbm_tune_time = time.time() - t0

print(f"  Best val weighted-F1: {lgbm_study.best_value:.4f}")
print(f"  Tuning time: {lgbm_tune_time:.1f}s")
print(f"  Best params: {lgbm_study.best_params}")


# =============================================================================
# STEP 7: TRAIN FINAL MODELS ON FULL TRAIN+VAL DATA
# =============================================================================
print("\n[7/9] Training final models on train+val combined...")

# Combine train + val for final training
X_xgb_final  = pd.concat([X_xgb_train,  X_xgb_val])
X_lgbm_final = pd.concat([X_lgbm_train, X_lgbm_val])
y_final       = np.concatenate([y_train, y_val])

# ── Final XGBoost ──────────────────────────────────────────────────────────
xgb_best_params = xgb_study.best_params.copy()
xgb_best_params.update({
    "objective":   "multi:softprob",
    "num_class":   5,
    "tree_method": "hist",
    "random_state": 42,
    "n_jobs":      -1,
})

t0 = time.time()
xgb_model = XGBClassifier(**xgb_best_params)
xgb_model.fit(X_xgb_final, y_final, verbose=False)
xgb_train_time = time.time() - t0
print(f"  XGBoost  trained in {xgb_train_time:.1f}s")

# ── Final LightGBM ─────────────────────────────────────────────────────────
lgbm_best_params = lgbm_study.best_params.copy()
lgbm_best_params.update({
    "objective":   "multiclass",
    "num_class":   5,
    "random_state": 42,
    "n_jobs":      -1,
    "verbose":     -1,
})

t0 = time.time()
lgbm_model = LGBMClassifier(**lgbm_best_params)
lgbm_model.fit(
    X_lgbm_final, y_final,
    categorical_feature=CAT_COLS,
)
lgbm_train_time = time.time() - t0
print(f"  LightGBM trained in {lgbm_train_time:.1f}s")


# =============================================================================
# STEP 8: EVALUATE ON TEST SET
# =============================================================================
print("\n[8/9] Evaluating on TEST SET (first time seeing this data)...")
print("=" * 65)

xgb_preds  = xgb_model.predict(X_xgb_test)
lgbm_preds = lgbm_model.predict(X_lgbm_test)

xgb_acc   = accuracy_score(y_test, xgb_preds)
lgbm_acc  = accuracy_score(y_test, lgbm_preds)
xgb_f1    = f1_score(y_test, xgb_preds,  average="weighted")
lgbm_f1   = f1_score(y_test, lgbm_preds, average="weighted")

# ── Summary table ──────────────────────────────────────────────────────────
print(f"\n{'Metric':<25} {'XGBoost':>12} {'LightGBM':>12}")
print("-" * 52)
print(f"{'Test Accuracy':<25} {xgb_acc*100:>11.2f}% {lgbm_acc*100:>11.2f}%")
print(f"{'Weighted F1':<25} {xgb_f1:>12.4f} {lgbm_f1:>12.4f}")
print(f"{'Tune time (s)':<25} {xgb_tune_time:>12.1f} {lgbm_tune_time:>12.1f}")
print(f"{'Train time (s)':<25} {xgb_train_time:>12.1f} {lgbm_train_time:>12.1f}")

# ── Per-class report ───────────────────────────────────────────────────────
print(f"\n── XGBoost per-class report ──")
print(classification_report(y_test, xgb_preds, target_names=CLASS_ORDER, digits=3))

print(f"── LightGBM per-class report ──")
print(classification_report(y_test, lgbm_preds, target_names=CLASS_ORDER, digits=3))

# ── Declare winner ─────────────────────────────────────────────────────────
if xgb_acc > lgbm_acc:
    winner = "XGBoost"
    winner_model   = xgb_model
    winner_X_test  = X_xgb_test
    winner_X_final = X_xgb_final
    winner_acc     = xgb_acc
    winner_f1      = xgb_f1
elif lgbm_acc > xgb_acc:
    winner = "LightGBM"
    winner_model   = lgbm_model
    winner_X_test  = X_lgbm_test
    winner_X_final = X_lgbm_final
    winner_acc     = lgbm_acc
    winner_f1      = lgbm_f1
else:
    # Tie on accuracy → use weighted F1 as tiebreaker
    if xgb_f1 >= lgbm_f1:
        winner, winner_model = "XGBoost",  xgb_model
        winner_X_test, winner_X_final = X_xgb_test, X_xgb_final
        winner_acc, winner_f1 = xgb_acc, xgb_f1
    else:
        winner, winner_model = "LightGBM", lgbm_model
        winner_X_test, winner_X_final = X_lgbm_test, X_lgbm_final
        winner_acc, winner_f1 = lgbm_acc, lgbm_f1

print("=" * 65)
print(f"  🏆 WINNER: {winner}")
print(f"     Test Accuracy : {winner_acc*100:.2f}%")
print(f"     Weighted F1   : {winner_f1:.4f}")
print("=" * 65)


# =============================================================================
# STEP 9: SHAP FEATURE IMPORTANCE (winner model)
# =============================================================================
print(f"\n[9/9] Computing SHAP feature importance for {winner}...")

# Use a sample for SHAP (faster, still representative)
shap_sample = winner_X_final.sample(n=min(2000, len(winner_X_final)), random_state=42)

explainer   = shap.TreeExplainer(winner_model)
shap_values = explainer.shap_values(shap_sample)

# shap_values shape depends on SHAP version + model type:
#   Newer SHAP + LightGBM → 3D array (samples, features, classes)
#   Older SHAP + LightGBM → list of 2D arrays → stacks to (classes, samples, features)
#   XGBoost multiclass    → list of 2D arrays → stacks to (classes, samples, features)
shap_arr = np.array(shap_values)

if shap_arr.ndim == 3 and shap_arr.shape[2] == 5:
    # (samples, features, classes) — newer SHAP with LightGBM
    mean_shap = np.abs(shap_arr).mean(axis=0).mean(axis=1)
elif shap_arr.ndim == 3:
    # (classes, samples, features) — older SHAP / XGBoost
    mean_shap = np.abs(shap_arr).mean(axis=0).mean(axis=0)
else:
    # (samples, features) — single output, shouldn't happen here
    mean_shap = np.abs(shap_arr).mean(axis=0)

feature_names = list(winner_X_final.columns)
mean_shap = np.array(mean_shap).flatten()  # guarantee 1D

shap_df = pd.DataFrame({
    "feature":    feature_names,
    "importance": mean_shap
}).sort_values("importance", ascending=False).reset_index(drop=True)

print(f"\n── SHAP Feature Importances ({winner}) ──")
for _, row in shap_df.iterrows():
    bar = "█" * int(row["importance"] * 300)
    print(f"  {row['feature']:<30} {row['importance']:.4f}  {bar}")

# ── Save SHAP bar chart ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
colors = ["#e74c3c" if imp > shap_df["importance"].median() else "#3498db" for imp in shap_df["importance"]]
ax.barh(shap_df["feature"][::-1], shap_df["importance"][::-1], color=colors[::-1])
ax.set_xlabel("Mean |SHAP Value| (impact on prediction)", fontsize=11)
ax.set_title(f"Feature Importance — {winner} (SHAP)", fontsize=13, fontweight="bold")
ax.axvline(shap_df["importance"].median(), color="gray", linestyle="--", linewidth=1, label="Median")
ax.legend()
plt.tight_layout()
shap_path = f"{REPORTS_DIR}shap_importance_{winner.lower().replace(' ','_')}.png"
plt.savefig(shap_path, dpi=150)
plt.close()
print(f"\n  SHAP chart saved → {shap_path}")

# ── Save confusion matrix ──────────────────────────────────────────────────
winner_preds = xgb_preds if winner == "XGBoost" else lgbm_preds
cm = confusion_matrix(y_test, winner_preds)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASS_ORDER)
fig, ax = plt.subplots(figsize=(8, 6))
disp.plot(ax=ax, colorbar=True, cmap="Blues")
ax.set_title(f"Confusion Matrix — {winner}", fontsize=13, fontweight="bold")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
cm_path = f"{REPORTS_DIR}confusion_matrix_{winner.lower().replace(' ','_')}.png"
plt.savefig(cm_path, dpi=150)
plt.close()
print(f"  Confusion matrix saved → {cm_path}")


# =============================================================================
# SAVE ALL ARTIFACTS
# =============================================================================
print(f"\n── Saving artifacts ──")

# Winner model
joblib.dump(winner_model, f"{MODELS_DIR}predictor.joblib")
print(f"  ✓ predictor.joblib         ({winner})")

# Scaler (fitted on train split only)
joblib.dump(scaler, f"{MODELS_DIR}scaler.joblib")
print(f"  ✓ scaler.joblib")

# All label encoders for categorical features + target
all_encoders = {**le_encoders, "target": le_target}
joblib.dump(all_encoders, f"{MODELS_DIR}encoders.joblib")
print(f"  ✓ encoders.joblib          (department, sleep, extra, travel, target)")

# Feature order (critical for inference — input must match this order)
joblib.dump(FEATURE_COLS, f"{MODELS_DIR}feature_order.joblib")
print(f"  ✓ feature_order.joblib     {FEATURE_COLS}")

# Model metadata (for API / frontend display)
metadata = {
    "winner":          winner,
    "test_accuracy":   round(winner_acc * 100, 2),
    "weighted_f1":     round(winner_f1, 4),
    "class_order":     CLASS_ORDER,
    "numeric_cols":    NUM_COLS,
    "categorical_cols": CAT_COLS,
    "xgb_val_f1":      round(xgb_study.best_value, 4),
    "lgbm_val_f1":     round(lgbm_study.best_value, 4),
    "xgb_best_params": xgb_study.best_params,
    "lgbm_best_params": lgbm_study.best_params,
}
joblib.dump(metadata, f"{MODELS_DIR}metadata.joblib")
print(f"  ✓ metadata.joblib          (accuracy, params, class_order)")

print(f"\n{'='*65}")
print(f"  Training complete!")
print(f"  Winner : {winner}")
print(f"  Accuracy: {winner_acc*100:.2f}%  |  Weighted F1: {winner_f1:.4f}")
print(f"  All artifacts saved to {MODELS_DIR}")
print(f"{'='*65}")
