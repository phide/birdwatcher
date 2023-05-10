import os
import asyncio
import RPi.GPIO as GPIO
import picamera
import time
from telegram import InputFile
from telegram import Bot
from telegram.ext import Updater

# Replace the following variable with your bot token
TELEGRAM_BOT_TOKEN = "###"

# Replace the following variable with the chat ID of your Telegram channel
# To get the chat ID, add your bot to the channel as an admin and send a message to the channel.
# Check the updates on https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN>/getUpdates
TELEGRAM_CHANNEL_CHAT_ID = "-1001539604283"

#updater = Updater(TELEGRAM_BOT_TOKEN, update_queue=False)
#bot = updater.bot
bot = Bot(TELEGRAM_BOT_TOKEN)

SENSOR_PIN = 26
LED_PIN = 6

def capture_image():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"bird_{timestamp}.jpg"
        camera.capture(filename)
        print(f"Image captured: {filename}")
        return filename
    
async def send_image_to_telegram(filename):
    with open(filename, 'rb') as f:
        await bot.send_photo(chat_id=TELEGRAM_CHANNEL_CHAT_ID, photo=InputFile(f))


async def motion_detected(channel):
    print("Motion detected!")
    GPIO.output(LED_PIN, GPIO.HIGH)
    image_filename = capture_image()
    GPIO.output(LED_PIN, GPIO.LOW)
    await send_image_to_telegram(image_filename)
    os.remove(image_filename)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Disable warnings

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SENSOR_PIN, GPIO.IN)
GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=motion_detected)

print("Bird watcher started. Press Ctrl+C to exit.")
GPIO.add_event_detect(MOTION_SENSOR_PIN, GPIO.RISING, callback=lambda x: asyncio.run_coroutine_threadsafe(motion_detected(x), loop), bouncetime=2000)
loop = asyncio.get_event_loop()
try:
    loop.run_forever()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    loop.close()
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()