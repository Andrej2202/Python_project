import unittest

from aircraft import Plane, Helicopter
from pilot import Pilot
from airport import Airport


def make_plane(
    number='P-1',
    max_distance=5000,
    max_cargo_weight=10,
    min_line_length=1000,
    fuel=0
):
    """
    Хелпер создает самолет так, чтобы тесты могли работать
    даже если конструктор в коде студента сломан.
    """
    try:
        plane = Plane(number, max_distance, max_cargo_weight, min_line_length)
    except TypeError:
        plane = Plane()
        plane.number = number
        plane.max_distance = max_distance
        plane.max_cargo_weight = max_cargo_weight
        plane.min_line_length = min_line_length

    plane.fuel = fuel
    return plane


def make_helicopter(
    number='H-1',
    max_distance=1000,
    max_cargo_weight=2,
    is_military=False,
    fuel=0
):
    """
    Хелпер создает вертолет так, чтобы тесты могли работать
    даже если конструктор в коде студента сломан.
    """
    try:
        helicopter = Helicopter(number, max_distance, max_cargo_weight, is_military)
    except TypeError:
        helicopter = Helicopter()
        helicopter.number = number
        helicopter.max_distance = max_distance
        helicopter.max_cargo_weight = max_cargo_weight
        helicopter.is_military = is_military

    helicopter.fuel = fuel
    return helicopter


def make_pilot(
    name='Name',
    surname='Surname',
    patronymic='Patronymic',
    working_experience=0,
    age=30
):
    """
    Хелпер создает пилота так, чтобы тесты могли работать
    даже если конструктор в коде студента сломан.
    """
    try:
        pilot = Pilot(name, surname, patronymic, working_experience, age)
    except TypeError:
        pilot = Pilot()
        pilot.name = name
        pilot.surname = surname
        pilot.patronymic = patronymic
        pilot.working_experience = working_experience
        pilot.age = age

    if not hasattr(pilot, 'current_airport'):
        pilot.current_airport = None

    return pilot


class TestCurrentWorkingBehavior(unittest.TestCase):

    def test_airport_default_capacity_if_none(self):
        airport = Airport('Test Airport', None, 3000)
        self.assertEqual(airport.max_aircrafts, 10)

    def test_airport_initial_state(self):
        airport = Airport('Test Airport', 5, 3000)

        self.assertEqual(airport.name, 'Test Airport')
        self.assertEqual(airport.max_aircrafts, 5)
        self.assertEqual(airport.line_lengths, 3000)
        self.assertEqual(airport.planes, [])
        self.assertEqual(airport.helicopters, [])
        self.assertEqual(airport.pilots, [])
        self.assertEqual(airport.fuel, 1000000)

    def test_add_aircraft_adds_plane_and_helicopter(self):
        airport = Airport('Test Airport', 10, 3000)

        plane = make_plane(number='PL-1')
        helicopter = make_helicopter(number='HL-1')

        airport.add_aircraft(plane)
        airport.add_aircraft(helicopter)

        self.assertEqual(len(airport.planes), 1)
        self.assertEqual(len(airport.helicopters), 1)
        self.assertIn(plane, airport.planes)
        self.assertIn(helicopter, airport.helicopters)

    def test_aircraft_find_returns_none_if_not_found(self):
        airport = Airport('Test Airport', 10, 3000)

        result = airport.aircraft_find('UNKNOWN')
        self.assertIsNone(result)

    def test_aircraft_find_finds_plane_and_helicopter(self):
        airport = Airport('Test Airport', 10, 3000)

        plane = make_plane(number='PL-1')
        helicopter = make_helicopter(number='HL-1')

        airport.add_aircraft(plane)
        airport.add_aircraft(helicopter)

        found_plane = airport.aircraft_find('PL-1')
        found_helicopter = airport.aircraft_find('HL-1')

        self.assertIs(found_plane, plane)
        self.assertIs(found_helicopter, helicopter)

    def test_add_pilot_adds_pilot_and_sets_current_airport(self):
        airport = Airport('Test Airport', 10, 3000)
        pilot = make_pilot()

        airport.add_pilot(pilot)

        self.assertEqual(len(airport.pilots), 1)
        self.assertIn(pilot, airport.pilots)
        self.assertIs(pilot.current_airport, airport)

    def test_add_pilot_does_not_add_duplicate(self):
        airport = Airport('Test Airport', 10, 3000)
        pilot = make_pilot()

        airport.add_pilot(pilot)
        airport.add_pilot(pilot)

        self.assertEqual(len(airport.pilots), 1)

    def test_add_aircraft_stops_when_airport_is_full(self):
        airport = Airport('Test Airport', 1, 3000)

        plane1 = make_plane(number='PL-1')
        plane2 = make_plane(number='PL-2')

        airport.add_aircraft(plane1)
        airport.add_aircraft(plane2)

        total_aircrafts = len(airport.planes) + len(airport.helicopters)
        self.assertEqual(total_aircrafts, 1)

    def test_send_aircraft_not_found(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 3000)

        airport1.send_aircraft(airport2, 'UNKNOWN', 100)

        self.assertEqual(len(airport1.planes), 0)
        self.assertEqual(len(airport1.helicopters), 0)
        self.assertEqual(len(airport2.planes), 0)
        self.assertEqual(len(airport2.helicopters), 0)

    def test_send_aircraft_distance_too_long(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 3000)

        plane = make_plane(number='PL-1', max_distance=100, min_line_length=1000)
        airport1.add_aircraft(plane)

        airport1.send_aircraft(airport2, plane.number, 200)

        self.assertIn(plane, airport1.planes)
        self.assertNotIn(plane, airport2.planes)

    def test_send_aircraft_target_full(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 1, 3000)

        blocker = make_plane(number='BLOCKER')
        airport2.add_aircraft(blocker)

        plane = make_plane(number='PL-1')
        airport1.add_aircraft(plane)

        airport1.send_aircraft(airport2, plane.number, 100)

        self.assertIn(plane, airport1.planes)
        self.assertNotIn(plane, airport2.planes)
        self.assertEqual(len(airport2.planes), 1)

    def test_send_aircraft_line_length_not_enough(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 500)

        plane = make_plane(number='PL-1', min_line_length=1000)
        airport1.add_aircraft(plane)

        airport1.send_aircraft(airport2, plane.number, 100)

        self.assertIn(plane, airport1.planes)
        self.assertNotIn(plane, airport2.planes)

    def test_successful_plane_transfer(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 3000)

        plane = make_plane(
            number='PL-1',
            max_distance=5000,
            min_line_length=1000,
            fuel=0
        )

        airport1.add_aircraft(plane)

        pilot1 = make_pilot(name='P1', working_experience=0)
        pilot2 = make_pilot(name='P2', working_experience=0)

        airport1.add_pilot(pilot1)
        airport1.add_pilot(pilot2)

        distance = 1000
        expected_fuel = distance * 0.25

        airport1.send_aircraft(airport2, plane.number, distance)

        # Самолет перемещен
        self.assertEqual(len(airport1.planes), 0)
        self.assertEqual(len(airport2.planes), 1)
        self.assertIn(plane, airport2.planes)

        # Топливо у самолета потрачено
        self.assertEqual(plane.fuel, 0)

        # Топливо у аэропорта уменьшено
        self.assertEqual(airport1.fuel, 1000000 - expected_fuel)

        # Пилоты получили опыт
        self.assertGreater(pilot1.working_experience, 0)
        self.assertGreater(pilot2.working_experience, 0)


if __name__ == '__main__':
    unittest.main()

# python -m unittest test_green.py -v