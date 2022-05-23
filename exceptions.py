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


class AlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class NotAuthorized(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class NotExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def validation(user_name: str = '', name: str = '', password: int = 6, email: str = '', age: int = 0):
    for each_letter in name:
        if each_letter.isdigit():
            raise InvalidInputError('Name cannot contain numbers')
    if len(user_name) <= 2:
        raise InvalidInputError('Username must be 3 or more letters')
    if len(name) == '' or len(name) <= 2:
        raise InvalidInputError('Name must be 3 or more letters')
    if int(age) < 18:
        raise InvalidInputError('You must be over 18')
    if len(password) <= 5:
        raise InvalidInputError('Password must be 6 or more letters')
    if '@' not in email:
        raise InvalidInputError('Email must have @ in it')




