from pymongo import MongoClient
from consts import DBURL, DB
from bson import ObjectId
from exceptions import *


class TodoManagement:
    def __init__(self):
        self.client = MongoClient(DBURL)
        self.db = self.client[DB]
        self.todo_collection = self.db.todos

    def create_todo_list(self, user_name, todo):
        try:
            dict = {
                'ownerId': user_name,
                'text': todo
            }
            self.todo_collection.insert_one(dict)
        except Exception as exc:
            raise DBError('Failed to insert the todo to the db', internal_exception=exc)
        return {}

    def delete_todo_list(self, user_name):
        try:
            d = self.todo_collection.delete_many({'ownerId': user_name})
        except Exception as exc:
            raise DBError('Failed to delete the todo from the db', internal_exception=exc)
        return {}
    
    def get_todo_list(self, user_id):
        try:
            parsed_todo_list = []
            todo_list = self.todo_collection.find({'ownerId': user_id}, {'ownerId': 1, 'text': 1, })
            for todo in todo_list:
                parsed_todo_list.append({
                    '_id': str(todo['_id']),
                    'ownerId': todo['ownerId'],
                    'text': todo['text']
                })
            all_todos = {
                'data': parsed_todo_list
            }
            return all_todos
        except Exception as exc:
            raise DBError('Failed to get the todos from the db', internal_exception=exc)

    def delete_todo(self, todo_id):
        try:
            self.todo_collection.delete_one({'_id': ObjectId(todo_id)})
        except Exception as exc:
            raise DBError('Failed to delete the todo from the db', internal_exception=exc)
        return {}