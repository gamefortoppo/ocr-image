from paddleocr import PaddleOCR
import numpy as np
import cv2

# Load model 1 lần duy nhất
ocr = PaddleOCR(
    lang="japan",          # ✅ EN + VI + JP
    use_angle_cls=False,   # UI & document không cần rotate
    device="cpu"
)

def run_ocr(image_bytes: bytes):
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image")

    result = ocr.ocr(img, cls=False)

    output = []

    if not result or not result[0]:
        return output

    for line in result[0]:
        box_points = line[0]
        text = line[1][0]

        xs = [int(p[0]) for p in box_points]
        ys = [int(p[1]) for p in box_points]

        output.append({
            "text": text,
            "box_2d": [
                min(xs),
                min(ys),
                max(xs),
                max(ys)
            ]
        })

    return output
