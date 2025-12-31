import numpy as np


sleep_map = {"<6": 0.3, "6-8": 1.0, ">8": 0.8}
travel_map = {"<30": 1.0, "30-60": 0.7, ">60": 0.4}
extra_map = {"Low": 0.3, "Medium": 0.7, "High": 1.0}

FEATURE_ORDER = [
    "last_sem_spi",
    "internal_assessment_avg",
    "attendance_percentage",
    "total_backlogs",
    "pyq_solving_frequency",
    "study_hours_weekly",
    "gaming_hours_weekly",
    "assignment_delay_count",
    "sleep_score",
    "travel_score",
    "extra_score",
    "department"
]


def preprocess_input(data: dict, scaler, encoders):
    processed = {
        "last_sem_spi": data["last_sem_spi"],
        "internal_assessment_avg": data["internal_assessment_avg"],
        "attendance_percentage": data["attendance_percentage"],
        "total_backlogs": data["total_backlogs"],
        "pyq_solving_frequency": data["pyq_solving_frequency"],
        "study_hours_weekly": data["study_hours_weekly"],
        "gaming_hours_weekly": data["gaming_hours_weekly"],
        "assignment_delay_count": data["assignment_delay_count"],
        "sleep_score": sleep_map[data["sleep_category"]],
        "travel_score": travel_map[data["travel_time_category"]],
        "extra_score": extra_map[data["extra_curricular_level"]],
        "department": encoders["department"].transform([data["department"]])[0]
    }

    numeric_part = np.array([[
        processed["last_sem_spi"],
        processed["internal_assessment_avg"],
        processed["attendance_percentage"],
        processed["total_backlogs"],
        processed["pyq_solving_frequency"],
        processed["study_hours_weekly"],
        processed["gaming_hours_weekly"],
        processed["assignment_delay_count"]
    ]])

    scaled_numeric = scaler.transform(numeric_part)[0]

    final_vector = np.array([
        scaled_numeric[0],
        scaled_numeric[1],
        scaled_numeric[2],
        scaled_numeric[3],
        scaled_numeric[4],
        scaled_numeric[5],
        scaled_numeric[6],
        scaled_numeric[7],
        processed["sleep_score"],
        processed["travel_score"],
        processed["extra_score"],
        processed["department"]
    ]).reshape(1, -1)

    return final_vector
