import pygame
import numpy as np
import colorsys
from rpi_ws281x import *


class Controller:
    def __init__(self, npixels):
        self.sections = ["Pattern", "Color 1", "Color 2"]
        self.currentSection = 0
        self.columnpos = 0
        self.npixels = npixels
        self.menus = {"Pattern": ["rainbow", "singlecolor", "stars", "gradient", "breathing", "twocolor"], "Color 1": ["hbar1", "sbar1", "vbar1"], "Color 2": ["hbar2", "sbar2", "vbar2"]}
        self.indices = {"rainbow": np.zeros((npixels, 3), dtype=np.uint8), "singlecolor": np.zeros((npixels, 3), dtype=np.uint8), "stars": np.zeros((npixels, 3), dtype=np.uint8), "gradient": np.zeros((npixels, 3), dtype=np.uint8), "breathing": np.zeros((npixels, 3), dtype=np.uint8), "twocolor": np.zeros((npixels, 3), dtype=np.uint8)}
        self.currentpattern = 'twocolor'
        self.h1 = 0
        self.s1 = 0
        self.v1 = 0
        self.h2 = 0
        self.s2 = 0
        self.v2 = 0
        self.currentItem = None
        pygame.init()
        self.screen = pygame.display.set_mode((800, 480))

    def hsv2rgb_pg(self, h, s, v):
        outvalues = colorsys.hsv_to_rgb(h / 100, s / 100, v / 100)
        return (round(outvalues[0] * 255), round(outvalues[1] * 255), round(outvalues[2] * 255))
    
    def updateStrip(self, strip):
        for i in range(self.npixels):
            current = self.indices[self.currentpattern][i]
            strip.setPixelColor(i, Color(self.indices[self.currentpattern][i, 0], self.indices[self.currentpattern][i, 1], self.indices[self.currentpattern][i, 2]))
        strip.show()

    def advancePatterns(self):
        if self.currentpattern == 'twocolor':
            for i in range(self.npixels):
                if i % 2 == 0:
                    colors = self.hsv2rgb_pg(self.h1, self.s1, self.v1)
                else:
                    colors = self.hsv2rgb_pg(self.h2, self.s2, self.v2)
                self.indices[self.currentpattern][i, 0] = colors[0]
                self.indices[self.currentpattern][i, 1] = colors[1]
                self.indices[self.currentpattern][i, 2] = colors[2]

    def rightInput(self):
        if self.currentItem == None:
            self.columnpos = 0
            self.currentItem = self.menus[self.sections[self.currentSection]][self.columnpos]

    def leftInput(self):
        if self.currentItem != None:
            self.currentItem = None

    def upInput(self):
        if self.currentItem != None:
            menuItems = len(self.menus[self.sections[self.currentSection]])
            self.columnpos -= 1
            if self.columnpos < 0:
                self.columnpos = menuItems - 1
            self.currentItem = self.menus[self.sections[self.currentSection]][self.columnpos]
        else:
            self.currentSection -= 1
            if self.currentSection < 0:
                self.currentSection = len(self.sections) - 1

    def downInput(self):
        if self.currentItem != None:
            menuItems = len(self.menus[self.sections[self.currentSection]])
            self.columnpos += 1
            if self.columnpos == menuItems:
                self.columnpos = 0
            self.currentItem = self.menus[self.sections[self.currentSection]][self.columnpos]
        else:
            self.currentSection += 1
            if self.currentSection == len(self.sections):
                self.currentSection = 0
    
    def clickInput(self):
        if self.currentSection == 0 and self.currentItem is not None:
            self.currentpattern = self.currentItem

    def rotaryRight(self):
        if self.currentItem == "hbar1":
            self.h1 += 4
            if self.h1 > 100:
                self.h1 -= 100
        if self.currentItem == "sbar1":
            self.s1 += 4
            if self.s1 > 100:
                self.s1 -= 100
        if self.currentItem == "vbar1":
            self.v1 += 4
            if self.v1 > 100:
                self.v1 -= 100
        if self.currentItem == "hbar2":
            self.h2 += 4
            if self.h2 > 100:
                self.h2 -= 100
        if self.currentItem == "sbar2":
            self.s2 += 4
            if self.s2 > 100:
                self.s2 -= 100
        if self.currentItem == "vbar2":
            self.v2 += 4
            if self.v2 > 100:
                self.v2 -= 100

    def rotaryLeft(self):
        if self.currentItem == "hbar1":
            self.h1 -= 4
            if self.h1 < 0:
                self.h1 += 100
        if self.currentItem == "sbar1":
            self.s1 -= 4
            if self.s1 < 0:
                self.s1 += 100
        if self.currentItem == "vbar1":
            self.v1 -= 4
            if self.v1 < 0:
                self.v1 += 100
        if self.currentItem == "hbar2":
            self.h2 -= 4
            if self.h2 < 0:
                self.h2 += 100
        if self.currentItem == "sbar2":
            self.s2 -= 4
            if self.s2 < 0:
                self.s2 += 100
        if self.currentItem == "vbar2":
            self.v2 -= 4
            if self.v2 < 0:
                self.v2 += 100

    def createDisplay(self):
        self.screen.fill((0, 0, 0))
        font_name = "ShareTechMono-Regular.ttf"
        font = pygame.font.Font(font_name, 50)
        for leftItem in range(len(self.sections)):
            if leftItem == self.currentSection:
                text = font.render(self.sections[leftItem], False, (0, 0, 0))
                textRect = text.get_rect()
                textRect.topleft = (0, 50 * leftItem)
                pygame.draw.rect(self.screen, (255, 255, 255), textRect)
                self.screen.blit(text, textRect)
            else:
                text = font.render(self.sections[leftItem], False, (255, 255, 255))
                textRect = text.get_rect()
                textRect.topleft = (0, 50 * leftItem)
                self.screen.blit(text, textRect)
        barRect = pygame.Rect(390, 0, 20, 480)
        pygame.draw.rect(self.screen, (255, 255, 255), barRect)

        if self.currentItem != None:
            rightList = self.menus[self.sections[self.currentSection]]
            for rightItem in range(len(rightList)):
                if "bar" in rightList[rightItem]:
                    if rightItem == self.columnpos:
                        outerRect = pygame.Rect(410, 110 * rightItem, 310, 110)
                        pygame.draw.rect(self.screen, (255, 255, 255), outerRect)
                    if "1" in rightList[rightItem]:
                        if rightList[rightItem][0] == "h":
                            for h in range(100):
                                hRect = pygame.Rect(415 + (3 * h), 5 + (110 * rightItem), 3, 100)
                                pygame.draw.rect(self.screen, self.hsv2rgb_pg(h, self.s1, self.v1), hRect)
                                if h == self.h1:
                                    pygame.draw.rect(self.screen, (255, 255, 255), hRect)
                        if rightList[rightItem][0] == "s":
                            for s in range(100):
                                sRect = pygame.Rect(415 + (3 * s), 5 + (110 * rightItem), 3, 100)
                                pygame.draw.rect(self.screen, self.hsv2rgb_pg(self.h1, s, self.v1), sRect)
                                if s == self.s1:
                                    pygame.draw.rect(self.screen, (255, 255, 255), sRect)
                        if rightList[rightItem][0] == "v":
                            for v in range(100):
                                vRect = pygame.Rect(415 + (3 * v), 5 + (110 * rightItem), 3, 100)
                                pygame.draw.rect(self.screen, self.hsv2rgb_pg(self.h1, self.s1, v), vRect)
                                if v == self.v1:
                                    pygame.draw.rect(self.screen, (255, 255, 255), vRect)
                    if "2" in rightList[rightItem]:
                        if rightList[rightItem][0] == "h":
                            for h in range(100):
                                hRect = pygame.Rect(415 + (3 * h), 5 + (110 * rightItem), 3, 100)
                                pygame.draw.rect(self.screen, self.hsv2rgb_pg(h, self.s2, self.v2), hRect)
                                if h == self.h2:
                                    pygame.draw.rect(self.screen, (255, 255, 255), hRect)
                        if rightList[rightItem][0] == "s":
                            for s in range(100):
                                sRect = pygame.Rect(415 + (3 * s), 5 + (110 * rightItem), 3, 100)
                                pygame.draw.rect(self.screen, self.hsv2rgb_pg(self.h2, s, self.v2), sRect)
                                if s == self.s2:
                                    pygame.draw.rect(self.screen, (255, 255, 255), sRect)
                        if rightList[rightItem][0] == "v":
                            for v in range(100):
                                vRect = pygame.Rect(415 + (3 * v), 5 + (110 * rightItem), 3, 100)
                                pygame.draw.rect(self.screen, self.hsv2rgb_pg(self.h2, self.s2, v), vRect)
                                if v == self.v2:
                                    pygame.draw.rect(self.screen, (255, 255, 255), vRect)
                else:
                    if rightItem == self.columnpos:
                        text = font.render(rightList[rightItem], False, (0, 0, 0))
                        textRect = text.get_rect()
                        textRect.topleft = (410, 50 * rightItem)
                        pygame.draw.rect(self.screen, (255, 255, 255), textRect)
                        self.screen.blit(text, textRect)
                    else:
                        text = font.render(rightList[rightItem], False, (255, 255, 255))
                        textRect = text.get_rect()
                        textRect.topleft = (410, 50 * rightItem)
                        self.screen.blit(text, textRect)

        pygame.display.flip()
