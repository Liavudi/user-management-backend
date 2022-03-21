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
        self.logged_in = False

    def add_user(self, user_name: str, name: str, password: int, email: str, age: int):
        om = self.collection.find({}, {'_id': 0, 'username': 1})
        for o in om:
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
        for user in details:
            if user['username'] == user_name and user['password'] == password:
                continue
            else:
                raise NotFound('Username or password is incorrect')

    def update_user(self, u_id: int, name: str, age: int):
        validation(name=name, age= age)
        try:
            user_objects = [users_id for users_id in self.collection.find({'_id': ObjectId(u_id)})]
            if len(user_objects) != 1:
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
            return {}
        except Exception as exc:
            raise DBError('Failed to delete the user from the db', internal_exception=exc)

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
            raise DBError('Failed to get the users from the db', internal_exception=exc)
