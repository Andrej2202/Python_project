from aircraft import Plane
from aircraft import Helicopter
import random
class Airport:


    def __init__(self, name, max_aircrafts, line_lengths):
        self.name = name
        self.max_aircrafts = max_aircrafts
        if self.max_aircrafts is None:
            self.max_aircrafts = 10
        self.line_lengths = line_lengths
        self.planes = []
        self.helicopters = []
        self.pilots= []
        self.fuel=1000000

    def __str__(self):
            return f'Airport: Name: {self.name} Max Aircrafts: {self.max_aircrafts} Line Length: {self.line_lengths} Planes: {self.planes} Helicopters: {self.helicopters} Pilots: {self.pilots} Fuel: {self.fuel}'

    def aircraft_find(self, number):
        aircraft_sent = None  # средство, отправленное из начального аэропорта
        for i in self.planes:
            if i.number == number:
                aircraft_sent = i
                break
        for i in self.helicopters:
            if i.number == number:
                aircraft_sent = i
                break
        return aircraft_sent
    def send_aircraft(self, target_airport, number, distance):
        aircraft_sent = self.aircraft_find(number)
        if aircraft_sent is None:
            print('Aircraft not found')
            return
        if distance > aircraft_sent.max_distance:
            print('Aircraft found with maximum distance')
            return
        if target_airport.max_aircrafts <= len(target_airport.planes+target_airport.helicopters):
            print('Aircraft maximum capacity reached')
            return
        if type(aircraft_sent) == Plane and target_airport.line_lengths < aircraft_sent.min_line_length:
            print('Airport line length not enough')
            return
        if type(aircraft_sent) == Helicopter and aircraft_sent.is_military == True and target_airport.max_aircrafts*0.5 < len(target_airport.planes+target_airport.helicopters): #очепятка милирати
            print('Aircraft maximum capacity reached')
            return
        if len(self.pilots) < 2:
            print('Airport doesnt have 2 pilots to transfer')
            return


        need_fuel = distance * 0.25
        can_fuel = False
        if need_fuel > aircraft_sent.fuel:
            can_fuel = self.add_fuel(number, need_fuel)

        if can_fuel == False:
            print('Aircraft cant take off due to the fuel issues')

        pilots_for_transfer=random.sample(self.pilots, 2)  #выбирает несколько случайных элементов из списка
        for pilot in pilots_for_transfer:
            if(self.transfer_pilot(target_airport, pilot) == False):
                return

        print('transfer is approved')
        aircraft_sent.fuel -= need_fuel
        for pilot in pilots_for_transfer:
            pilot.working_experience += distance #Стаж в тыс. км
            print(f'Pilot: {pilot.name} working experience increased')

        if type(aircraft_sent) == Plane:
            self.planes.remove(aircraft_sent)
            target_airport.planes.append(aircraft_sent)
        if type(aircraft_sent) == Helicopter:
            self.helicopters.remove(aircraft_sent)
            target_airport.helicopters.append(aircraft_sent)

        
        

        print(f'fuel {need_fuel} spent for flight')
        print('Aircraft successfully transferred')

    def transfer_pilot(self, target_airport, pilot):
        if(self.disolve_pilot(pilot) == False):
            print('There is no such pilot in this airport')
            return False
        if(target_airport.add_pilot(pilot) == False):
            print('There is already a pilot with this name in target airport')
        pilot.current_airport = target_airport.name
        return True
        

    def disolve_pilot(self, pilot):
        if pilot in self.pilots:
            self.pilots.remove(pilot)
            print('Pilot disolved')
            return True
        print('Pilot is already disolved')
        return False


    def add_fuel(self, number, need_fuel):
        aircraft = self.aircraft_find(number)
        max_additional_fuel = aircraft.max_distance * 0.25 - aircraft.fuel
        if need_fuel > max_additional_fuel:
            print('This aircraft cant hold so much fuel')
            return False
        if self.fuel < need_fuel:
            print('airport fuel not enough')
            return False
        self.fuel -= need_fuel
        aircraft.fuel += need_fuel
        return True
        

    def add_pilot(self, pilot):
        if pilot not in self.pilots:
            if(pilot.age < 25 or pilot.age > 50):
                print('Pilot age is not in bounds')
                return False
            self.pilots.append(pilot)
            pilot.current_airport = self
            print('Pilot added')
            return True
        print('Pilot is already added')
        return False


    def add_aircraft(self, *args):   #кортеж, в который мы ппередаем сколько угодно параметров
        for new_aircraft in args:
            if self.max_aircrafts == len(self.planes) + len(self.helicopters):
                print('Airport is full')
                break
            if type(new_aircraft) == Plane:
                self.planes.append(new_aircraft)
                print(f'Plane: {new_aircraft.number} added')
            # else: #Если передать кракозюбру она станет вертолетом
            #     self.helicopters.append(new_aircraft)
            #     print(f'Helicopter: {new_aircraft.number} added')
            elif type(new_aircraft) == Helicopter:
                    self.helicopters.append(new_aircraft)
                    print(f'Helicopter: {new_aircraft.number} added')
            else:
                print(f'Unknown aircraft: {new_aircraft.number} not added')


    def remove_aircraft(self, *args):
        for number in args:
            for plane in self.planes:
                if plane.number == number:
                    self.planes.remove(plane)
                    print(f"Plane: {plane.number} removed") #очепятка
                    break
            for helicopter in self.helicopters:
                if helicopter.number == number:
                    self.helicopters.remove(helicopter)
                    print(f"Helicopter: {helicopter.number} removed") #очепятка
                    break
        #Тихий скип если не найдено


#sheremetievo=Airport('sheremetievo', 24, 500)

#def __str__(self):







