class Aircraft:
    def __init__(self, number, max_distance, max_cargo_weight):
        self.number=number
        self.max_distance=max_distance
        self.max_cargo_weight=max_cargo_weight
        self.fuel=0
    def __str__(self):
        return f'Aircraft: Number:{self.number}, Max_distance: {self.max_distance}, Max_cargo_weight: {self.max_cargo_weight}'

class Plane(Aircraft):
    def __init__(self, number, max_distance, max_cargo_weight, min_line_length):
        super().__init__(number, max_distance, max_cargo_weight)
        self.min_line_length=min_line_length
    def __str__(self):
        return f"Plane: Number: {self.number}, Max_distance: {self.max_distance}, Max_cargo_weight: {self.max_cargo_weight}, Min_line_length: {self.min_line_length}"

class Helicopter(Aircraft):
    def __init__(self, number, max_distance, max_cargo_weight, is_military):
        super().__init__(number, max_distance, max_cargo_weight)
        self.is_military=is_military
    def __str__(self):
        return f'Helicopter: Number: {self.number}, Max_distance: {self.max_distance}, Max_cargo_weight: {self.max_cargo_weight}, Is_military: {self.is_military}'



#su_57=Plane('54664', 576, 6798, 57)
#print(su_57)