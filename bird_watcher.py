import os
import time
import picamera
import RPi.GPIO as GPIO
from datetime import datetime

# Configure the motion sensor
SENSOR_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# Configure the camera
camera = picamera.PiCamera()
camera.resolution = (1024, 768)

def capture_image():
    # Generate a unique filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"bird_{timestamp}.jpg"
    
    # Capture and save the image
    camera.capture(filename)
    print(f"Image captured: {filename}")

def on_motion_detected(channel):
    print("Motion detected!")
    capture_image()

# Set up the motion detection callback
GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=on_motion_detected)

try:
    print("Bird watcher started. Press Ctrl+C to exit.")
    while True:
        print(f"Motion sensor pin state: {GPIO.input(SENSOR_PIN)}")
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Exiting...")
    
finally:
    GPIO.cleanup()
