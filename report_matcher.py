from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dataset" / "iu_xray"


def find_matching_report(image_filename):

    projection_path = next(
        DATA_DIR.rglob("indiana_projections.csv")
    )

    report_path = next(
        DATA_DIR.rglob("indiana_reports.csv")
    )

    projections = pd.read_csv(projection_path)
    reports = pd.read_csv(report_path)

    # Match exact image filename
    matched_image = projections.loc[
        projections["filename"].astype(str).str.strip()
        == Path(image_filename).name.strip()
    ]

    if matched_image.empty:
        return None

    uid = matched_image.iloc[0]["uid"]

    matched_report = reports.loc[
        reports["uid"].astype(str) == str(uid)
    ]

    if matched_report.empty:
        return None

    row = matched_report.iloc[0]

    def clean(value):
        if pd.isna(value):
            return ""
        return str(value).strip()

    sections = [
        "indication",
        "comparison",
        "findings",
        "impression"
    ]

    report_text = "\n\n".join(
        f"{section.upper()}:\n{clean(row[section])}"
        for section in sections
        if section in row and clean(row[section])
    )

    return {
        "uid": str(uid),
        "filename": image_filename,
        "report_text": report_text,
        "pages": [
            {
                "page": 1,
                "text": report_text
            }
        ]
    }


if __name__ == "__main__":

    result = find_matching_report(
        "993_IM-0001-4001.dcm.png"
    )

    if result:
        print("MATCH FOUND!")
        print("UID:", result["uid"])
        print(result["report_text"])
    else:
        print("No matching report found.")