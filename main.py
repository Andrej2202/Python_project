from aircraft import Plane, Helicopter
from airport import Airport
from Exceptions import AircraftError, AirportError, PilotError
from pilot import Pilot
import json
import random


def find_tests(airport1):
    print('Aircraft find tests:')
    try:
        print(airport1.aircraft_find('19-662-0603'))
    except AircraftError as e:
        print(f"{e}")
    try:
        print(airport1.aircraft_find('88-515-9241'))
    except AircraftError as e:
        print(f"{e}")
    try:
        print(airport1.aircraft_find('88-515-9240'))
    except AircraftError as e:
        print(f"{e}")

def transfer_tests(airport1, airport2):
    print('\nTransfer tests:')
    try:
        name = airport1.pilots[0].name
        surname = airport1.pilots[0].surname
        print(f'Trying to transfer pilot {surname} {name} from {airport1.name} to {airport2.name}')
        airport1.transfer_pilot(airport2, airport1.pilots[0])
        print(f'Transfered pilot {surname} {name} from {airport1.name} to {airport2.name} sucesfully')
    except PilotError as e:
            print(f"Error: {e}")

    try:
        mock_pilot = Pilot('Vanya', 'Ivanov', 'Ivanich', 78, 45)
        name = mock_pilot.name
        surname = mock_pilot.surname
        print(f'Trying to transfer pilot {surname} {name} from {airport1.name} to {airport2.name}')
        airport1.transfer_pilot(airport2, mock_pilot)
        print(f'Transfered pilot {surname} {name} from {airport1.name} to {airport2.name} sucesfully')
    except PilotError as e:
            print(f"Error: {e}")


with open('airports.json', encoding='utf-8') as json_file:  #encoding распознает русские элементы, чтобы не было ошибки
    data=json.load(json_file)   #json файл преобразовываем в список
with open('FIO.json', encoding='utf-8') as json_file2:  #encoding распознает русские элементы, чтобы не было ошибки
    fio_data=json.load(json_file2)
#print(data)
#print(data[0])
added_airports=[]
for i in data:
    airport=Airport(i['name'], i['max_aricrafts'], i['line_length'])
    for j in i['planes']:
        plane=Plane(j['number'], j['max_distance'], j['max_cargo_weight'], j['min_line_length'])
        try:
            airport.add_aircraft(plane)
        except AirportError as e:
             print("There are too many airplanes already.")
    for j in i['helicopters']:
        helicopter = Helicopter(j['number'], j["max_distance"], j["max_cargo_weight"], j['is_military'])
        try:
            airport.add_aircraft(helicopter)
        except AirportError as e:
                print("There are too many airplanes already.")
    for j in range(5):
        pilot = Pilot(fio_data[0]['names'][random.randint(0, len(fio_data[0]['names']) - 1)], f'Surname{j}', f'Patronymic{j}', random.randint(0, 10000), random.randint(25, 50))
        airport.pilots.append(pilot)
        #airport.add_pilot(pilot)
        print(pilot)
    added_airports.append(airport)





airport1=added_airports[0]
airport2=added_airports[1]
print('\n----------------------------------------------------------------------------\n')
find_tests(airport1)
transfer_tests(airport1, airport2)

print('\nDisolve pilot tests:')
try:
    airport1.disolve_pilot(airport1.pilots[0])
except PilotError as e:
            print(f"Error: {e}")

try:
    mock_pilot = Pilot('Vanya', 'Ivanov', 'Ivanich', 78, 45)
    airport1.disolve_pilot(mock_pilot)
except PilotError as e:
            print(f"Error: {e}")

'''


    def add_fuel(self, number, need_fuel):
        aircraft = self.aircraft_find(number)
        max_additional_fuel = aircraft.max_distance * 0.25 - aircraft.fuel
        if need_fuel > max_additional_fuel:
            raise AircraftError('This aircraft cant hold so much fuel')
        if self.fuel < need_fuel:
            raise AirportError('airport fuel not enough')
        self.fuel -= need_fuel
        aircraft.fuel += need_fuel

    def add_pilot(self, pilot):
        if pilot not in self.pilots:
            if pilot.age < 25 or pilot.age > 50:
                raise PilotError('Pilot age is not in bounds')
            self.pilots.append(pilot)
            pilot.current_airport = self
            print('Pilot added')
            return True
        raise PilotError('Pilot is already added')

    def add_aircraft(self, *args):
        for new_aircraft in args:
            if self.max_aircrafts == len(self.planes) + len(self.helicopters):
                raise AirportError('Airport is full')
            if type(new_aircraft) == Plane:
                self.planes.append(new_aircraft)
                print(f'Plane: {new_aircraft.number} added')
            elif type(new_aircraft) == Helicopter:
                self.helicopters.append(new_aircraft)
                print(f'Helicopter: {new_aircraft.number} added')
            else:
                raise AircraftError(f'Unknown aircraft: {new_aircraft.number} not added')

    def remove_aircraft(self, *args):
        for number in args:
            found = False
            for plane in self.planes:
                if plane.number == number:
                    self.planes.remove(plane)
                    print(f"Plane: {plane.number} removed")
                    found = True
                    break
            if not found:
                for helicopter in self.helicopters:
                    if helicopter.number == number:
                        self.helicopters.remove(helicopter)
                        print(f"Helicopter: {helicopter.number} removed")
                        found = True
                        break
            if not found:
                print(f"Aircraft not found, number: {number}")


    
                



    
                

    def send_aircraft(self, target_airport, number, distance):
            aircraft_sent = self.aircraft_find(number)
            
            if distance > aircraft_sent.max_distance:
                raise AircraftError(f"Aircraft found, but maximum distance: {aircraft_sent.max_distance} is lower then distance between airports: {distance}")
            
            if target_airport.max_aircrafts <= len(target_airport.planes) + len(target_airport.helicopters):
                raise AirportError("Aircraft maximum capacity reached")
            
            if type(aircraft_sent) == Plane and target_airport.line_lengths < aircraft_sent.min_line_length:
                raise AirportError('Airport line length not enough')
            
            if type(aircraft_sent) == Helicopter and aircraft_sent.is_military and target_airport.max_aircrafts * 0.5 < len(target_airport.planes) + len(target_airport.helicopters):
                raise AircraftError('Aircraft maximum capacity reached')
            
            if len(self.pilots) < 2:
                raise AirportError('Airport doesnt have 2 pilots to transfer')
            
            need_fuel = distance * 0.25
            if need_fuel > aircraft_sent.fuel:
                self.add_fuel(number, need_fuel)
            
            pilots_for_transfer = random.sample(self.pilots, 2)
            
            for pilot in pilots_for_transfer:
                self.transfer_pilot(target_airport, pilot)
            
            print('transfer is approved')
            aircraft_sent.fuel -= need_fuel
            
            for pilot in pilots_for_transfer:
                pilot.working_experience += distance
                print(f'Pilot: {pilot.name} working experience increased')
            
            if type(aircraft_sent) == Plane:
                self.planes.remove(aircraft_sent)
                target_airport.planes.append(aircraft_sent)
            elif type(aircraft_sent) == Helicopter:
                self.helicopters.remove(aircraft_sent)
                target_airport.helicopters.append(aircraft_sent)
            
            print(f'fuel {need_fuel} spent for flight')
            print('Aircraft successfully transferred')
'''