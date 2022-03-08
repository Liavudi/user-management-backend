class User:
    def __init__(self, name: str, age: int):
        # TODO: add a validation that the name and age are correct
        # name - cannot be empty!
        # age - must be above 18
        self.name = name
        self.age = age

    def print_user(self):
        print(f'Name: {self.name}, Age: {self.age}')

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'age': self.age
        }