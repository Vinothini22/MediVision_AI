import pandas as pd
from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit

from dataset_loader import DATASET_DIR

# ==========================================
# LOAD PAIRED DATASET
# ==========================================

input_path = DATASET_DIR / "processed" / "paired_dataset.csv"

df = pd.read_csv(input_path)

required = {"uid", "filename", "image_path"}

if not required.issubset(df.columns):
    raise ValueError("Required dataset columns are missing.")

if df.empty:
    raise ValueError("Paired dataset is empty.")

if df["uid"].isna().any():
    raise ValueError("Missing UID detected.")

# ==========================================
# FIRST SPLIT: TRAIN 70%, TEMP 30%
# ==========================================

splitter1 = GroupShuffleSplit(
    n_splits=1,
    train_size=0.70,
    random_state=42
)

train_idx, temp_idx = next(
    splitter1.split(df, groups=df["uid"])
)

train_df = df.iloc[train_idx].copy()
temp_df = df.iloc[temp_idx].copy()

# ==========================================
# SECOND SPLIT: VALIDATION / TEST
# ==========================================

splitter2 = GroupShuffleSplit(
    n_splits=1,
    train_size=0.50,
    random_state=42
)

val_idx, test_idx = next(
    splitter2.split(temp_df, groups=temp_df["uid"])
)

val_df = temp_df.iloc[val_idx].copy()
test_df = temp_df.iloc[test_idx].copy()

# ==========================================
# VERIFY NO UID LEAKAGE
# ==========================================

train_ids = set(train_df["uid"])
val_ids = set(val_df["uid"])
test_ids = set(test_df["uid"])

assert train_ids.isdisjoint(val_ids)
assert train_ids.isdisjoint(test_ids)
assert val_ids.isdisjoint(test_ids)

assert (
    len(train_df) + len(val_df) + len(test_df)
    == len(df)
)

# ==========================================
# SAVE SPLITS
# ==========================================

output_dir = DATASET_DIR / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

train_df.to_csv(output_dir / "train.csv", index=False)
val_df.to_csv(output_dir / "validation.csv", index=False)
test_df.to_csv(output_dir / "test.csv", index=False)

# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n===== MEDIVISION DATASET SPLIT =====")

print("Total Image Records:", len(df))
print("Unique Report IDs:", df["uid"].nunique())

print("\nTRAIN")
print("Images:", len(train_df))
print("Unique UIDs:", len(train_ids))

print("\nVALIDATION")
print("Images:", len(val_df))
print("Unique UIDs:", len(val_ids))

print("\nTEST")
print("Images:", len(test_df))
print("Unique UIDs:", len(test_ids))

print("\nUID Leakage: NONE")
print("Split Verification: PASSED")

print("\nFiles Saved Successfully!")