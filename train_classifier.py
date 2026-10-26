from pathlib import Path

import numpy as np
import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


BASE_DIR = Path(__file__).resolve().parent

FEATURE_DIR = BASE_DIR / "features"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# 1. Load saved ViT features

train = np.load(FEATURE_DIR / "train_features.npz")
validation = np.load(
    FEATURE_DIR / "validation_features.npz"
)

X_train = train["features"]
y_train = train["labels"]

X_val = validation["features"]
y_val = validation["labels"]


print("\n===== DATASET INFORMATION =====")

print("Training Features:", X_train.shape)
print("Training Labels:", y_train.shape)

print("Validation Features:", X_val.shape)
print("Validation Labels:", y_val.shape)


# 2. Validate feature dimensions

assert X_train.shape[1] == 768
assert X_val.shape[1] == 768

assert len(X_train) == len(y_train)
assert len(X_val) == len(y_val)

assert set(np.unique(y_train)) == {0, 1}


# 3. Create classification pipeline

classifier = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=42
        )
    )
])


# 4. Train classifier

print("\nTraining Classifier...")

classifier.fit(X_train, y_train)

print("MODEL TRAINING SUCCESSFUL!")


# 5. Validation predictions

predictions = classifier.predict(X_val)


# 6. Calculate validation metrics

accuracy = accuracy_score(y_val, predictions)

precision = precision_score(
    y_val,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_val,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_val,
    predictions,
    zero_division=0
)


print("\n===== VALIDATION RESULTS =====")

print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("F1 Score:", round(f1, 4))

print("\nClassification Report:")

print(
    classification_report(
        y_val,
        predictions,
        labels=[0, 1],
        target_names=[
            "Normal",
            "Other Report Labels"
        ],
        zero_division=0
    )
)

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_val,
        predictions,
        labels=[0, 1]
    )
)


# 7. Save trained classifier

model_path = MODEL_DIR / "vit_classifier.joblib"

joblib.dump(classifier, model_path)

print("\nModel Saved:", model_path)

print("\nSTEP 37 COMPLETED!")