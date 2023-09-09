from mixer import Mixer
import pygame
import sys

mixer = Mixer(['water', 'lemon', 'syrup', 'lime'], [10000, 10000, 10000, 10000])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mixer.upInput()
            if event.key == pygame.K_DOWN:
                mixer.downInput()
            if event.key == pygame.K_q:
                mixer.pressInput()
    mixer.createScreen()