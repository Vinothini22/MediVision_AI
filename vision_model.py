import torch
import numpy as np
from PIL import Image
from transformers import ViTModel, ViTImageProcessor
import streamlit as st


MODEL_NAME = "google/vit-base-patch16-224-in21k"


@st.cache_resource
def load_vision_model():

    processor = ViTImageProcessor.from_pretrained(
        MODEL_NAME
    )

    model = ViTModel.from_pretrained(
        MODEL_NAME
    )

    model.eval()

    return processor, model


def analyze_xray(uploaded_file):

    processor, model = load_vision_model()

    image = Image.open(uploaded_file).convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model(**inputs)

        features = outputs.last_hidden_state[:, 0, :]

    feature_vector = features.squeeze().cpu().numpy()

    return {
        "status": "Vision Transformer Processing Successful",
        "model": MODEL_NAME,
        "feature_dimension": len(feature_vector),
        "feature_vector": feature_vector
    }