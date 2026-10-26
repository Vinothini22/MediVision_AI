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
    f1_score
)

BASE_DIR = Path(__file__).resolve().parent
FEATURE_DIR = BASE_DIR / "features"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Load previously extracted features
train = np.load(FEATURE_DIR / "train_features.npz")
val = np.load(FEATURE_DIR / "validation_features.npz")

X_train = train["features"]
y_train = train["labels"]

X_val = val["features"]
y_val = val["labels"]

print("Training:", X_train.shape)
print("Validation:", X_val.shape)

# Try different regularization strengths
c_values = [0.001, 0.01, 0.1, 1.0, 10.0]

best_f1 = -1
best_model = None
best_c = None

print("\n===== MODEL OPTIMIZATION =====")

for c in c_values:

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(
            C=c,
            max_iter=3000,
            class_weight="balanced",
            random_state=42
        ))
    ])

    model.fit(X_train, y_train)

    predictions = model.predict(X_val)

    accuracy = accuracy_score(y_val, predictions)
    precision = precision_score(
        y_val, predictions, zero_division=0
    )
    recall = recall_score(
        y_val, predictions, zero_division=0
    )
    f1 = f1_score(
        y_val, predictions, zero_division=0
    )

    print(f"\nC = {c}")
    print("Accuracy:", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("F1:", round(f1, 4))

    if f1 > best_f1:
        best_f1 = f1
        best_model = model
        best_c = c

# Save optimized model separately
output_path = MODEL_DIR / "vit_classifier_optimized.joblib"

joblib.dump(best_model, output_path)

print("\n===== BEST MODEL =====")
print("Best C:", best_c)
print("Best Validation F1:", round(best_f1, 4))
print("Saved:", output_path)
print("\nSTEP 38 COMPLETED!")