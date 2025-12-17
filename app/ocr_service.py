from PIL import Image
import pytesseract

def run_ocr(image: Image.Image) -> str:
    return pytesseract.image_to_string(
        image,
        lang="eng+vie+jpn",
        config="--oem 3 --psm 6"
    )
