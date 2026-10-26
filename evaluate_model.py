from pathlib import Path

import numpy as np
import joblib
import pandas as pd

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
RESULT_DIR = BASE_DIR / "results"

RESULT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load final test features
test = np.load(FEATURE_DIR / "test_features.npz")

X_test = test["features"]
y_test = test["labels"]

print("\n===== TEST DATASET =====")
print("Features:", X_test.shape)
print("Labels:", y_test.shape)

assert X_test.shape == (1111, 768)
assert len(y_test) == 1111

# 2. Load previously optimized model
model_path = MODEL_DIR / "vit_classifier_optimized.joblib"

model = joblib.load(model_path)

print("\nOptimized Model Loaded Successfully!")

# 3. Predict test labels
predictions = model.predict(X_test)

# 4. Calculate final metrics
accuracy = accuracy_score(y_test, predictions)

precision = precision_score(
    y_test, predictions, zero_division=0
)

recall = recall_score(
    y_test, predictions, zero_division=0
)

f1 = f1_score(
    y_test, predictions, zero_division=0
)

cm = confusion_matrix(
    y_test, predictions, labels=[0, 1]
)

print("\n===== FINAL TEST RESULTS =====")

print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("F1 Score:", round(f1, 4))

print("\nClassification Report:")

print(
    classification_report(
        y_test,
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
print(cm)

# 5. Save metrics
metrics = pd.DataFrame([{
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1_score": f1
}])

metrics.to_csv(
    RESULT_DIR / "final_test_metrics.csv",
    index=False
)

# 6. Save confusion matrix
pd.DataFrame(
    cm,
    index=["Actual_Normal", "Actual_Other"],
    columns=["Predicted_Normal", "Predicted_Other"]
).to_csv(
    RESULT_DIR / "confusion_matrix.csv"
)

# 7. Save predictions
pd.DataFrame({
    "actual_label": y_test,
    "predicted_label": predictions
}).to_csv(
    RESULT_DIR / "test_predictions.csv",
    index=False
)

print("\nResults Saved Successfully!")
print("STEP 39.2 COMPLETED!")