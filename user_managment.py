from typing import List
import json
from flask import Flask, render_template
from pymongo import MongoClient
from bson import ObjectId


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return "Welcome to hello"




class User:
    def __init__(self,name: str = '', age: int = ''):

        self.name = name
        self.age = age
    def print_user(self):
        print(f'Name: {self.name}, Age: {self.age}')

    def to_dict(self) -> dict:
        return {
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
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['users']
        self.collection = self.db.all_users



    def add_user(self,name:str, age:int):
        new_user = User(name, age)
        new_user = new_user.to_dict()
        self.collection.insert_one(new_user)


        # TODO: add validation that the user doesn't already exist in userlist

    def update_user(self, id:int, name:str, age: int ):
        user_id = [users_id for users_id in self.collection.find({'_id': ObjectId(id)})]
        for u in user_id:
            user_id = str(u['_id'])
            if id == user_id:
                self.collection.replace_one({'name': u['name'], 'age': u['age']}, {
                    'name': name,
                    'age': age
                })
        return {}

    # def update_user_age(self, exist_user: str, new_age: str):
    #     # TODO: implement this function
    #     try:
    #         exist_user = str(input("Please enter exist user name: "))
    #         new_age = int(input("Enter new age: "))
    #         for user in self.userlist:
    #             if user.name == exist_user:
    #                 if user.age == new_age:
    #                     print("Please enter new age, not the same...")
    #                     self.update_user_age()
    #                     return False
    #                 user.age = new_age
    #             else:
    #                 print(f"Invalid Input, no exist user named {exist_user}")
    #
    #     except ValueError:
    #         print("Invalid Input please try again.")

    def delete_user(self, _id):
       user_id = [users_id for users_id in self.collection.find({'_id': ObjectId(_id)})]
       for u in user_id:
           user_id = str(u['_id'])
           if _id == user_id:
               self.collection.delete_one({'_id': ObjectId(_id)})
       return  {}





    def show_user_list(self):
        for user in self.userlist:
            user.print_user()

    def list_users(self) -> List[User]:

       user_list = self.collection.find({})
       parsed_user_list = []
       for user in user_list:
           parsed_user_list.append({
               'id': str(user['_id']),
               'name': user['name'],
               'age': user['age']})
       all_users = {
           'users': parsed_user_list
       }

       return all_users






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
