from fastapi import FastAPI, UploadFile, File
from app.ocr_service import run_ocr
from PIL import Image
import io

app = FastAPI()

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return run_ocr(image)
