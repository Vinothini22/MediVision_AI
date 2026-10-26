from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

BASE_DIR = Path(__file__).resolve().parent

RESULT_DIR = BASE_DIR / "results"
GRAPH_DIR = RESULT_DIR / "graphs"

GRAPH_DIR.mkdir(parents=True, exist_ok=True)

# Load saved evaluation results
metrics = pd.read_csv(
    RESULT_DIR / "final_test_metrics.csv"
)

cm_df = pd.read_csv(
    RESULT_DIR / "confusion_matrix.csv",
    index_col=0
)

predictions = pd.read_csv(
    RESULT_DIR / "test_predictions.csv"
)

# GRAPH 1: Performance Metrics
metric_names = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1 Score"
]

metric_values = [
    metrics["accuracy"].iloc[0] * 100,
    metrics["precision"].iloc[0] * 100,
    metrics["recall"].iloc[0] * 100,
    metrics["f1_score"].iloc[0] * 100
]

fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(metric_names, metric_values)

ax.set_title("MediVision AI - Final Test Performance")
ax.set_ylabel("Score (%)")
ax.set_ylim(0, 100)

ax.bar_label(bars, fmt="%.2f%%", padding=3)

fig.tight_layout()

fig.savefig(
    GRAPH_DIR / "performance_metrics.png",
    dpi=300
)

plt.close(fig)

# GRAPH 2: Confusion Matrix
cm = cm_df.to_numpy()

fig, ax = plt.subplots(figsize=(7, 6))

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=[
        "Normal",
        "Other Labels"
    ]
)

display.plot(
    ax=ax,
    cmap="Blues",
    values_format="d",
    colorbar=False
)

ax.set_title("MediVision AI - Test Confusion Matrix")

fig.tight_layout()

fig.savefig(
    GRAPH_DIR / "confusion_matrix.png",
    dpi=300
)

plt.close(fig)

# GRAPH 3: Actual vs Predicted Counts
actual = predictions["actual_label"].value_counts()
predicted = predictions["predicted_label"].value_counts()

labels = [0, 1]

actual_counts = [
    actual.get(label, 0) for label in labels
]

predicted_counts = [
    predicted.get(label, 0) for label in labels
]

import numpy as np

x = np.arange(2)
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    x - width / 2,
    actual_counts,
    width,
    label="Actual"
)

ax.bar(
    x + width / 2,
    predicted_counts,
    width,
    label="Predicted"
)

ax.set_xticks(x)
ax.set_xticklabels(["Normal", "Other Labels"])

ax.set_ylabel("Number of Images")
ax.set_title("Actual vs Predicted Label Distribution")
ax.legend()

fig.tight_layout()

fig.savefig(
    GRAPH_DIR / "actual_vs_predicted.png",
    dpi=300
)

plt.close(fig)

print("\n===== GRAPH GENERATION =====")

print("1. Performance Metrics Graph - Saved")
print("2. Confusion Matrix Graph - Saved")
print("3. Actual vs Predicted Graph - Saved")

print("\nSTEP 40 COMPLETED!")