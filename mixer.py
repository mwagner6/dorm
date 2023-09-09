import json

class Mixer:
    def __init__(self, drinks, amounts):
        self.ingredients = drinks
        self.amounts = amounts

        with open('drinks.json') as f:
            tempDrinkDict = json.load(f)
        
        self.drinkOptions = {}
        self.numDrinks = 0
        for drink in tempDrinkDict:
            passing = True
            for ingredient in tempDrinkDict[drink]:
                if ingredient not in self.ingredients:
                    passing = False
            if passing:
                self.drinkOptions[drink] = tempDrinkDict[drink]
                self.numDrinks += 1
        
        self.currentDrink = 0


mixer = Mixer(['water', 'lemon', 'syrup', 'lime'], [10000, 10000, 10000, 10000])
    
