import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dataset" / "iu_xray" / "processed"

splits = ["train", "validation", "test"]

for split in splits:

    input_path = DATA_DIR / f"{split}.csv"

    df = pd.read_csv(input_path)

    # Normalize report labels
    labels = (
        df["Problems"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Exclude empty labels
    df = df.loc[labels != ""].copy()
    labels = labels.loc[labels != ""]

    # Experimental binary labels
    df["label"] = (labels != "normal").astype(int)

    output_path = DATA_DIR / f"{split}_labeled.csv"

    df.to_csv(output_path, index=False)

    print(f"\n===== {split.upper()} =====")
    print("Total Records:", len(df))
    print("Normal:", int((df["label"] == 0).sum()))
    print("Other:", int((df["label"] == 1).sum()))
    print("Saved:", output_path)

print("\nLABEL PREPARATION COMPLETED!")