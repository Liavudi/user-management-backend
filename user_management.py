from typing import List
from pymongo import MongoClient
from bson import ObjectId
from user import User
from consts import DBURL, DB
from exceptions import *

class UserManagement:
    def __init__(self):
        self.userlist: List[User] = []
        self.client = MongoClient(DBURL)
        self.db = self.client[DB]
        self.collection = self.db.users
        self.todo_collection = self.db.todos
        self.logged_in = False

    def add_user(self, user_name: str, name: str, password: int, email: str, age: int):

        om = self.collection.find({}, {'_id': 0, 'username': 1})
        for o in om:
            print(o['username'])
            if o['username'] == user_name:
                raise UsernameAlreadyExists('Username already exists')
        new_user = User(user_name, name, password, email, age)
        new_user = new_user.to_dict()
        try:
            self.collection.insert_one(new_user)
        except Exception as exc:
            raise DBError('Failed to insert the user to the db', internal_exception=exc)

    def login(self, user_name: str, password: int):
        details = self.collection.find({"username": f"{user_name}"}, {'_id': 0, 'name': 0, 'email': 0, 'age': 0})
        print(details)
        for user in details:
            print(user)
            if user['username'] == user_name and user['password'] == password:
                print('Alright good')

            else:
                raise NotFound('Username or password is incorrect')

    def update_user(self, u_id: int, name: str, age: int):
        validation(name=name, age= age)
        try:
            user_objects = [users_id for users_id in self.collection.find({'_id': ObjectId(u_id)})]
            if len(user_objects) != 1:
                # Failed to find (A.K.A NotFound) status code is 404, handle it accordingly wherever you think is right)
                raise NotFound('Failed to find user with such id in the DB')
            user_id = user_objects[0]
            self.collection.replace_one({'name': user_id['name'], 'age': user_id['age']}, {
                'name': name,
                'age': age
            })
        except Exception as exc:
            raise DBError('Failed to insert the user to the db', internal_exception=exc)

    def delete_user(self, _id):
        try:
            self.collection.delete_one({'_id': ObjectId(_id)})
        except Exception as exc:
            raise DBError('Failed to insert the user to the db', internal_exception=exc)

        return {}

    def show_user_list(self):
        for user in self.userlist:
            user.print_user()

    def list_users(self) -> dict:
        try:
            user_list = self.collection.find({})
            parsed_user_list = []
            for user in user_list:
                parsed_user_list.append({
                    'id': str(user['_id']),
                    'username': user['username'],
                    'name': user['name'],
                    'email': user['email'],
                    'age': user['age']})
            all_users = {
                'users': parsed_user_list
            }

            return all_users
        except Exception as exc:
            raise DBError('Failed to insert the user to the db', internal_exception=exc)

    def create_todo_list(self,user_name, todo):
        dict = {
            'username': user_name,
            'todo': todo
        }
        self.todo_collection.insert_one(dict)
        return {}

    def get_todo_list(self,):
        parsed_todo_list = []
        todo_list = self.todo_collection.find({}, {'username': 1,'todo': 1, })

        for todo in todo_list:
            print(todo)
            parsed_todo_list.append({
                '_id': str(todo['_id']),
                'username': todo['username'],
                'todo': todo['todo']
            })
        all_todos = {
            'todos': parsed_todo_list
        }
        return all_todos

    def delete_todo(self, todo_id):
        print(todo_id)
        self.todo_collection.delete_one({'_id': ObjectId(todo_id)})
        return {}