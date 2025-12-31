import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import joblib

# 1. Load Data
path = "../data/student_performance_with_PS_and_labels.csv"
print(f"Loading data from {path}")
df = pd.read_csv(path)

# 2. Define Maps
sleep_map = {"<6": 0.3, "6-8": 1.0, ">8": 0.8}
travel_map = {"<30": 1.0, "30-60": 0.7, ">60": 0.4}
extra_map = {"Low": 0.3, "Medium": 0.7, "High": 1.0}

print("Applying custom mappings...")
df['sleep_score'] = df['sleep_category'].map(sleep_map)
df['travel_score'] = df['travel_time_category'].map(travel_map)
df['extra_score'] = df['extra_curricular_level'].map(extra_map)

# 3. Handle Department
print("Encoding department...")
le_dept = LabelEncoder()
df['department'] = le_dept.fit_transform(df['department'])

# 4. Scale Numeric Columns
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

print("Scaling numeric features...")
scaler = MinMaxScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# 5. Prepare X and y
feature_order = numeric_cols + ['sleep_score', 'travel_score', 'extra_score', 'department']

X = df[feature_order]
y = df["performance_category"]

# Encode Target (y)
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)

# 6. Train Model
print(f"Training on {X.shape[1]} features")
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.25, random_state=42)

# Using your params
params = {
    'n_estimators': 995,
    'max_depth': 3,
    'min_child_weight': 2,
    'learning_rate': 0.2767290889210465,
    'subsample': 0.6725823903100828,
    'colsample_bytree': 0.688567048234252,
    'gamma': 0.26935104909682095,
    'tree_method': 'hist',
    'booster': 'gbtree'
}

xgb_model = XGBClassifier(**params)
xgb_model.fit(X_train, y_train)

print(f"Accuracy: {xgb_model.score(X_test, y_test) * 100:.2f}%")

# 7. Save Artifacts
joblib.dump(xgb_model, "../models/predictor.joblib")
print("Saved predictor.joblib")

joblib.dump(scaler, "../models/scaler.joblib")
print("Saved scaler.joblib")

# Save Encoders (Only department is needed for inference now)
encoders = {
    "department": le_dept,
    "target": le_target,
}
joblib.dump(encoders, "../models/encoders.joblib")
print("Saved encoders.joblib")
