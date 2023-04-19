import RPi.GPIO as GPIO
import time
import os
import signal
import subprocess

BUTTON_PIN = 27
LED_PIN = 17
bird_watcher_process = None

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

def button_callback(channel):
    print("button pressed")
    global bird_watcher_process

    if bird_watcher_process is None:
        print("Starting bird_watcher.py")
        bird_watcher_process = subprocess.Popen(["python3", "bird_watcher.py"])
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        print("Terminating bird_watcher.py")
        bird_watcher_process.terminate()
        bird_watcher_process = None
        GPIO.output(LED_PIN, GPIO.LOW)

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    print("Waiting for button press. Press Ctrl+C to exit.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    if bird_watcher_process is not None:
        bird_watcher_process.terminate()
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
