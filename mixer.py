import json
import pygame

class Mixer:
    def __init__(self, drinks, amounts):
        self.ingredients = drinks
        self.amounts = amounts

        with open('drinks.json') as f:
            tempDrinkDict = json.load(f)
        
        self.drinkOptions = []
        self.drinkNames = []
        self.numDrinks = 0
        for drink in tempDrinkDict:
            passing = True
            for ingredient in tempDrinkDict[drink]:
                if ingredient not in self.ingredients:
                    passing = False
            if passing:
                self.drinkOptions.append(tempDrinkDict[drink])
                self.drinkNames.append(drink)
                self.numDrinks += 1
        
        self.currentDrinkInd = 0
        self.currentDrink = self.drinkNames[0]
        pygame.init()
        self.screen = pygame.display.set_mode((800, 480))

    def createScreen(self):
        self.screen.fill((0, 0, 0))
        font_name = 'ShareTechMono-Regular.ttf'
        font = pygame.font.Font(font_name, 35)
        for drink in range(len(self.drinkOptions)):
            if drink == self.currentDrinkInd:
                text = font.render(self.drinkNames[drink], False, (0, 0, 0))
                textRect = text.get_rect()
                textRect.topleft = (0, 50 * drink)
                pygame.draw.rect(self.screen, (255, 255, 255), textRect)
                self.screen.blit(text, textRect)
            else:
                text = font.render(self.drinkNames[drink], False, (255, 255, 255))
                textRect = text.get_rect()
                textRect.topleft = (0, 50 * drink)
                self.screen.blit(text, textRect)
        pygame.display.flip()

    def downInput(self):
        self.currentDrinkInd += 1
        if self.currentDrinkInd == self.numDrinks:
            self.currentDrinkInd = 0
        self.currentDrink = self.drinkNames[self.currentDrinkInd]

    def upInput(self):
        self.currentDrinkInd -= 1
        if self.currentDrinkInd < 0:
            self.currentDrinkInd = self.numDrinks - 1
        self.currentDrink = self.drinkNames[self.currentDrinkInd]

    def pressInput(self):
        self.dispense()

    def dispense(self):
        currentDict = self.drinkOptions[self.currentDrinkInd]
        print("Dispensing " + self.currentDrink + ":")
        for i in currentDict:
            currentIngredient = i
            ingIndex = self.ingredients.index(i)
            self.amounts[ingIndex] -= currentDict[currentIngredient]
            print(str(currentDict[currentIngredient]) + 'ml of ' + currentIngredient + ' from channel ' + str(ingIndex) + '. Volume remaining: ' + str(self.amounts[ingIndex]))

    
