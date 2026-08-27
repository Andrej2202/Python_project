import json
import random
with open('FIO.json', encoding='utf-8') as json_file:  #encoding распознает русские элементы, чтобы не было ошибки
    data=json.load(json_file)
# print(data[0]['names'])
# print(data[1]['surnames'])
# print(data[2]['patronums'])
print(data[0]['names'][random.randint(0, len(data[0]['names']) - 1)], data[1]['surnames'][random.randint(0, len(data[1]['surnames']) - 1)], data[2]['patronums'][random.randint(0, len(data[2]['patronums']) - 1)])