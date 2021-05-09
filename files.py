import csv
import os

class fileManager:
    __file_name = 'game.csv'
    __shop_file_name = "shop.csv"
    __colums = ['hight_score', 'last_score', 'player', 'effect', 'coins']
    __shopColumns = ['id', 'type', 'inShop', 'price', 'file']

    def __createFiles(self):
        __data = [
            self.__colums,
            "0,0,skin_6.png,none,0".split(",")
        ]
        __fieldnames = __data[0]
        __vals = []
        for values in __data[1:]:
            inner_dict = dict(zip(__fieldnames, values))
            __vals.append(inner_dict)
        with open(self.__file_name, "w", encoding="utf-8", newline='') as file:

            __writer = csv.DictWriter(file, fieldnames = __fieldnames, delimiter=",")
            __writer.writeheader()
            for row in __vals:
                __writer.writerow(row)

    def __init__(self):
        if not os.path.exists(self.__file_name):
            self.__createFiles()

    def find(self, file_name = "game.csv", params = False):
        with open(file_name) as file:
            __result = []
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                if params:
                    __result.append(row[params])
                else:
                    __result.append(row)
            return __result

    def write(self, params, file_name = "game.csv"):
        __data_list = []
        with open(file_name) as file:
            __reader = csv.DictReader(file)
            for key, val in params.items():
                for row in __reader:
                    row[key] = val
                    __data_list.append(row)
        with open(file_name, "w", newline='') as file:
            writer = csv.DictWriter(file, self.__colums)
            writer.writeheader()
            writer.writerows(__data_list)

    def addCoin(self, file_name = "game.csv", count = 1):
        __data_list = []
        with open(file_name) as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['coins'] = int(row['coins']) + count
                __data_list.append(row)
        with open(file_name, "w", newline='') as file:
            writer = csv.DictWriter(file, self.__colums)
            writer.writeheader()
            writer.writerows(__data_list)

    @staticmethod
    def createFile(name, data = dict):
        __shopColumns = ['id']
        __vals = []
        for i in data.keys():
            __count = len(data[i])
            __shopColumns.append(i)
        for i in range(__count):
            __values = [i + 1]
            for j in data.keys():
                __values.append(data[j][i])
            inner_dict = dict(zip(__shopColumns, __values))
            __vals.append(inner_dict)
        print(__vals)
        with open(name, "w", encoding="utf-8", newline='') as file:
            __writer = csv.DictWriter(file, fieldnames = __shopColumns, delimiter=",")
            __writer.writeheader()
            for row in __vals:
                __writer.writerow(row)
