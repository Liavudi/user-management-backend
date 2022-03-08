from consts import *
class DBError(Exception):
    def __init__(self, message: str, internal_exception: Exception = None):
        super().__init__(message)
        self.message = message
        self.internal_exception = internal_exception


class InvalidInputError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class UsernameAlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def validation(user_name: str = 0, name: str = 0, password: int = 0, email: str = '', age: int = 0):
    for each_letter in name:
        if each_letter.isdigit():
            raise InvalidInputError('Name cannot contain numbers')
    if len(name) == '' or len(name) <= 2:
        raise InvalidInputError('Name must be more than 3 letters')
    if int(age) < 18:
        raise InvalidInputError('You must be over 18')



