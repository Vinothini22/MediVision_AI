import argparse
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader
from transformers import ViTModel

from training_dataset import XRayDataset, MODEL_NAME


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = (
    BASE_DIR / "dataset" / "iu_xray" / "processed"
)

FEATURE_DIR = BASE_DIR / "features"

FEATURE_DIR.mkdir(parents=True, exist_ok=True)


def extract_features(split, limit=20):

    csv_path = DATA_DIR / f"{split}_labeled.csv"

    dataset = XRayDataset(csv_path)

    if limit > 0:
        dataset.df = dataset.df.iloc[:limit].reset_index(drop=True)

    loader = DataLoader(
        dataset,
        batch_size=2,
        shuffle=False,
        num_workers=0
    )

    device = torch.device("cpu")

    torch.set_num_threads(8)

    print("Loading Vision Transformer...")

    model = ViTModel.from_pretrained(MODEL_NAME)

    model.to(device)
    model.eval()

    # Freeze model parameters
    for parameter in model.parameters():
        parameter.requires_grad = False

    all_features = []
    all_labels = []

    print("Starting feature extraction...")

    with torch.inference_mode():

        for batch_number, batch in enumerate(loader, start=1):

            pixel_values = batch["pixel_values"].to(device)

            outputs = model(pixel_values=pixel_values)

            # CLS token: 768-dimensional representation
            features = outputs.last_hidden_state[:, 0, :]

            all_features.append(
                features.cpu().numpy()
            )

            all_labels.append(
                batch["labels"].numpy()
            )

            print(
                f"Processed {min(batch_number * 2, len(dataset))}"
                f"/{len(dataset)} images"
            )

    X = np.concatenate(all_features, axis=0)
    y = np.concatenate(all_labels, axis=0)

    output_path = FEATURE_DIR / f"{split}_features.npz"

    np.savez_compressed(
        output_path,
        features=X,
        labels=y
    )

    print("\n===== FEATURE EXTRACTION RESULT =====")
    print("Split:", split)
    print("Feature Shape:", X.shape)
    print("Label Shape:", y.shape)
    print("Saved:", output_path)
    print("FEATURE EXTRACTION SUCCESSFUL!")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--split",
        choices=["train", "validation", "test"],
        default="train"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20
    )

    args = parser.parse_args()

    extract_features(args.split, args.limit)