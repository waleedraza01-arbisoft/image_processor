import io
import cv2
import numpy as np
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_dummy_image():
    # Create a 100x100 black image
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    # Draw a white rectangle (to create edges)
    cv2.rectangle(img, (20, 20), (80, 80), (255, 255, 255), 2)
    # Encode to JPEG bytes
    _, encoded = cv2.imencode('.jpg', img)
    return io.BytesIO(encoded.tobytes())

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "active", "service": "image-processor"}

def test_edge_detection():
    # 1. Create a fake image file
    image_bytes = create_dummy_image()
    
    # 2. Upload it
    response = client.post(
        "/detect-edges",
        files={"file": ("test.jpg", image_bytes, "image/jpeg")}
    )
    
    # 3. Check response
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    # Ensure we got bytes back
    assert len(response.content) > 0

def test_invalid_file_type():
    response = client.post(
        "/detect-edges",
        files={"file": ("test.txt", b"not an image", "text/plain")}
    )
    assert response.status_code == 400