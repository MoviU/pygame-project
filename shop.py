import pygame
import files
import os

class Shop:
    def getBalance(self):
        balance = self.__fileManager.find("game.csv", 'coins')
        return int(balance)

    def getSkin(self):
        skin = self.__fileManager.find("game.csv", 'player')
        return skin

    def getEffect(self):
        effect = self.__fileManager.find("game.csv", 'effect')
        return effect

    def getItems(self):
        items = self.__fileManager.find("shop.csv")
        return items

    def __init__(self):
        if not os.path.exists("shop.csv"):
            files.fileManager.createFile("shop.csv", {
                'type': ['skin', 'effect', 'skin'],
                'inShop': ['1', '1', '1'],
                'price': ['1000', '50000', '5000'],
                'file':  ['skin_1.png', 'effect_1.png', 'skin_2.png']
            })
        self.__fileManager = files.fileManager()
        self.balance = self.getBalance
        self.skin = self.getSkin()
        self.effect = self.getEffect()
        self.items = self.getItems()

