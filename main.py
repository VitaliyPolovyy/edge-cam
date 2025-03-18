import atexit
import signal
import sys
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io
import time
from PIL import Image
import uvicorn
from camera import CameraController

# Create FastAPI app
app = FastAPI(title="Minimal Camera API")

# Initialize global camera controller

camera = None
try:
    camera = CameraController(resolution=(4608, 2592))
    #camera = CameraController(resolution=(1920, 1080))
    camera.start()
    print("Camera initialized and started")
except Exception as e:
    print(f"Camera initialization failed: {e}")
    sys.exit(1)


# Handle graceful shutdown
def signal_handler(sig, frame):
    print("Shutting down camera...")
    if camera:
        camera.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


@app.get("/")
async def root():
    return {"message": "Camera API running. Use /capture to take a photo."}

@app.get("/capture")
async def capture_image():
    try:
        img_array = camera.capture_image()
        img = Image.fromarray(img_array)
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        
        return StreamingResponse(content=img_io, media_type="image/jpeg")
    


    except Exception as e:
        print(f"Error capturing image: {e}")
        return {"error": str(e)}

# Register cleanup function 

def cleanup():
    if camera:
        print("Cleaning up camera resources...")
        try:
            camera.stop()
            print("Camera stopped successfully")
        except Exception as e:
            print(f"Error stopping camera: {e}")


atexit.register(cleanup)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
    