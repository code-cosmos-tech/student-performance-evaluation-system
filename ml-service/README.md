# Student Performance Predictor – ML Service

This service provides machine learning–based predictions for student academic performance.  
It is designed as a **stateless ML inference microservice** and is consumed by the main backend (Node.js/Express).

The service predicts a student’s **performance category** based on academic, behavioral, and contextual features.

---

## Responsibilities

This ML service is responsible for:

- Loading the trained ML model and preprocessing artifacts
- Validating incoming student feature data
- Performing inference using an XGBoost classifier
- Returning prediction results with confidence scores

This service **does not**:
- Handle authentication
- Interact with databases
- Manage users or sessions

---

## Tech Stack

- **Framework**: FastAPI
- **ML Model**: XGBoost (trained offline)
- **Preprocessing**: Scikit-learn
- **Model Serialization**: joblib
- **Runtime**: Python 3.12.6

---

## Project Structure
```
ml-service/
│
├── app/
│   ├── main.py                # FastAPI app entry point
│   │
│   ├── api/
│   │   └── routes.py          # API routes
│   │
│   ├── core/
│   │   ├── config.py          # Environment-based configuration
│   │   ├── dependencies.py    # Shared dependencies
│   │   └── model_loader.py    # Model & artifact loading
│   │
│   ├── schemas/
│   │   ├── request.py         # Input validation schemas
│   │   └── response.py        # Output schemas
│   │
│   └── services/
│       ├── preprocess.py      # Feature preprocessing
│       └── predictor.py       # Prediction logic
│
├── models/
│   ├── predictor.joblib       # Trained XGBoost model
│   ├── scaler.joblib          # Feature scaler
│   └── encoders.joblib        # Label encoders
│
├── tests/
│   └── test_predictor.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Environment Configuration

This service uses environment variables for all configurable values.

### `.env.example`

```env
APP_NAME="ML API Service - Student Performance Evaluation System"
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true

API_PREFIX=/api
API_SERVICE=ml

CORS_ORIGINS=http://localhost:3000

MODEL_PATH=models/predictor.joblib
SCALER_PATH=models/scaler.joblib
ENCODERS_PATH=models/encoders.joblib
```

Create your local .env file by copying:

```bash
cp .env.example .env
```

---

## Installation

1. Create virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

2. Install dependencies
```bash
pip install -r requirements.txt requirements-dev.txt
```

---

## Running the service

Start the FastAPI server by using uvicorn
```bash
uvicorn app.main:app --reload
```

By default, service runs at:
```arduino
http://localhost:8000
```

Interactive API docs are available at:
```arduino
http://localhost:8000/docs
```

---

## API Endpoints

### Health Check

**GET /api/{version}/ml/health**

Response:
```json
{
    "status": "ok",
    "model_loaded": true
}
```

### Predict Student Performance

**POST /api/{version}/ml/predict**

Request Body:
```json
{
  "lastSemSPI": 7.8,
  "internalAssessmentAvg": 65,
  "attendancePercentage": 82,
  "totalBacklogs": 1,
  "pyqSolvingFreq": 3,
  "studyHoursWeekly": 22,
  "sleepCategory": "6-8",
  "gamingHoursWeekly": 6,
  "assignmentDelayCount": 2,
  "department": "CSE",
  "travelTimeCategory": "30-60",
  "extraCurricularLevel": "Medium"
}
```

Response Body:
```json
{
    "performance_category": "Average",
    "confidence": 0.81,
    "probability": {
        "At Risk": 0.12,
        "Average": 0.81,
        "Good": 0.07
    }
}
```

---

## Integration with backend

This service is intended to be called by the Node.js/Express backend.

Typical flow:
```scss
Frontend → Backend (Node.js) → ML Service (FastAPI)
```

The frontend should never call the ML service directly.

---

## Notes

- The model, scaler, and encoders are loaded once and reused for all requests
- Preprocessing logic exactly matches the training pipeline
- Strict input validation is enforced using Pydantic schemas
- The service is stateless and horizontally scalable
