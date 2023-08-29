import cv2
import numpy as np
from controller import Controller

# Sample code to demonstrate Encoder class.  Prints the value every 5 seconds, and also whenever it changes.
import time
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

def valueChanged(value, direction):
    if direction == 'R':
        controller.rotaryRight()
    else:
        controller.rotaryLeft()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
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
            if event.key == pygame.K_q:
                controller.clickInput()
            if event.key == pygame.K_a:
                valueChanged(0, 'L')
            if event.key == pygame.K_s:
                valueChanged(0, 'R')
    controller.advancePatterns()
    img = controller.simImg()
    cv2.imshow('simulation', cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB))
    controller.createDisplay()
