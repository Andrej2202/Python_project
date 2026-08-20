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


class DummyUnknownAircraft:
    number = 'DUMMY'


class TestExpectedButBrokenBehavior(unittest.TestCase):

    def test_plane_constructor_should_work(self):
        try:
            plane = Plane('PL-1', 5000, 10, 1000)
        except Exception as e:
            self.fail(f'Plane(...) должен нормально создаваться, но ошибка: {e}')

        self.assertEqual(plane.number, 'PL-1')
        self.assertEqual(plane.max_distance, 5000)
        self.assertEqual(plane.max_cargo_weight, 10)
        self.assertEqual(plane.min_line_length, 1000)
        self.assertEqual(plane.fuel, 0)

    def test_helicopter_constructor_should_work(self):
        try:
            helicopter = Helicopter('H-1', 1000, 2, True)
        except Exception as e:
            self.fail(f'Helicopter(...) должен нормально создаваться, но ошибка: {e}')

        self.assertEqual(helicopter.number, 'H-1')
        self.assertEqual(helicopter.max_distance, 1000)
        self.assertEqual(helicopter.max_cargo_weight, 2)
        self.assertEqual(helicopter.is_military, True)
        self.assertEqual(helicopter.fuel, 0)

    def test_pilot_constructor_should_work(self):
        try:
            pilot = Pilot('Ivan', 'Ivanov', 'Ivanovich', 10, 30)
        except Exception as e:
            self.fail(f'Pilot(...) должен нормально создаваться, но ошибка: {e}')

        self.assertEqual(pilot.name, 'Ivan')
        self.assertEqual(pilot.surname, 'Ivanov')
        self.assertEqual(pilot.patronymic, 'Ivanovich')
        self.assertEqual(pilot.working_experience, 10)
        self.assertEqual(pilot.age, 30)

    def test_aircraft_string_representation(self):
        plane = make_plane(number='STR-PLANE')
        helicopter = make_helicopter(number='STR-HELICOPTER')

        self.assertIn('STR-PLANE', str(plane))
        self.assertIn('STR-HELICOPTER', str(helicopter))

    def test_airport_string_representation(self):
        airport = Airport('TestAirport', 10, 3000)

        self.assertIn('TestAirport', str(airport))

    def test_helicopter_transfer_should_work(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 3000)

        helicopter = make_helicopter(number='H-1', max_distance=1000, is_military=False)
        airport1.add_aircraft(helicopter)

        pilot1 = make_pilot(name='P1')
        pilot2 = make_pilot(name='P2')

        airport1.add_pilot(pilot1)
        airport1.add_pilot(pilot2)

        try:
            airport1.send_aircraft(airport2, helicopter.number, 100)
        except Exception as e:
            self.fail(f'Отправка вертолета не должна падать, но ошибка: {e}')

        self.assertEqual(len(airport1.helicopters), 0)
        self.assertEqual(len(airport2.helicopters), 1)
        self.assertIn(helicopter, airport2.helicopters)

    def test_fuel_should_not_be_added_if_airport_has_not_enough_fuel(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 3000)

        plane = make_plane(number='PL-1', max_distance=5000, fuel=0)
        airport1.add_aircraft(plane)

        airport1.fuel = 0

        airport1.send_aircraft(airport2, plane.number, 100)

        # Если аэропорт не может заправить судно, топливо у судна не должно измениться
        self.assertEqual(plane.fuel, 0)

    def test_not_enough_pilots_should_not_crash_or_move_aircraft(self):
        airport1 = Airport('Source', 10, 3000)
        airport2 = Airport('Target', 10, 3000)

        plane = make_plane(number='PL-1', max_distance=5000, fuel=0)
        airport1.add_aircraft(plane)

        try:
            airport1.send_aircraft(airport2, plane.number, 100)
        except Exception as e:
            self.fail(f'При нехватке пилотов метод не должен падать, но ошибка: {e}')

        # Если пилотов меньше двух, рейс не должен состояться
        self.assertEqual(len(airport1.planes), 1)
        self.assertEqual(len(airport2.planes), 0)
        self.assertIn(plane, airport1.planes)

    def test_remove_aircraft_should_use_number_not_name(self):
        airport = Airport('Test Airport', 10, 3000)
        plane = make_plane(number='REMOVE-1')

        airport.add_aircraft(plane)

        try:
            airport.remove_aircraft('REMOVE-1')
        except Exception as e:
            self.fail(f'Удаление воздушного судна не должно падать, но ошибка: {e}')

        self.assertEqual(len(airport.planes), 0)
        self.assertNotIn(plane, airport.planes)

    def test_add_aircraft_should_not_add_unknown_type_as_helicopter(self):
        airport = Airport('Test Airport', 10, 3000)
        dummy = DummyUnknownAircraft()

        airport.add_aircraft(dummy)

        self.assertEqual(len(airport.planes), 0)
        self.assertEqual(len(airport.helicopters), 0)

    def test_disolve_pilot_method_should_exist(self):
        airport = Airport('Test Airport', 10, 3000)

        self.assertTrue(
            callable(getattr(airport, 'disolve_pilot', None)),
            'У аэропорта должен быть метод увольнения пилота, например fire_pilot'
        )

    def test_refuel_aircraft_method_should_exist(self):
        airport = Airport('Test Airport', 10, 3000)

        self.assertTrue(
            callable(getattr(airport, 'add_fuel', None)),
            'У аэропорта должен быть отдельный метод заправки, например refuel_aircraft'
        )

    def test_pilot_age_should_be_validated(self):
        pilot1 = Pilot('Ivan', 'Ivanov', 'Ivanovich', 10, 20)
        airport = Airport('Test Airport', 10, 3000)
        before_update = len(airport.pilots)
        airport.add_pilot(pilot1)
        self.assertEqual(before_update, len(airport.pilots))



if __name__ == '__main__':
    unittest.main()

# python -m unittest test_red.py -v