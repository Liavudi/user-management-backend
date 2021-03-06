import datetime
from user_management import UserManagement
from todo_management import TodoManagement
from flask import Flask, request, Response, session
from flask_cors import CORS
import json
from exceptions import *

app = Flask("UserManagement")
um = UserManagement()
tm = TodoManagement()
cors = CORS(app, supports_credentials=True)
app.secret_key = '5#dwda1d23wa]/'
app.permanent_session_lifetime = datetime.timedelta(days=1)
app.config.update(
    SECRET_KEY='test',
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="None"
)


@app.route('/', methods=['POST'])
def index():
    error_message = 'Couldn\'t reach the DB. Try again later'
    return Response(json.dumps({
        'error': {
            'message': error_message
        }
    }), status=400, mimetype='application/json')


@app.route("/users", methods=['POST'])
def create_user():
    input_data = json.loads(request.data)
    try:
        um.add_user(user_name=input_data.get('username'),
                    name=input_data.get('name'),
                    password=input_data.get('password'),
                    email=input_data.get('email'),
                    age=input_data.get('age'))
        return Response(json.dumps({
                'data': 'User Created Successfully'
        }), status=201)
    except InvalidInputError as exc:
        return Response(json.dumps({
            'error': {
                'message': exc.message
            }
        }
        ), status=400)
    except DBError:
        return Response(json.dumps({
            'error': {
                'message': 'Service unavailable'
            }
        }), status=503)
    except AlreadyExists as exc:
        return Response(json.dumps({
            'error': {
                'message': exc.message
            }
        }),status = 500)
    except Exception:
        return Response(json.dumps({
            'error': {
                'message': 'Internal server error'
            }
        }), status=500)


@app.route("/users/<user_name>/<user_id>", methods=['DELETE'])
def delete_user(user_name, user_id):
    try:
        um.delete_user(user_id)
        tm.delete_todo_list(user_name)
        return Response(json.dumps({
            'data': 'User deleted successfully!'
        }))
    except NotFound as exc:
        return Response(json.dumps({
            'error': {
                'message': exc.message
            }
        }), status=404)
    except Exception:
        return Response(json.dumps({
            'error': {
                'message': 'Internal server error'
            }
        }), status=500)


@app.route("/users/", methods=['GET'])
def list_users():
    try:
        if 'username' in session:
            user_name = session['username']
            user_list = um.list_users(user_name)
            return user_list
        else:
            return Response(json.dumps({
                'error': {
                    'message': 'You are not the user!'
                }
            }), status=401)
    except DBError:
        return Response(json.dumps({
            'error': {
                'message': 'Service unavailable'
            }
        }), status=503)

    except NotAuthorized as exc:
        return Response(json.dumps({
            'error': {
                'message': exc.message
            }
        }), status=401)

    except Exception:
        return Response(json.dumps({
            'error': {
                'message': 'Internal server error'
            }
        }), status=500)


@app.route("/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    try:
        if 'username' in session:
            logged_user = session['username']
        data = json.loads(request.data)
        um.update_user(user_id, name=data.get('name'), age=data.get('age'), email=data.get('email'), role=data.get('role'), user_name= data.get('username'), logged=logged_user)
        return Response(json.dumps({
            'data': 'User has been updated successfully'
        }), status=200)
    except InvalidInputError as exc:
        return Response(json.dumps({
            'error': {
                'message': exc.message
            }
        }), status=400)
    except NotAuthorized as exc:
        return Response(json.dumps({
            'error': {
                'message': exc.message
            }
        }), status=401)
    except DBError as exc:
        return Response(json.dumps({
            'error': {
                'message': exc.message
            }
        }), status=503)


@app.route("/login", methods=['POST'])
def log_in():
    try:
        input_data = json.loads(request.data)
        login_details = um.login(user_name=input_data.get('userName'), password=input_data.get('password'))
        session['username'] = str(input_data.get('userName'))
        return Response(json.dumps({
                'data': login_details
        }), status=200)
    except NotExists as exc:
        return Response(json.dumps({
            'error':{
                'message': exc.message
            }
        }), status=404)
    except NotFound as exc:
        return Response(json.dumps({
            'error': {
                'message': exc.message
            }
        }), status=404)
    except Exception:
        return Response(json.dumps({
            'error': {
                'message': 'Internal server error'
            }
        }), status=500)


@app.route("/logout", methods=['POST'])
def log_out():
    if 'username' in session:
        session.pop('username', default=None)
        return Response(json.dumps({
            'data': 'User has logged out successfully!'
        }),status=200)
    return Response(json.dumps({
        'error':{
            'message': 'User isn\'t logged in'
        }
    }),status=405)


@app.route("/todolist", methods=['POST'])
def create_todo():
    try:
        input_data = json.loads(request.data)
        tm.create_todo_list(user_name=input_data.get('user'), todo=input_data.get('todo'))
        return Response(json.dumps({
            'data': 'Todo created Successfully!'
        }), status=201)
    except NotFound as exc:
        return Response(json.dumps({
            'error': {
                'message': exc.message
            }
        }), status=404)
    except Exception:
        return Response(json.dumps({
            'error': {
                'message': 'Internal server error'
            }
        }), status=500)


@app.route("/todolist/", methods=['GET'])
def get_todo():
    try:
        if 'username' in session:
            user_id = session['username']
            return tm.get_todo_list(user_id)
        else:
            return Response(json.dumps({
                'error': {
                    'message': 'You are not the user!'
                }
            }),status=401)
    except NotFound as exc:
        return Response(json.dumps({
            'error': {
                'message': exc.message
            }
        }), status=404)
    except Exception:
        return Response(json.dumps({
            'error': {
                'message': 'Internal server error'
            }
        }), status=500)


@app.route("/todolist/<todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    try:
        tm.delete_todo(todo_id=todo_id)
        return Response(json.dumps({
            'data': 'User deleted successfully!'

        }))
    except NotFound as exc:
        return Response(json.dumps({
            'error': {
                'message': exc.message
            }
        }), status=404)
    except Exception:
        return Response(json.dumps({
            'error': {
                'message': 'Internal server error'
            }
        }), status=500)




app.run(debug=True)
