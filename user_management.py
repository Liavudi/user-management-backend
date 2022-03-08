from typing import List
from pymongo import MongoClient
from bson import ObjectId
from user import User
from consts import DBURL, DB


class UserManagment():
    def __init__(self):
        self.userlist: List[User] = []
        self.client = MongoClient(DBURL)
        self.db = self.client[DB]
        self.collection = self.db.users

    def add_user(self, name: str, age: int):
        if len(name) <= 2:
            raise Exception('Name is less than 2 letters.')
        if age < 18:
            raise Exception('You must be over 18')

        new_user = User(name, age)
        new_user = new_user.to_dict()
        # TODO: add error handling in case the insertion fails
        self.collection.insert_one(new_user)

    def update_user(self, u_id: int, name: str, age: int):
        user_objects = [users_id for users_id in self.collection.find({'_id': ObjectId(u_id)})]
        if len(user_objects) != 1:
            raise Exception('Failed to find user with such id in the DB')
        user_id = user_objects[0]

        self.collection.replace_one({'name': user_id['name'], 'age': user_id['age']}, {
            'name': name,
            'age': age
        })
        return {}

    def delete_user(self, _id):
        self.collection.delete_one({'_id': ObjectId(_id)})
        return {}

    def show_user_list(self):
        for user in self.userlist:
            user.print_user()

    def list_users(self) -> dict:
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



