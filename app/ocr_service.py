from PIL import Image
import pytesseract
import pandas as pd

LANG = "eng+vie+jpn"

def run_ocr(image_bytes):
    image = Image.open(image_bytes).convert("RGB")

    data = pytesseract.image_to_data(
        image,
        lang=LANG,
        config="--oem 3 --psm 6",
        output_type=pytesseract.Output.DATAFRAME
    )

    results = []

    for _, row in data.iterrows():
        text = str(row["text"]).strip()

        if not text or row["conf"] < 0:
            continue

        x1 = int(row["left"])
        y1 = int(row["top"])
        x2 = x1 + int(row["width"])
        y2 = y1 + int(row["height"])

        results.append({
            "text": text,
            "box_2d": [x1, y1, x2, y2],
            "confidence": float(row["conf"])
        })

    return results
