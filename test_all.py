import unittest
from aircraft import Plane, Helicopter
from pilot import Pilot
from airport import Airport
from Exceptions import AircraftError, AirportError, PilotError


class TestConstructorsAndStrings(unittest.TestCase):
    def test_plane_constructor_should_work(self):
        plane = Plane('PL-1', 5000, 10, 1000)
        self.assertEqual(plane.number, 'PL-1')
        self.assertEqual(plane.max_distance, 5000)
        self.assertEqual(plane.fuel, 0)

    def test_helicopter_constructor_should_work(self):
        helicopter = Helicopter('H-1', 1000, 2, True)
        self.assertEqual(helicopter.number, 'H-1')
        self.assertEqual(helicopter.is_military, True)

    def test_pilot_constructor_should_work(self):
        pilot = Pilot('Ivan', 'Ivanov', 'Ivanovich', 10, 30)
        self.assertEqual(pilot.name, 'Ivan')
        self.assertEqual(pilot.age, 30)

    def test_aircraft_string_representation(self):
        plane = Plane('STR-PLANE', 5000, 10, 1000)
        helicopter = Helicopter('STR-HELICOPTER', 1000, 2, False)
        self.assertIn('STR-PLANE', str(plane))
        self.assertIn('STR-HELICOPTER', str(helicopter))

    def test_airport_string_representation(self):
        airport = Airport('TestAirport', 10, 3000)
        self.assertIn('TestAirport', str(airport))


class TestAirportStateAndCapacity(unittest.TestCase):
    def test_airport_default_capacity_if_none(self):
        airport = Airport('Test Airport', None, 3000)
        self.assertEqual(airport.max_aircrafts, 10)

    def test_airport_initial_state(self):
        airport = Airport('Test Airport', 5, 3000)
        self.assertEqual(airport.max_aircrafts, 5)
        self.assertEqual(airport.fuel, 1000000)

    def test_add_aircraft_adds_plane_and_helicopter(self):
        airport = Airport('Test Airport', 10, 3000)
        plane = Plane('PL-1', 5000, 10, 1000)
        helicopter = Helicopter('HL-1', 1000, 2, False)
        airport.add_aircraft(plane, helicopter)
        self.assertEqual(len(airport.planes), 1)
        self.assertEqual(len(airport.helicopters), 1)

    def test_add_aircraft_stops_when_airport_is_full(self):
        airport = Airport('Test Airport', 1, 3000)
        airport.add_aircraft(Plane('PL-1', 5000, 10, 1000))
        with self.assertRaises(AirportError):
            airport.add_aircraft(Plane('PL-2', 5000, 10, 1000))
        self.assertEqual(len(airport.planes) + len(airport.helicopters), 1)

    def test_add_aircraft_should_not_add_unknown_type(self):
        airport = Airport('Test Airport', 10, 3000)
        class Dummy: number = 'DUMMY'
        with self.assertRaises(AircraftError):
            airport.add_aircraft(Dummy())
        self.assertEqual(len(airport.planes) + len(airport.helicopters), 0)


class TestPilotManagement(unittest.TestCase):
    def test_add_pilot_adds_pilot_and_sets_current_airport(self):
        airport = Airport('Test Airport', 10, 3000)
        pilot = Pilot('Name', 'Surname', 'Patronymic', 0, 30)
        airport.add_pilot(pilot)
        self.assertEqual(len(airport.pilots), 1)
        self.assertIs(pilot.current_airport, airport)

    def test_add_pilot_does_not_add_duplicate(self):
        airport = Airport('Test Airport', 10, 3000)
        pilot = Pilot('Name', 'Surname', 'Patronymic', 0, 30)
        airport.add_pilot(pilot)
        with self.assertRaises(PilotError):
            airport.add_pilot(pilot)
        self.assertEqual(len(airport.pilots), 1)

    def test_pilot_age_should_be_validated(self):
        airport = Airport('Test Airport', 10, 3000)
        with self.assertRaises(PilotError):
            airport.add_pilot(Pilot('Ivan', 'Ivanov', 'Ivanovich', 10, 20))
        self.assertEqual(len(airport.pilots), 0)


class TestAircraftSearchAndRemoval(unittest.TestCase):
    def test_aircraft_find_raises_if_not_found(self):
        airport = Airport('Test Airport', 10, 3000)
        with self.assertRaises(AircraftError):
            airport.aircraft_find('UNKNOWN')

    def test_aircraft_find_finds_plane_and_helicopter(self):
        airport = Airport('Test Airport', 10, 3000)
        plane = Plane('PL-1', 5000, 10, 1000)
        helicopter = Helicopter('HL-1', 1000, 2, False)
        airport.add_aircraft(plane, helicopter)
        self.assertIs(airport.aircraft_find('PL-1'), plane)
        self.assertIs(airport.aircraft_find('HL-1'), helicopter)

    def test_remove_aircraft_should_use_number(self):
        airport = Airport('Test Airport', 10, 3000)
        plane = Plane('REMOVE-1', 5000, 10, 1000)
        airport.add_aircraft(plane)
        airport.remove_aircraft('REMOVE-1')
        self.assertEqual(len(airport.planes), 0)


class TestRefueling(unittest.TestCase):
    def test_fuel_should_not_be_added_if_airport_has_not_enough_fuel(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 3000)
        plane = Plane('PL-1', 5000, 10, 1000)
        airport1.add_aircraft(plane)
        airport1.fuel = 0
        with self.assertRaises(AirportError):
            airport1.send_aircraft(airport2, plane.number, 100)
        self.assertEqual(plane.fuel, 0)


class TestSendAircraft(unittest.TestCase):
    def test_helicopter_transfer_should_work(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 3000)
        helicopter = Helicopter('H-1', 1000, 2, False)
        airport1.add_aircraft(helicopter)
        airport1.add_pilot(Pilot('P1', 'S1', 'Pa1', 0, 30))
        airport1.add_pilot(Pilot('P2', 'S2', 'Pa2', 0, 30))
        airport1.send_aircraft(airport2, helicopter.number, 100)
        self.assertEqual(len(airport1.helicopters), 0)
        self.assertEqual(len(airport2.helicopters), 1)

    def test_not_enough_pilots_should_not_move_aircraft(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 3000)
        airport1.add_aircraft(Plane('PL-1', 5000, 10, 1000))
        with self.assertRaises(AirportError):
            airport1.send_aircraft(airport2, 'PL-1', 100)
        self.assertEqual(len(airport1.planes), 1)
        self.assertEqual(len(airport2.planes), 0)

    def test_send_aircraft_distance_too_long(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 3000)
        airport1.add_aircraft(Plane('PL-1', 100, 10, 1000))
        with self.assertRaises(AircraftError):
            airport1.send_aircraft(airport2, 'PL-1', 200)
        self.assertEqual(len(airport1.planes), 1)
        self.assertEqual(len(airport2.planes), 0)

    def test_send_aircraft_target_full(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 1, 3000)
        airport2.add_aircraft(Plane('BLOCKER', 5000, 10, 1000))
        airport1.add_aircraft(Plane('PL-1', 5000, 10, 1000))
        with self.assertRaises(AirportError):
            airport1.send_aircraft(airport2, 'PL-1', 100)
        self.assertEqual(len(airport1.planes), 1)
        self.assertEqual(len(airport2.planes), 1)

    def test_send_aircraft_line_length_not_enough(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 500)
        airport1.add_aircraft(Plane('PL-1', 5000, 10, 1000))
        with self.assertRaises(AirportError):
            airport1.send_aircraft(airport2, 'PL-1', 100)
        self.assertEqual(len(airport1.planes), 1)
        self.assertEqual(len(airport2.planes), 0)

    def test_successful_plane_transfer(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 3000)
        plane = Plane('PL-1', 5000, 10, 1000)
        airport1.add_aircraft(plane)
        p1 = Pilot('P1', 'S1', 'Pa1', 0, 30)
        p2 = Pilot('P2', 'S2', 'Pa2', 0, 30)
        airport1.add_pilot(p1)
        airport1.add_pilot(p2)
        distance = 1000
        airport1.send_aircraft(airport2, plane.number, distance)
        self.assertEqual(len(airport1.planes), 0)
        self.assertEqual(len(airport2.planes), 1)
        self.assertEqual(plane.fuel, 0)
        self.assertEqual(airport1.fuel, 1000000 - (distance * 0.25))
        self.assertGreater(p1.working_experience, 0)
        self.assertGreater(p2.working_experience, 0)


if __name__ == '__main__':
    unittest.main()