from pathlib import Path
import pandas as pd

# Dataset location
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset" / "iu_xray"


def find_file(filename):
    matches = list(DATASET_DIR.rglob(filename))

    if not matches:
        raise FileNotFoundError(
            f"{filename} not found inside {DATASET_DIR}"
        )

    return matches[0]


def load_dataset():

    # Locate CSV files
    reports_path = find_file("indiana_reports.csv")
    projections_path = find_file("indiana_projections.csv")

    # Read CSV files
    reports = pd.read_csv(reports_path)
    projections = pd.read_csv(projections_path)

    # Validate required columns
    report_columns = {"uid", "findings", "impression"}
    projection_columns = {"uid", "filename", "projection"}

    if not report_columns.issubset(reports.columns):
        raise ValueError("Required report columns missing")

    if not projection_columns.issubset(projections.columns):
        raise ValueError("Required projection columns missing")

    # Avoid duplicate report IDs
    if reports["uid"].duplicated().any():
        raise ValueError("Duplicate report UID detected")

    # Pair images with reports using UID
    paired = pd.merge(
        projections,
        reports,
        on="uid",
        how="inner",
        validate="many_to_one"
    )

    # Locate image folder
    images_dir = find_file("images_normalized")

    # Add actual image paths
    paired["image_path"] = paired["filename"].apply(
        lambda name: str(images_dir / str(name))
    )

    # Verify image availability
    paired["image_exists"] = paired["image_path"].apply(
        lambda path: Path(path).is_file()
    )

    return paired


if __name__ == "__main__":

    dataset = load_dataset()

    print("\n===== MEDIVISION DATASET =====")

    print("Total paired records:", len(dataset))

    print(
        "Available images:",
        int(dataset["image_exists"].sum())
    )

    print(
        "Missing images:",
        int((~dataset["image_exists"]).sum())
    )

    print("\nProjection Distribution:")

    print(dataset["projection"].value_counts())

    print("\nFirst Paired Record:")

    sample = dataset.iloc[0]

    print("UID:", sample["uid"])
    print("Image:", sample["filename"])
    print("Projection:", sample["projection"])
    print("Image Exists:", sample["image_exists"])
    print("Findings:", sample["findings"])
    print("Impression:", sample["impression"])

    # Save verified records
    output_dir = DATASET_DIR / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    valid_dataset = dataset[
        dataset["image_exists"]
    ].copy()

    output_path = output_dir / "paired_dataset.csv"

    valid_dataset.to_csv(
        output_path,
        index=False
    )

    print("\nSaved:", output_path)
    print("Valid paired records:", len(valid_dataset))