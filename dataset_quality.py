import pandas as pd
from pathlib import Path

from dataset_loader import DATASET_DIR

# Load verified paired dataset
dataset_path = DATASET_DIR / "processed" / "paired_dataset.csv"

df = pd.read_csv(dataset_path)

print("\n===== MEDIVISION DATASET QUALITY REPORT =====")

print("Total Image Records:", len(df))

print("Unique Report IDs:", df["uid"].nunique())

print("\nProjection Distribution:")
print(df["projection"].value_counts())

print("\nMissing Findings:")
print(df["findings"].isna().sum())

print("\nMissing Impressions:")
print(df["impression"].isna().sum())

print("\nDuplicate Image Filenames:")
print(df["filename"].duplicated().sum())

print("\nMissing Image Files:")
print((~df["image_path"].apply(
    lambda p: Path(p).is_file()
)).sum())

print("\n===== QUALITY CHECK COMPLETED =====")