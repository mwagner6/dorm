from menu import Menu
import pygame
import sys
mymenu = Menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mymenu.leftInput()
            if event.key == pygame.K_RIGHT:
                mymenu.rightInput()
            if event.key == pygame.K_UP:
                mymenu.upInput()
            if event.key == pygame.K_DOWN:
                mymenu.downInput()
            if event.key == pygame.K_w:
                mymenu.rotaryRight()
            if event.key == pygame.K_s:
                mymenu.rotaryLeft()
        mymenu.createDisplay()