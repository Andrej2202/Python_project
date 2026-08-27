from aircraft import Plane, Helicopter
import random
from Exceptions import AircraftError, AirportError, PilotError


class Airport:
    def __init__(self, name, max_aircrafts, line_lengths):
        self.name = name
        self.max_aircrafts = max_aircrafts if max_aircrafts is not None else 10
        self.line_lengths = line_lengths
        self.planes = []
        self.helicopters = []
        self.pilots = []
        self.fuel = 1000000

    def __str__(self):
        return f'Airport: Name: {self.name} Max Aircrafts: {self.max_aircrafts} Line Length: {self.line_lengths} Planes: {len(self.planes)} Helicopters: {len(self.helicopters)} Pilots: {len(self.pilots)} Fuel: {self.fuel}'

    def aircraft_find(self, number):
        aircraft_sent = None
        for i in self.planes:
            if i.number == number:
                aircraft_sent = i
                break
        for i in self.helicopters:
            if i.number == number:
                aircraft_sent = i
                break
        if aircraft_sent is None:
            raise AircraftError(f"There is no aircraft with number {number}")
        return aircraft_sent

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

    def transfer_pilot(self, target_airport, pilot):
        temp_pilot = pilot
        self.disolve_pilot(pilot)
        temp_pilot.current_airport = target_airport
        target_airport.add_pilot(temp_pilot)

    def disolve_pilot(self, pilot):
        if pilot in self.pilots:
            self.pilots.remove(pilot)
            print('Pilot disolved')
            return
        raise PilotError(f'There is no such pilot in {self.name}')

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
            return
        raise PilotError('Pilot is already added')

    def add_aircraft(self, *args):
        for new_aircraft in args:
            if self.max_aircrafts < len(self.planes) + len(self.helicopters):
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


if __name__ == '__main__':
    best_airport=Airport('Vnukovo', 15, 100)
    print(str(best_airport))