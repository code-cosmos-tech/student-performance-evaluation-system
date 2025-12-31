def test_health_check(client):
    response = client.get("/api/1.0.0/ml/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True


def test_prediction_success(client):
    payload = {
        "lastSemSPI": 7.5,
        "internalAssessmentAvg": 65,
        "attendancePercentage": 80,
        "totalBacklogs": 1,
        "pyqSolvingFrequency": 3,
        "studyHoursWeekly": 20,
        "sleepCategory": "6-8",
        "gamingHoursWeekly": 5,
        "assignmentDelayCount": 1,
        "department": "CSE",
        "travelTimeCategory": "30-60",
        "extraCurricularLevel": "Medium"
    }

    response = client.post("/api/1.0.0/ml/predict", json=payload)
    assert response.status_code == 200

    data = response.json()

    assert "performance_category" in data
    assert "confidence" in data
    assert "probabilities" in data

    assert data["performance_category"] in ["At Risk", "Average", "Good"]
    assert 0.0 <= data["confidence"] <= 1.0


def test_prediction_invalid_input(client):
    payload = {
        "lastSemSPI": 15,  # invalid (>10)
        "internalAssessmentAvg": 65,
        "attendancePercentage": 80,
        "totalBacklogs": -1,  # invalid
        "pyqSolvingFrequency": 3,
        "studyHoursWeekly": 20,
        "sleepCategory": "10-12",  # invalid
        "gamingHoursWeekly": 5,
        "assignmentDelayCount": 1,
        "department": "UNKNOWN",
        "travelTimeCategory": "30-60",
        "extraCurricularLevel": "Medium"
    }

    response = client.post("/api/1.0.0/ml/predict", json=payload)

    assert response.status_code == 422  # validation error
