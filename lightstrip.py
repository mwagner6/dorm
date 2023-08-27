# Sample code to demonstrate Encoder class.  Prints the value every 5 seconds, and also whenever it changes.
import time
from rpi_ws281x import *
import RPi.GPIO as GPIO
from encoder import Encoder
import colorsys
led_count = 600
lightstrip_datapin = 18
led_hz = 800000
led_dma = 10
led_brightness = 255
led_invert = False
led_channel = 0

strip = Adafruit_NeoPixel(led_count, lightstrip_datapin, led_hz, led_dma, led_invert, led_brightness, led_channel)
strip.begin()

def valueChanged(value, direction, hue):
    for i in range(led_count):
        strip.setPixelColor(i, hsv2rgb(hue, 100, 100))
    strip.show()
    
def hsv2rgb(h, s, v):
    outvalues = colorsys.hsv_to_rgb(h/360, s/100, v/100)
    return Color(round(outvalues[0] * 255), round(outvalues[1] * 255), round(outvalues[2] * 255))

GPIO.setmode(GPIO.BCM)

e1 = Encoder(23, 17, valueChanged)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    for i in range(led_count):
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
    pass

GPIO.cleanup()
