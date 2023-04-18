import RPi.GPIO as GPIO
import time

SENSOR_PIN = 26
LED_PIN = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

def motion_detected(channel):
    print("Motion detected!")
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED_PIN, GPIO.LOW)

GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=motion_detected)

try:
    print("PIR motion sensor test with LED. Press Ctrl+C to exit.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()