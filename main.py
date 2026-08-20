from ex.aircraft import Plane
from ex.aircraft import Helicopter
from ex.airport import Airport
from pilot import Pilot
import json
import random
with open('airports.json', encoding='utf-8') as json_file:  #encoding распознает русские элементы, чтобы не было ошибки
    data=json.load(json_file)   #json файл преобразовываем в список
#print(data)
#print(data[0])
added_airports=[]
for i in data:
    airport=Airport(i['name'], i['max_aricrafts'], i['line_length'])
    for j in i['planes']:
        plane=Plane(j['number'], j['max_distance'], j['max_cargo_weight'], j['min_line_length'])
        airport.add_aircraft(plane)
    for j in i['helicopters']:
        helicopter = Helicopter(j['number'], j["max_distance"], j["max_cargo_weight"], j['is_military'])
        airport.add_aircraft(helicopter)
    for j in range(5):
        pilot = Pilot(f'Name{j}', f'Surname{j}', f'Patronymic{j}', 1000, random.randint(25, 50))
        airport.pilots.append(pilot)
        print(pilot)
    added_airports.append(airport)


airport1=added_airports[0]
airport2=added_airports[1]
print(len(airport1.planes))
print(len(airport2.planes))
plane1 = airport1.planes[0]
airport1.send_aircraft(airport2, "19-662-0603", 3761)
print(len(airport1.planes))
print(len(airport2.planes))







#print(airport)
#print(i)