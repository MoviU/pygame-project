import csv
import os

class fileManager:
    file_name = 'game.csv'
    colums = ['hight_score', 'last_score', 'player', 'effect']

    def createFiles(self):
        data = [
            self.colums,
            "0,0,default,none".split(",")
        ]
        fieldnames = data[0]
        vals = []
        for values in data[1:]:
            inner_dict = dict(zip(fieldnames, values))
            vals.append(inner_dict)
        with open(self.file_name, "w", encoding="utf-8", newline='') as file:

            writer = csv.DictWriter(file, fieldnames = fieldnames, delimiter=",")
            writer.writeheader()
            for row in vals:
                writer.writerow(row)
    def __init__(self):
        if not os.path.exists(self.file_name):
            self.createFiles()

    def find(self, params):
        with open(self.file_name) as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                print(row[params])

    def write(self, params):
        data_list = []
        with open(self.file_name) as file:
            reader = csv.DictReader(file)
            for key, val in params.items():
                for row in reader:
                    row[key] = val
                    data_list.append(row)
                    print(data_list)
        with open(self.file_name, "w", newline='') as file:
            writer = csv.DictWriter(file, self.colums)
            writer.writeheader()
            writer.writerows(data_list)
file = fileManager()
file.write({'last_score': '130'})