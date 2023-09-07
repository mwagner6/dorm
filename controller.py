import pygame
import random
import numpy as np
import colorsys
from datetime import datetime
try:
    from rpi_ws281x import *
except:
    pass


class Controller:
    def __init__(self, npixels):
        self.sections = ["Pattern", "Color 1", "Color 2", "Add Colors", "Clear Colors", "Brightness", "Wake Time"]
        self.brightness = 1
        self.currentSection = 0
        self.columnpos = 0
        self.npixels = npixels
        self.menus = {"Pattern": ["rainbow", "singlecolor", "stars", "gradient", "breathing", "twocolor", "shootertrails", "shooters", "wakeup"], "Color 1": ["hbar1", "sbar1", "vbar1"], "Color 2": ["hbar2", "sbar2", "vbar2"], "Add Colors": ["hbarS", "sbarS", "vbarS"], "Clear Colors": ["Reset Colors"], "Brightness": ['Bbar'], "Waketime":["wakeTime"]}
        self.indices = {"rainbow": np.zeros((npixels, 3), dtype=np.uint8), "singlecolor": np.zeros((npixels, 3), dtype=np.uint8), "stars": np.zeros((npixels, 3), dtype=np.uint8), "gradient": np.zeros((npixels, 3), dtype=np.uint8), "breathing": np.zeros((npixels, 3), dtype=np.uint8), "twocolor": np.zeros((npixels, 3), dtype=np.uint8), "shootertrails": np.zeros((npixels, 3), dtype=np.uint8), "shooters": np.zeros((npixels, 3), dtype=np.uint8), "wakeup": np.zeros((npixels, 3))}
        self.stars = []
        self.shooters = []
        self.wakeH = 12
        self.wakeM = 30
        self.shootertimer = 0
        self.currentcolor = 0
        self.currentpattern = 'rainbow'
        self.positioncounter = 0
        self.h1 = 0
        self.s1 = 0
        self.v1 = 0
        self.h2 = 0
        self.s2 = 0
        self.v2 = 0
        self.listColors = []
        self.selectingH = 0
        self.selectingS = 0
        self.selectingV = 0
        self.currentItem = None
        pygame.init()
        self.screen = pygame.display.set_mode((800, 480))

    def hsv2rgb_pg(self, h, s, v):
        outvalues = colorsys.hsv_to_rgb(h / 100, s / 100, v / 100)
        return (round(outvalues[0] * 255), round(outvalues[1] * 255), round(outvalues[2] * 255))
    
    def updateStrip(self, strip):
        for i in range(self.npixels):
            current = self.indices[self.currentpattern][i]
            strip.setPixelColor(i, Color(int(self.indices[self.currentpattern][i, 0] * self.brightness), int(self.indices[self.currentpattern][i, 1] * self.brightness), int(self.indices[self.currentpattern][i, 2] * self.brightness)))
        strip.show()
    
    def simImg(self):
        img = np.zeros((1270, 1770, 3))
        for i in range(175):
            img[0:10, 10*(i+1):10*(i+2), 0] = self.indices[self.currentpattern][i, 0]
            img[0:10, 10*(i+1):10*(i+2), 1] = self.indices[self.currentpattern][i, 1]
            img[0:10, 10*(i+1):10*(i+2), 2] = self.indices[self.currentpattern][i, 2]
        for i in range(125):
            img[10*(i+1):10*(i+2), 1760:1770, 0] = self.indices[self.currentpattern][i+175, 0]
            img[10*(i+1):10*(i+2), 1760:1770, 1] = self.indices[self.currentpattern][i+175, 1]
            img[10*(i+1):10*(i+2), 1760:1770, 2] = self.indices[self.currentpattern][i+175, 2]
        for i in range(175):
            img[1260:1270, 10*(174-i):10*(175-i), 0] = self.indices[self.currentpattern][i+300, 0]
            img[1260:1270, 10*(174-i):10*(175-i), 1] = self.indices[self.currentpattern][i+300, 1]
            img[1260:1270, 10*(174-i):10*(175-i), 2] = self.indices[self.currentpattern][i+300, 2]
        for i in range(125):
            img[10*(124-i):10*(125-i), 0:10, 0] = self.indices[self.currentpattern][i+475, 0]
            img[10*(124-i):10*(125-i), 0:10, 1] = self.indices[self.currentpattern][i+475, 1]
            img[10*(124-i):10*(125-i), 0:10, 2] = self.indices[self.currentpattern][i+475, 2]
        return img
    
    def advancePatterns(self):
        if self.currentpattern == 'rainbow':
            self.positioncounter += 1
            if self.positioncounter > 100:
                self.positioncounter -= 100
            for i in range(self.npixels):
                h = (i+self.positioncounter) % 100
                rgbvals = self.hsv2rgb_pg(h, 100, 100)
                self.indices['rainbow'][i, 0] = rgbvals[0]
                self.indices['rainbow'][i, 1] = rgbvals[1] 
                self.indices['rainbow'][i, 2] = rgbvals[2]

        if self.currentpattern == 'singlecolor':
            for i in range(self.npixels):
                colors = self.hsv2rgb_pg(self.h1, self.s1, self.v1)
                self.indices[self.currentpattern][i, 0] = colors[0]
                self.indices[self.currentpattern][i, 1] = colors[1]
                self.indices[self.currentpattern][i, 2] = colors[2]

        if self.currentpattern == 'stars':
            lightvals = [0] * self.npixels
            for i in range(self.npixels):
                if random.random() < 0.0005:
                    self.stars.append([i, 100])
            for star in self.stars:
                star[1] -= 1
                for d in range(-3, 4):
                    dist = abs(d)
                    if star[0]+d < len(lightvals) and star[0]+d >= 0:
                        lightvals[star[0]+d] += (0.3 ** dist) * star[1]/100
            for i in range(self.npixels):
                if lightvals[i] > 1:
                    lightvals[i] = 1
                colors1 = self.hsv2rgb_pg(self.h1, self.s1, self.v1)
                colors2 = self.hsv2rgb_pg(self.h2, self.s2, self.v2)
                self.indices[self.currentpattern][i, 0] = lightvals[i] * colors1[0] + (1-lightvals[i]) * colors2[0]
                self.indices[self.currentpattern][i, 1] = lightvals[i] * colors1[1] + (1-lightvals[i]) * colors2[1]
                self.indices[self.currentpattern][i, 2] = lightvals[i] * colors1[2] + (1-lightvals[i]) * colors2[2]
            remindices = []
            for i in range(len(self.stars)):
                star = self.stars[i]
                if star[1] == 0:
                    remindices.append(i)
            for index in sorted(remindices, reverse=True):
                del self.stars[index]

        if self.currentpattern == 'gradient':
            self.positioncounter += 1
            if self.positioncounter > 100 * np.pi:
                self.positioncounter = 0
            for i in range(self.npixels):
                sinpos = (self.positioncounter + i) / 50
                val = 0.5 + (np.sin(sinpos) / 2)
                colors1 = self.hsv2rgb_pg(self.h1, self.s1, self.v1)
                colors2 = self.hsv2rgb_pg(self.h2, self.s2, self.v2)
                self.indices[self.currentpattern][i, 0] = val * colors1[0] + (1-val) * colors2[0]
                self.indices[self.currentpattern][i, 1] = val * colors1[1] + (1-val) * colors2[1]
                self.indices[self.currentpattern][i, 2] = val * colors1[2] + (1-val) * colors2[2]
        
        if self.currentpattern == 'breathing':
            self.positioncounter += 1
            if self.positioncounter > 200:
                self.positioncounter = 0
            if self.positioncounter < 100:
                sinpos = self.positioncounter * np.pi / 100
                color = self.hsv2rgb_pg(self.h1, self.s1, self.v1)
            else:
                sinpos = (self.positioncounter - 100) * np.pi / 100
                color = self.hsv2rgb_pg(self.h2, self.s2, self.v2)
            for i in range(self.npixels):
                val = abs(np.sin(sinpos))
                self.indices[self.currentpattern][i, 0] = val * color[0]
                self.indices[self.currentpattern][i, 1] = val * color[1]
                self.indices[self.currentpattern][i, 2] = val * color[2]

        if self.currentpattern == 'twocolor':
            for i in range(self.npixels):
                if i % 2 == 0:
                    colors = self.hsv2rgb_pg(self.h1, self.s1, self.v1)
                else:
                    colors = self.hsv2rgb_pg(self.h2, self.s2, self.v2)
                self.indices[self.currentpattern][i, 0] = colors[0]
                self.indices[self.currentpattern][i, 1] = colors[1]
                self.indices[self.currentpattern][i, 2] = colors[2]
        
        if self.currentpattern == 'shootertrails':
            self.shootertimer += 1
            if self.shootertimer == 60:
                self.currentcolor += 1
                if self.currentcolor > 1 + len(self.listColors):
                    self.currentcolor = 0
                if self.currentcolor < len(self.listColors):
                    currentColor = self.hsv2rgb_pg(self.listColors[self.currentcolor][0], self.listColors[self.currentcolor][1], self.listColors[self.currentcolor][2])
                elif self.currentcolor == len(self.listColors):
                    currentColor = self.hsv2rgb_pg(self.h1, self.s1, self.v1)
                else:
                    currentColor = self.hsv2rgb_pg(self.h2, self.s2, self.v2)
                self.shootertimer = 0
                self.shooters.insert(0, [0, currentColor])
            for shooter in self.shooters:
                shooter[0] += 1
                if shooter[0] == self.npixels:
                    del shooter
                else:
                    for i in range(0, 6):
                        if shooter[0]-i >= self.npixels-2:
                            continue
                        if shooter[1][0] * (0.4 ** i) > 1 or shooter[1][1] * (0.4 ** i) > 1 or shooter[1][2] * (0.4 ** i) > 1:
                            self.indices[self.currentpattern][shooter[0]-i, 0] = shooter[1][0] * (0.4 ** i)
                            self.indices[self.currentpattern][shooter[0]-i, 1] = shooter[1][1] * (0.4 ** i)
                            self.indices[self.currentpattern][shooter[0]-i, 2] = shooter[1][2] * (0.4 ** i)
                        else:
                            break
                    
        
        if self.currentpattern == 'shooters':
            self.shootertimer += 1
            if self.shootertimer == 60:
                self.currentcolor += 1
                if self.currentcolor > 1 + len(self.listColors):
                    self.currentcolor = 0
                if self.currentcolor < len(self.listColors):
                    currentColor = self.hsv2rgb_pg(self.listColors[self.currentcolor][0], self.listColors[self.currentcolor][1], self.listColors[self.currentcolor][2])
                elif self.currentcolor == len(self.listColors):
                    currentColor = self.hsv2rgb_pg(self.h1, self.s1, self.v1)
                else:
                    currentColor = self.hsv2rgb_pg(self.h2, self.s2, self.v2)
                self.shootertimer = 0
                self.shooters.insert(0, [0, currentColor])
            for shooter in self.shooters:
                shooter[0] += 1
                if shooter[0] == self.npixels:
                    del shooter
                else:
                    for i in range(0, 15):
                        if shooter[0]-i >= self.npixels-2:
                            continue
                        self.indices[self.currentpattern][shooter[0]-i, 0] = shooter[1][0] * (0.4 ** i)
                        self.indices[self.currentpattern][shooter[0]-i, 1] = shooter[1][1] * (0.4 ** i)
                        self.indices[self.currentpattern][shooter[0]-i, 2] = shooter[1][2] * (0.4 ** i)
        
        if self.currentpattern == 'wakeup':
            now = datetime.now()
            midnight = now.replace(hour=0, minute=0, second=0)
            minutespassed = (now-midnight).seconds / 60
            waketimeMin = self.wakeH * 60 + self.wakeM
            sunColor = [250, 235, 158]
            if minutespassed > waketimeMin - 30:
                scaleUp = (minutespassed - waketimeMin) * 1/30
                if scaleUp > 1:
                    scaleUp = 1
                print(int(scaleUp * sunColor[0]))
                for i in range(self.npixels):
                    self.indices[self.currentpattern][i, 0] = int(scaleUp * sunColor[0])
                    self.indices[self.currentpattern][i, 1] = int(scaleUp * sunColor[1])
                    self.indices[self.currentpattern][i, 2] = int(scaleUp * sunColor[2])
                    

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
        if self.currentSection == 3 and self.currentItem is not None:
            self.listColors.append([self.selectingH, self.selectingS, self.selectingV])
            self.selectingH = 0
            self.selectingS = 0
            self.selectingV = 0
        if self.currentSection == 4 and self.currentItem is not None:
            self.listColors = []

    def rotaryRight(self):
        if self.currentItem == "hbar1":
            self.h1 += 1
            if self.h1 > 100:
                self.h1 -= 100
        if self.currentItem == "sbar1":
            self.s1 += 1
            if self.s1 > 100:
                self.s1 -= 100
        if self.currentItem == "vbar1":
            self.v1 += 1
            if self.v1 > 100:
                self.v1 -= 100
        if self.currentItem == "hbar2":
            self.h2 += 1
            if self.h2 > 100:
                self.h2 -= 100
        if self.currentItem == "sbar2":
            self.s2 += 1
            if self.s2 > 100:
                self.s2 -= 100
        if self.currentItem == "vbar2":
            self.v2 += 1
            if self.v2 > 100:
                self.v2 -= 100
        if self.currentItem == "hbarS":
            self.selectingH += 1
            if self.selectingH > 100:
                self.selectingH -= 100
        if self.currentItem == "sbarS":
            self.selectingS += 1
            if self.selectingS > 100:
                self.selectingS -= 100
        if self.currentItem == "vbarS":
            self.selectingV += 1
            if self.selectingV > 100:
                self.selectingV -= 100
        if self.currentItem == "Bbar" and self.brightness < 1:
            self.brightness += 0.02

    def rotaryLeft(self):
        if self.currentItem == "hbar1":
            self.h1 -= 1
            if self.h1 < 0:
                self.h1 += 100
        if self.currentItem == "sbar1":
            self.s1 -= 1
            if self.s1 < 0:
                self.s1 += 100
        if self.currentItem == "vbar1":
            self.v1 -= 1
            if self.v1 < 0:
                self.v1 += 100
        if self.currentItem == "hbar2":
            self.h2 -= 1
            if self.h2 < 0:
                self.h2 += 100
        if self.currentItem == "sbar2":
            self.s2 -= 1
            if self.s2 < 0:
                self.s2 += 100
        if self.currentItem == "vbar2":
            self.v2 -= 1
            if self.v2 < 0:
                self.v2 += 100
        if self.currentItem == "hbarS":
            self.selectingH -= 1
            if self.selectingH < 0:
                self.selectingH += 100
        if self.currentItem == "sbarS":
            self.selectingS -= 1
            if self.selectingS < 0:
                self.selectingS += 100
        if self.currentItem == "vbarS":
            self.selectingV -= 1
            if self.selectingV < 0:
                self.selectingV += 100
        if self.currentItem == "Bbar" and self.brightness > 0:
            self.brightness -= 0.02 

    def createDisplay(self):
        self.screen.fill((0, 0, 0))
        font_name = "ShareTechMono-Regular.ttf"
        font = pygame.font.Font(font_name, 35)
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
                    if "S" in rightList[rightItem]:
                        if rightList[rightItem][0] == "h":
                            for h in range(100):
                                hRect = pygame.Rect(415 + (3 * h), 5 + (110 * rightItem), 3, 100)
                                pygame.draw.rect(self.screen, self.hsv2rgb_pg(h, self.selectingS, self.selectingV), hRect)
                                if h == self.selectingH:
                                    pygame.draw.rect(self.screen, (255, 255, 255), hRect)
                        if rightList[rightItem][0] == "s":
                            for s in range(100):
                                sRect = pygame.Rect(415 + (3 * s), 5 + (110 * rightItem), 3, 100)
                                pygame.draw.rect(self.screen, self.hsv2rgb_pg(self.selectingH, s, self.selectingV), sRect)
                                if s == self.selectingS:
                                    pygame.draw.rect(self.screen, (255, 255, 255), sRect)
                        if rightList[rightItem][0] == "v":
                            for v in range(100):
                                vRect = pygame.Rect(415 + (3 * v), 5 + (110 * rightItem), 3, 100)
                                pygame.draw.rect(self.screen, self.hsv2rgb_pg(self.selectingH, self.selectingS, v), vRect)
                                if v == self.selectingV:
                                    pygame.draw.rect(self.screen, (255, 255, 255), vRect)
                    if "B" in rightList[rightItem]:
                        for b in range(100):
                            bRect = pygame.Rect(415 + (3 * b), 5 + (110 * rightItem), 3, 100)
                            pygame.draw.rect(self.screen, self.hsv2rgb_pg(0, 0, b), bRect)
                            if b == int(self.brightness * 100):
                                pygame.draw.rect(self.screen, self.hsv2rgb_pg(b, 100, 100), bRect)
                else:
                    if rightItem == self.columnpos:
                        text = font.render(rightList[rightItem], False, (0, 0, 0))
                        textRect = text.get_rect()
                        textRect.topleft = (410, 35 * rightItem)
                        pygame.draw.rect(self.screen, (255, 255, 255), textRect)
                        self.screen.blit(text, textRect)
                    else:
                        text = font.render(rightList[rightItem], False, (255, 255, 255))
                        textRect = text.get_rect()
                        textRect.topleft = (410, 35 * rightItem)
                        self.screen.blit(text, textRect)

        pygame.display.flip()
