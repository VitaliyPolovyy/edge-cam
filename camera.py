from picamera2 import Picamera2
import time
from pathlib import Path
import uuid

class CameraController:
    def __init__(self, resolution=(1920, 1080)):
        self.picam2 = Picamera2()
        self.configure(resolution)
        
    def configure(self, resolution):
        config = self.picam2.create_still_configuration(main={"size": resolution})
        self.picam2.configure(config)
        
    def start(self):
        self.picam2.start()
        # Give camera time to adjust
        time.sleep(0.5)
        
    def stop(self):
        self.picam2.stop()
        
    def capture_image(self, save_path=None, filename=None, format="jpeg"):
        if not self.picam2.started:
            self.start()
            
        if not filename:
            filename = f"{uuid.uuid4()}.{format}"
            
        if save_path:
            path = Path(save_path)
            path.mkdir(exist_ok=True)
            file_path = path / filename
            self.picam2.capture_file(str(file_path), format=format)
            return str(file_path)
        else:
            # Return image as bytes
            return self.picam2.capture_array()
        
      

def main():
    picam2 = Picamera2(camera_num=0)  # Try 0, or iterate through cameras
    config = picam2.create_still_configuration()
    picam2.configure(config)
    picam2.start()
    picam2.capture_file("test_image.jpg")
    print("Image captured successfully!")


    picam2.capture_file("test_image.jpg")
    picam2.stop()
    print("Image captured successfully!")


if __name__ == "__main__":
    main()
    
