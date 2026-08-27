class Pilot:
    def __init__(self, name, surname, patronymic, working_experience, age):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.working_experience = working_experience
        self.age = age
        self.current_airport = None


    def __str__(self):
        return f'Pilot: Name: {self.name}, Surname: {self.surname}, Patronymic: {self.patronymic}, Working_experience: {self.working_experience} Age: {self.age} Current_airport: {self.current_airport}'

if __name__ == '__main__':
    best_pilot=Pilot('Sergey', 'Vasilyev', 'Genadievich', 6798, 30)
    best_pilot.current_airport = 'Nigyria'
    print(str(best_pilot))