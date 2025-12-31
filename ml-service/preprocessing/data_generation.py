# ================== PLEASE CHECK THE SAVING PATH BEFORE RUNNING THE FILE ================== #

import numpy as np
import pandas as pd

np.random.seed(42)
n = 20000

print(f"Generating synthetic student data with {n} students...")
data = {
    "last_sem_spi": np.round(np.random.uniform(1.0, 10.0, n), 2),
    "internal_assessment_avg": np.round(np.random.uniform(30, 90, n), 1),
    "attendance_percentage": np.round(np.random.uniform(20, 100, n), 1),
    "total_backlogs": np.random.poisson(1.2, n),
    "pyq_solving_frequency": np.random.randint(0, 6, n),  # times per week

    "study_hours_weekly": np.round(np.random.uniform(5, 50, n), 1),
    "sleep_category": np.random.choice(["<6", "6-8", ">8"], n, p=[0.3, 0.5, 0.2]),
    "gaming_hours_weekly": np.round(np.random.uniform(0, 30, n), 1),
    "assignment_delay_count": np.random.poisson(1.5, n),

    "department": np.random.choice(
        ["CE", "IT", "EC", "ME", "ICT", "EE"], n
    ),
    "travel_time_category": np.random.choice(
        ["<30", "30-60", ">60"], n, p=[0.4, 0.4, 0.2]
    ),
    "extra_curricular_level": np.random.choice(
        ["Low", "Medium", "High"], n, p=[0.4, 0.4, 0.2]
    )
}

df = pd.DataFrame(data)

# clean unrealistic values
df["total_backlogs"] = df["total_backlogs"].clip(0, 10)
df["assignment_delay_count"] = df["assignment_delay_count"].clip(0, 15)
print("Synthetic student data generated!")

# saving path
path = "../data/student_performance_data_synthetic.csv"
df.to_csv(path, index=False)
print(f"Student data saved at {path}")
