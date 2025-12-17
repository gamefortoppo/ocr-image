from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.ocr_service import run_ocr

app = FastAPI(title="PaddleOCR Backend")

# Allow website outside call this BE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # sau này có thể giới hạn domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()

    try:
        result = run_ocr(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
