import pytesseract
from PIL import Image

LANG_MAP = {
    "en": "eng",
    "vi": "vie",
    "ja": "jpn"
}

DEFAULT_LANG = "eng+vie+jpn"


def resolve_language(lang_param: str | None) -> str:
    """
    Convert query param to tesseract language string
    """
    if not lang_param:
        return DEFAULT_LANG

    langs = []
    for l in lang_param.split(","):
        l = l.strip().lower()
        if l in LANG_MAP:
            langs.append(LANG_MAP[l])

    return "+".join(langs) if langs else DEFAULT_LANG

def run_ocr(image: Image.Image, lang: str):
    # 1️⃣ Full text (native)
    full_text = pytesseract.image_to_string(
        image,
        lang=lang,
        config="--oem 3 --psm 6"
    ).strip()

    # 2️⃣ Word-level + boxes
    data = pytesseract.image_to_data(
        image,
        lang=lang,
        config="--oem 3 --psm 11",
        output_type=pytesseract.Output.DICT
    )

    blocks = []
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

        blocks.append({
            "text": text,
            "box_2d": [x1, y1, x2, y2],
            "confidence": conf
        })

    return {
        "full_text": full_text,
        "blocks": blocks
    }
