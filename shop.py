import pygame
import files
import os
import csv

class Shop:
    __colums = ['id', 'type', 'inShop', 'price', 'file']

    def getBalance(self):
        balance = self.__fileManager.find("game.csv", 'coins')
        return int(balance[0])

    def getSkin(self):
        skin = self.__fileManager.find("game.csv", 'player')
        return skin[0]

    def buyed(self, id):
        __data_list = []
        for row in self.getItems():
            if row['id'] == id:
                row['inShop'] = '0'
            __data_list.append(row)
        with open("shop.csv", "w", newline='') as file:
            writer = csv.DictWriter(file, self.__colums)
            writer.writeheader()
            writer.writerows(__data_list)

    def find(self, id, key):
        for row in self.getItems():
            if row['id'] == id:
                return row[key]

    def buy(self, id):
        __price = int(self.find(id, 'price'))
        if self.getBalance() >= __price:
            self.buyed(id)
            self.__fileManager.write({'coins': self.getBalance() - __price})
            return True
        return False

    def setSkin(self, id):
        self.__fileManager.write({'player': self.find(id, 'file')})

    def setEffect(self, id):
        if id == 'none':
            self.__fileManager.write({'effect': 'none'})
        else:
            self.__fileManager.write({'effect': self.find(id, 'file')})

    def getEffect(self):
        effect = self.__fileManager.find("game.csv", 'effect')
        return effect[0]

    def getItems(self):
        items = self.__fileManager.find("shop.csv")
        return items

    def __init__(self):
        if not os.path.exists("shop.csv"):
            files.fileManager.createFile("shop.csv", {
                'type': ['skin', 'skin', 'skin', 'skin', 'skin', 'skin', 'skin', 'effect', 'effect', 'effect'],
                'inShop': ['1', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
                'price': ['1000', '750', '750', '500', '500', '0', '500', '5000', '2500', '3000'],
                'file':  ['skin_1.png', 'skin_2.png', 'skin_3.png', 'skin_4.png', 'skin_5.png', 'skin_6.png', 'skin_7.png', 'effect_1', 'effect_2', 'effect_3']
            })
        self.__fileManager = files.fileManager()
        self.balance = self.getBalance
        self.skin = self.getSkin()
        self.effect = self.getEffect()
        self.items = self.getItems()

