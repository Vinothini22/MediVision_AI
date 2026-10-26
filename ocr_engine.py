import easyocr
import streamlit as st
import fitz
import numpy as np
from PIL import Image


@st.cache_resource
def load_ocr():
    return easyocr.Reader(["en"], gpu=False)


def extract_image_text(image):
    reader = load_ocr()

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    image = image.convert("RGB")

    results = reader.readtext(
        np.array(image),
        detail=0,
        paragraph=True
    )

    return "\n".join(results)


def extract_scanned_pdf(uploaded_file):
    pdf = fitz.open(
        stream=uploaded_file.getvalue(),
        filetype="pdf"
    )

    pages = []

    try:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text().strip()

            if not text:
                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2),
                    alpha=False
                )

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                text = extract_image_text(image)

            pages.append({
                "page": page_number,
                "text": text
            })

    finally:
        pdf.close()

    return pages