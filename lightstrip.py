# Sample code to demonstrate Encoder class.  Prints the value every 5 seconds, and also whenever it changes.
import time
from rpi_ws281x import *
import RPi.GPIO as GPIO
from encoder import Encoder
import colorsys
import pygame
from controller import Controller
import sys
led_count = 600
lightstrip_datapin = 18
led_hz = 800000
led_dma = 10
led_brightness = 255
led_invert = False
led_channel = 0
controller = Controller(led_count)

strip = Adafruit_NeoPixel(led_count, lightstrip_datapin, led_hz, led_dma, led_invert, led_brightness, led_channel)
strip.begin()

def valueChanged(value, direction):
    if direction == 'R':
        controller.rotaryRight()
    else:
        controller.rotaryLeft()
    
def hsv2rgb(h, s, v):
    outvalues = colorsys.hsv_to_rgb(h/100, s/100, v/100)
    return Color(round(outvalues[0] * 255), round(outvalues[1] * 255), round(outvalues[2] * 255))

GPIO.setmode(GPIO.BCM)

e1 = Encoder(23, 17, valueChanged)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            for i in range(led_count):
                strip.setPixelColor(i, Color(0, 0, 0))
                strip.show()
            GPIO.cleanup()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                controller.leftInput()
            if event.key == pygame.K_RIGHT:
                controller.rightInput()
            if event.key == pygame.K_UP:
                controller.upInput()
            if event.key == pygame.K_DOWN:
                controller.downInput()
            if event.key == pygame.K_KP_ENTER:
                controller.clickInput()
    controller.advancePatterns()
    controller.updateStrip(strip)
    controller.createDisplay()
