import cv2
import numpy as np
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

app = FastAPI(title="Edge Detection Service")

@app.get("/")
def health_check():
    return {"status": "active", "service": "image-processor"}

@app.post("/detect-edges")
async def detect_edges(file: UploadFile = File(...)):
    # 1. Validate file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload JPEG or PNG.")

    try:
        # 2. Read image bytes
        contents = await file.read()
        
        # 3. Convert bytes to numpy array
        nparr = np.frombuffer(contents, np.uint8)
        
        # 4. Decode image for OpenCV
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 5. Apply Edge Detection (Canny Algorithm)
        # First convert to grayscale (simplifies the math)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply Canny (100 and 200 are threshold values)
        edges = cv2.Canny(gray, 100, 200)
        
        # 6. Encode back to JPEG
        _, encoded_img = cv2.imencode('.jpg', edges)
        
        # 7. Return as a stream (Directly returns the image)
        return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)