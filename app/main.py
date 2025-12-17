from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io

from app.ocr_service import run_ocr

app = FastAPI()

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    text = run_ocr(image)

    return {
        "text": text
    }
