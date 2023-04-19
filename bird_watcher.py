import RPi.GPIO as GPIO
import picamera
import time

SENSOR_PIN = 26
LED_PIN = 6

def capture_image():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        camera.capture(f"Bilder/birdwatcher/bird_{timestamp}.jpg")
        print(f"Image captured: bird_{timestamp}.jpg")

def motion_detected(channel):
    print("Motion detected!")
    GPIO.output(LED_PIN, GPIO.HIGH)
    capture_image()
    GPIO.output(LED_PIN, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Disable warnings

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SENSOR_PIN, GPIO.IN)
GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=motion_detected)

try:
    print("Bird watcher started. Press Ctrl+C to exit.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()