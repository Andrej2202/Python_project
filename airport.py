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
        if type(aircraft_sent) == Helicopter and aircraft_sent.is_miliraty == True and target_airport.max_aircrafts*0.5 < len(target_airport.planes+target_airport.helicopters): #очепятка милирати
            print('Aircraft maximum capacity reached')
            return


        need_fuel = distance * 0.25
        #5 пункт ТЗ - заправка как отдельное действие
        if need_fuel > aircraft_sent.fuel:
            fill_fuel = need_fuel - aircraft_sent.fuel
            aircraft_sent.fuel += fill_fuel  #Добавили топливо, не проверив есть ли оно
            if self.fuel < fill_fuel:
                print('airport fuel not enough')
                return
            self.fuel -= fill_fuel
        print('transfer is approved')
        aircraft_sent.fuel -= need_fuel

        if type(aircraft_sent) == Plane:
            self.planes.remove(aircraft_sent)
            target_airport.planes.append(aircraft_sent)
        if type(target_airport) == Helicopter: #очепятка скорее всего
            self.helicopters.remove(aircraft_sent)
            target_airport.helicopters.append(aircraft_sent)


        pilots_for_transfer=random.sample(self.pilots, 2)  #выбирает несколько случайных элементов из списка
        # А если нет пилотов в целом?
        for pilot in pilots_for_transfer:
            pilot.working_experience += distance #Стаж в тыс. км
            print(f'Pilot: {pilot.name} working experience increased')

        print(f'fuel {need_fuel} spent for flight')
        print('Aircraft successfully transferred')

    def add_pilot(self, pilot):
        if pilot not in self.pilots:
            self.pilots.append(pilot)
            pilot.current_airport = self
            #Тихое добавление
            #Не увидел удаления


    def add_aircraft(self, *args):   #кортеж, в который мы ппередаем сколько угодно параметров
        for new_aircraft in args:
            if self.max_aircrafts == len(self.planes) + len(self.helicopters):
                print('Airport is full')
                break
            if type(new_aircraft) == Plane:
                self.planes.append(new_aircraft)
                print(f'Plane: {new_aircraft.number} added')
            else: #Если передать кракозюбру она станет вертолетом
                self.helicopters.append(new_aircraft)
                print(f'Helicopter: {new_aircraft.number} added')


    def remove_aircraft(self, *args):
        for number in args:
            for plane in self.planes:
                if plane.number == number:
                    self.planes.remove(plane)
                    print(f"Plane: {plane.name} removed") #очепятка
                    break
            for helicopter in self.helicopters:
                if helicopter.number == number:
                    self.helicopters.remove(helicopter)
                    print(f"Helicopter: {helicopter.name} removed") #очепятка
                    break
        #Тихий скип если не найдено


#sheremetievo=Airport('sheremetievo', 24, 500)

#def __str__(self):







