


class User:
    def __init__(self, user_name: str, name: str, password: int, email: str, age: int, role: str):
        self.user_name = user_name
        self.name = name
        self.age = age
        self.password = password
        self.email = email
        self.role = role

    def to_dict(self) -> dict:
        return {
            'username': self.user_name,
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'age': self.age,
            'role': self.role
            }