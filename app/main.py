from fastapi import FastAPI, UploadFile, File, Query
from app.ocr_service import run_ocr, resolve_language
from PIL import Image
import io

app = FastAPI()

@app.post("/ocr")
async def ocr_endpoint(
    file: UploadFile = File(...),
    language: str | None = Query(
        default=None,
        description="en, vi, ja or en,ja"
    )
):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    lang = resolve_language(language)
    result = run_ocr(image, lang)

    return {
        "language_used": lang,
        **result
    }
