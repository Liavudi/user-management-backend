from typing import List
import json
from flask import Flask, render_template



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/hello")
def hello():
    return "Welcome to hello"




class User:
    def __init__(self, id:int,name: str = '', age: int = ''):
        self.id = id
        self.name = name
        self.age = age
    def print_user(self):
        print(f'Id: {self.id} Name: {self.name}, Age: {self.age}')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }

class Helpers:
    def create_user_from_input(self) -> User:
        um = UserManagment()
        id = um.user_id()

        try:
            name = str(input('Enter name: '))
            for n in name:
                if n.isdigit():
                    print(ValueError("Invalid Input, please use only letters."))
                    self.create_user_from_input()
                    return False
            age = int(input('Enter age: '))
            new_user = User(id,name, age)
            return new_user
        except ValueError:
            print("Invalid Input")


class UserManagment():
    def __init__(self):
        self.userlist: List[User] = []

    # def user_id(self) -> List[User]:
    #     count = 0
    #     for user in self.userlist:
    #         count += 1
    #     return count



    def add_user(self,name:str, age:int):
        count = 0
        for user in self.userlist:
            count += 1
        id = count
        new_user = User(id, name, age)
        self.userlist.append(new_user)

        # TODO: add validation that the user doesn't already exist in userlist

    def update_user_name(self, exist_user_id: str, new_name: str):
        exist_user_id = int(exist_user_id)
        for user in self.userlist:
            if user.id == exist_user_id:
                user.name = new_name
            else:
                print(ValueError(f"Invalid Input, no exist user named {exist_user_id}"))

    def update_user_age(self, exist_user: str, new_age: str):
        # TODO: implement this function
        try:
            exist_user = str(input("Please enter exist user name: "))
            new_age = int(input("Enter new age: "))
            for user in self.userlist:
                if user.name == exist_user:
                    if user.age == new_age:
                        print("Please enter new age, not the same...")
                        self.update_user_age()
                        return False
                    user.age = new_age
                else:
                    print(f"Invalid Input, no exist user named {exist_user}")

        except ValueError:
            print("Invalid Input please try again.")

    def delete_user(self, id:int):
        user_id = int(id)

        for user in self.userlist:
            if user.id == user_id:
                self.userlist.remove(user)
                for users_after_deleted_user in self.userlist[user_id:]:
                    users_after_deleted_user.id -= 1

            else:
                print('ok')



    def show_user_list(self):
        for user in self.userlist:
            user.print_user()

    def list_users(self) -> List[User]:
        return self.userlist


def start_user_management_cycle():
    um = UserManagment()
    helpers = Helpers()
    while (True):
        print('User management options:')
        print('c - Create user')
        print('l - List users')
        print('n - Update user name')
        print('a - Update user age')
        print('d - Delete user')
        print('q - Exit')
        operation = input('Select an operation you want to perform:')
        operation = operation.lower()
        if operation == 'c':
            new_user = helpers.create_user_from_input()

            um.add_user(new_user)
        elif operation == 'd':
            exist_user = str(input("Please enter exist user: "))
            um.delete_user(exist_user)
        elif operation == 'n':
            existing_user = input('Enter existing user name: ')
            new_user = input('Enter new user name: ')
            um.update_user_name(existing_user, new_user)
        elif operation == 'a':
            exist_user = str(input("Please enter exist user name: "))
            new_age = int(input("Enter new age: "))
            um.update_user_age(exist_user, new_age)
        elif operation == 'l':
            um.show_user_list()
        elif operation == 'q':
            print('Goodbye!')
            return
        else:
            print(f'Received unexpected operation: {operation}')


def create_users_from_file(um: UserManagment, filepath: str):
    # Read users from the file
    # Parse the users
    # Add them to the user management

    with open(filepath) as f:
        data = json.load(f)
    for i in data:
        id = i.get('id')
        name = i.get('name')
        age = i.get('age')
        new_user = User(id,name, age)
        um.add_user(new_user)


if __name__ == '__main__':
    start_user_management_cycle()

    um = UserManagment()
    # start_user_management_cycle()  # cli (command-line-interface) for user management
    # GUI (guided-user-interface) - we will not implement now
    # create_users_from_file(um, "./sahar-users.json")
