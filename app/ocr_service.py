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
    data = pytesseract.image_to_data(
        image,
        lang=lang,
        config="--oem 3 --psm 11",
        output_type=pytesseract.Output.DICT
    )

    blocks = []
    full_text_lines = []

    n = len(data["text"])

    current_line = []
    last_line_num = -1

    for i in range(n):
        text = data["text"][i].strip()
        conf = int(data["conf"][i])
        line_num = data["line_num"][i]

        if not text or conf < 0:
            continue

        x1 = int(data["left"][i])
        y1 = int(data["top"][i])
        x2 = x1 + int(data["width"][i])
        y2 = y1 + int(data["height"][i])

        # 1️⃣ box-level (word)
        blocks.append({
            "text": text,
            "box_2d": [x1, y1, x2, y2],
            "confidence": conf,
            "line_num": line_num
        })

        # 2️⃣ line-level (sentence)
        if line_num != last_line_num:
            if current_line:
                full_text_lines.append(" ".join(current_line))
            current_line = [text]
            last_line_num = line_num
        else:
            current_line.append(text)

    if current_line:
        full_text_lines.append(" ".join(current_line))

    return {
        "full_text": "\n".join(full_text_lines),
        "blocks": blocks
    }
