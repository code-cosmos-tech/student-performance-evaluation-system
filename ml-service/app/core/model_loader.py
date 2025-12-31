import joblib
from app.core.config import settings


class ModelStore:
    model = None
    scaler = None
    encoders = None

    @classmethod
    def load_all(cls):
        if cls.model is None:
            cls.model = joblib.load(settings.model_path)
            cls.scaler = joblib.load(settings.scaler_path)
            cls.encoders = joblib.load(settings.encoders_path)
        return cls.model, cls.scaler, cls.encoders

    @classmethod
    def load_model(cls):
        if cls.model is None:
            cls.model = joblib.load(settings.model_path)
        return cls.model

    @classmethod
    def load_scaler(cls):
        if cls.scaler is None:
            cls.scaler = joblib.load(settings.scaler_path)
        return cls.scaler

    @classmethod
    def load_encoders(cls):
        if cls.encoders is None:
            cls.encoders = joblib.load(settings.encoders_path)
        return cls.encoders
