import RPi.GPIO as GPIO
import time

SENSOR_PIN = 26  # Change this to the GPIO pin you are using for the motion sensor

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def motion_detected(channel):
    print("Motion detected!")

GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=motion_detected)

try:
    print("PIR motion sensor test. Press Ctrl+C to exit.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()