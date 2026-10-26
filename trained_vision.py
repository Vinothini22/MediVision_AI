from pathlib import Path

import torch
import joblib
import streamlit as st

from PIL import Image
from transformers import ViTModel, ViTImageProcessor


BASE_DIR = Path(__file__).resolve().parent

MODEL_NAME = "google/vit-base-patch16-224-in21k"

CLASSIFIER_PATH = (
    BASE_DIR
    / "models"
    / "vit_classifier_optimized.joblib"
)


@st.cache_resource
def load_trained_vision():

    processor = ViTImageProcessor.from_pretrained(
        MODEL_NAME
    )

    vision_model = ViTModel.from_pretrained(
        MODEL_NAME
    )

    vision_model.eval()

    classifier = joblib.load(CLASSIFIER_PATH)

    return processor, vision_model, classifier


def predict_xray(uploaded_file):

    processor, vision_model, classifier = (
        load_trained_vision()
    )

    image = Image.open(uploaded_file).convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.inference_mode():

        outputs = vision_model(**inputs)

        features = outputs.last_hidden_state[:, 0, :]

    feature_vector = features.cpu().numpy()

    prediction = int(
        classifier.predict(feature_vector)[0]
    )

    probabilities = classifier.predict_proba(
        feature_vector
    )[0]

    label_names = {
        0: "Normal Report Label",
        1: "Other Report Labels"
    }

    classes = list(classifier.classes_)
    class_index = classes.index(prediction)

    return {
        "status": "Prediction Successful",
        "prediction": label_names[prediction],
        "predicted_label": prediction,
        "model_score": round(
            float(probabilities[class_index]) * 100,
            2
        ),
        "feature_dimension": feature_vector.shape[1],
        "note": (
            "Experimental report-derived classification only. "
            "Not a clinical diagnosis. Model score is not "
            "a calibrated medical confidence value."
        )
    }


if __name__ == "__main__":

    print("\n===== TRAINED VISION MODEL TEST =====")

    processor, vision_model, classifier = (
        load_trained_vision()
    )

    print("ViT Model Loaded Successfully!")
    print("Optimized Classifier Loaded Successfully!")
    print("Classifier Classes:", classifier.classes_)

    print("\nSTEP 41 COMPLETED!")