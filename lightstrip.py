# Sample code to demonstrate Encoder class.  Prints the value every 5 seconds, and also whenever it changes.
import time
from rpi_ws281x import *
import RPi.GPIO as GPIO
from encoder import Encoder
import colorsys
import pygame
from menu import Menu
import sys
led_count = 600
lightstrip_datapin = 18
led_hz = 800000
led_dma = 10
led_brightness = 255
led_invert = False
led_channel = 0
menu = Menu()

strip = Adafruit_NeoPixel(led_count, lightstrip_datapin, led_hz, led_dma, led_invert, led_brightness, led_channel)
strip.begin()

def valueChanged(value, direction):
    if direction == 'R':
        menu.rotaryRight()
    else:
        menu.rotaryLeft()
    
def hsv2rgb(h, s, v):
    outvalues = colorsys.hsv_to_rgb(h/100, s/100, v/100)
    return Color(round(outvalues[0] * 255), round(outvalues[1] * 255), round(outvalues[2] * 255))

GPIO.setmode(GPIO.BCM)

e1 = Encoder(23, 17, valueChanged)

while True:
    for event in pygame.events.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            for i in range(led_count):
                strip.setPixelColor(i, Color(0, 0, 0))
                strip.show()
            GPIO.cleanup()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                menu.leftInput()
            if event.key == pygame.K_RIGHT:
                menu.rightInput()
            if event.key == pygame.K_UP:
                menu.upInput()
            if event.key == pygame.K_DOWN:
                menu.downInput()
    for i in range(led_count):
        if i % 2 == 0:
            strip.setPixelColor(i, hsv2rgb(menu.h1, menu.s1, menu.v1))
        else:
            strip.setPixelColor(i, hsv2rgb(menu.h2, menu.s2, menu.v2))
    strip.show()
    menu.createDisplay()
