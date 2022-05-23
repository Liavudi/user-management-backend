from typing import List
from pymongo import MongoClient
from bson import ObjectId
from user import User
from consts import DBURL, DB
from exceptions import *
from passlib.hash import sha256_crypt

class UserManagement:
    def __init__(self):
        self.userlist: List[User] = []
        self.client = MongoClient(DBURL)
        self.db = self.client[DB]
        self.collection = self.db.users
        self.logged_in = False
        self.hash = sha256_crypt

    def add_user(self, user_name: str, name: str, password: int, email: str, age: int, role: str = 'user'):
        om = self.collection.find({}, {'_id': 0, 'username': 1, 'email': 1})
        for o in om:
            if o['username'] == user_name:
                raise AlreadyExists('Username already exists')
            if o['email'] == email:
                raise AlreadyExists('Email already exists')
        encrypt_password = self.hash.encrypt(str(password))
        new_user = User(user_name=user_name, name=name, password=encrypt_password, email=email, age=age, role=role)
        new_user = new_user.to_dict()
        try:
            self.collection.insert_one(new_user)
        except Exception as exc:
            raise DBError('Failed to insert the user to the db', internal_exception=exc)

    def login(self, user_name: str, password: int):
        details = self.collection.find({
            'username': str(user_name)},
            {
            '_id': 0,
            'name': 0,
            'email': 0,
            'age': 0,
            })
        if self.collection.count_documents({'username': user_name}) == 0:
            raise NotExists('Username doesn\'t exist')
        for user in details:
            if user['username'] == user_name and self.hash.verify(str(password), user['password']):
                return {'username': user['username'], 'role': user['role']}
            else:
                raise NotFound('Username or password are incorrect')

    def update_user(self, u_id: int, name: str, age: int, email:str, role:str, user_name:str):
        try:
            validation(name=name, age=age, email=email, user_name=user_name)
            if self.is_authorized(user_name):
                user_objects = [users_id for users_id in self.collection.find({'_id': ObjectId(u_id)})]
                if len(user_objects) != 1:
                    raise NotFound('Failed to find user with such id in the DB')
            raise NotAuthorized('You are not authorized!')
            user_id = user_objects[0]
            self.collection.replace_one({
                'name': user_id['name'],
                'age': user_id['age'],
                'email': user_id['email'],
                'username': user_id['username'],
                'password': user_id['password'],
                'role': user_id['role']},
                {
                'name': name,
                'age': age,
                'email': email,
                'username': user_id['username'],
                'password': user_id['password'],
                'role': role
                })
        except Exception as exc:
            raise DBError('Failed to insert the user to the db', internal_exception=exc)

    def delete_user(self, _id):
        try:
                self.collection.delete_one({'_id': ObjectId(_id)})
                return {}
        except Exception as exc:
            raise DBError('Failed to delete the user from the db', internal_exception=exc)

    def list_users(self, user_name) -> dict:
            try:
                if self.is_authorized(user_name):
                    user_list = self.collection.find({})
                    parsed_user_list = []
                    for user in user_list:
                        parsed_user_list.append({
                            'id': str(user['_id']),
                            'username': user['username'],
                            'name': user['name'],
                            'email': user['email'],
                            'age': user['age'],
                            'role': user['role']})
                    all_users = {
                        'users': parsed_user_list
                    }
                    return all_users
            except Exception as exc:
                raise DBError('Failed to get the users from the db', internal_exception=exc)
            raise NotAuthorized('You are not authorized!')

    def is_authorized(self, user_name) -> bool:
        user_details = self.collection.find({
            'username': str(user_name)},
            {
            '_id': 0,
            'username': 0,
            'password': 0,
            'name': 0,
            'email': 0,
            'age': 0
            })

        for details in user_details:
            if details['role'] == 'admin':
                return True
            return  False