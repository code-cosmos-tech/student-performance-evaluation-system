from fastapi import APIRouter, Depends
from app.core.model_loader import ModelStore
from app.core.dependencies import get_api_service_name, get_api_version
from app.schemas.request import StudentFeatures
from app.schemas.response import PredictionResponse
from app.services.predictor import run_prediction


router = APIRouter()


@router.get("/info")
async def info(api_service_name: str = Depends(get_api_service_name)):
    return {"api_service_name": api_service_name}


@router.get("/meta")
async def meta(api_version: str = Depends(get_api_version)):
    return {"api_version": api_version}


@router.get("/health")
def health_check():
    ModelStore.load_all()
    return {
        "status": "ok",
        "model_loaded": True
    }


@router.post("/predict", response_model=PredictionResponse)
def predict_student_performance(data: StudentFeatures):
    result = run_prediction(data.model_dump())
    return result
