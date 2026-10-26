from pathlib import Path

import pandas as pd
from PIL import Image

import torch
from torch.utils.data import Dataset
from transformers import ViTImageProcessor


MODEL_NAME = "google/vit-base-patch16-224-in21k"


class XRayDataset(Dataset):

    def __init__(self, csv_path):

        self.df = pd.read_csv(csv_path)

        required = {"image_path", "label"}

        if not required.issubset(self.df.columns):
            raise ValueError(
                "Required columns are missing."
            )

        self.processor = ViTImageProcessor.from_pretrained(
            MODEL_NAME
        )

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):

        row = self.df.iloc[index]

        image_path = Path(row["image_path"])

        if not image_path.is_file():
            raise FileNotFoundError(image_path)

        with Image.open(image_path) as img:
            image = img.convert("RGB")

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        pixel_values = inputs["pixel_values"].squeeze(0)

        label = torch.tensor(
            int(row["label"]),
            dtype=torch.long
        )

        return {
            "pixel_values": pixel_values,
            "labels": label
        }


if __name__ == "__main__":

    csv_path = (
        Path(__file__).resolve().parent
        / "dataset"
        / "iu_xray"
        / "processed"
        / "train_labeled.csv"
    )

    dataset = XRayDataset(csv_path)

    sample = dataset[0]

    print("\n===== DATASET LOADING TEST =====")

    print("Total Images:", len(dataset))

    print(
        "Image Tensor Shape:",
        sample["pixel_values"].shape
    )

    print(
        "Sample Label:",
        sample["labels"].item()
    )

    print("\nDATASET LOADING SUCCESSFUL!")