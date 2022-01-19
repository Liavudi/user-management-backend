import requests
from pymongo import MongoClient
from user_managment import UserManagment

from flask import Flask, render_template, request
from flask_cors import CORS
import json
app = Flask("UserManagement")
um = UserManagment()
cors = CORS(app)
client = MongoClient('mongodb://localhost:27017/')
db = client['users']
collection = db.all_users

@app.route('/')
def index():
    return 'no frontend yet'

@app.route("/users",methods=['POST'])
def create_user():
    input_data = json.loads(request.data)
    # id = um.user_id()
    # new_user = User( name=input_data.get('name'), age=input_data.get('age'))
    um.add_user(name=input_data.get('name'),age=input_data.get('age'))
    # for i in input_data:
    #     new_user = User(name=i.get('name'), age=i.get('age'))
    #     um.add_user(new_user)

    return {}
    
@app.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    # input_data = json.loads(request.data)
    # id = input_data.get('id')

    # data = json.loads(request.data)
    # exist_user = User(name=data.get('name'), age=data.get('age'))
    # um.delete_user(exist_user)

       return um.delete_user(user_id)



@app.route("/users", methods=['GET'])
def list_users():
    user_list = um.list_users()
    # response = {
    #     'users': []
    # }
    #
    # response['users'].append(user_list)

    return user_list

# @app.route("/update_age", methods=['PUT'])
# def update_name():
#     data = json.loads(request.data)
#     new_age = data.get('new')
#     exist_user = data.get('age')
#     um.update_user_name(exist_user, new_age)
#     return 'succesfully updated name'

@app.route("/users/<id>", methods=['PUT'])
def update_user(id):
    data = json.loads(request.data)
    um.update_user(id,name= data.get('name'), age=data.get('age'))
    return {}

app.run(debug=True)
