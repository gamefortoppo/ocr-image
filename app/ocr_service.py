from PIL import Image
import pytesseract

LANG = "eng+vie+jpn"

def run_ocr(image_bytes):
    image = Image.open(image_bytes).convert("RGB")

    data = pytesseract.image_to_data(
        image,
        lang=LANG,
        config="--oem 3 --psm 6",
        output_type=pytesseract.Output.DICT
    )

    results = []

    n = len(data["text"])

    for i in range(n):
        text = data["text"][i].strip()
        conf = int(data["conf"][i])

        if not text or conf < 0:
            continue

        x1 = int(data["left"][i])
        y1 = int(data["top"][i])
        x2 = x1 + int(data["width"][i])
        y2 = y1 + int(data["height"][i])

        results.append({
            "text": text,
            "box_2d": [x1, y1, x2, y2],
            "confidence": conf
        })

    return results
