from app.core.model_loader import ModelStore
from app.services.preprocess import preprocess_input


def run_prediction(features: dict):
    model, scaler, encoders = ModelStore.load_all()

    X = preprocess_input(features, scaler, encoders)
    probs = model.predict_proba(X)[0]
    classes = model.classes_
    best_idx = probs.argmax()

    predicted_class_idx = classes[best_idx]
    target_encoder = encoders["target"]
    predicted_label = target_encoder.inverse_transform([predicted_class_idx])[0]

    prob_dict = {}
    for i, class_idx in enumerate(classes):
        label = target_encoder.inverse_transform([class_idx])[0]
        prob_dict[label] = float(probs[i])

    return {
        "performance_category": predicted_label,
        "confidence": float(probs[best_idx]),
        "probabilities": prob_dict
    }
