from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
# from models import parser,UserData
from flask_restful import reqparse, fields
import uuid
import jwt
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'asdfgjhkl'
app.app_context().push()


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    key = db.Column(db.String(120),unique=True)
    value = db.Column(db.String(120))
    token = db.Column(db.String(500))

    def __init__(self, username, email, full_name, age, gender, password):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.age = age
        self.gender = gender
        self.password = password

    def update_token(self, token):
        self.token = token
        db.session.commit()

    def update_data(self, key, value):
        self.key = key
        self.value = value
        db.session.commit()


db.create_all()

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True,
                    help='Username is required')
parser.add_argument('email', type=str, required=True, help='Email is required')
parser.add_argument('full_name', type=str, required=True,
                    help='Full name is required')
parser.add_argument('age', type=int, required=True, help='Age is required')
parser.add_argument('gender', type=str, required=True,
                    help='Gender is required')
parser.add_argument('password', type=str, required=True,
                    help='Password is required')

resource_fields = {
    'user_id': fields.String(attribute='id'),
    'username': fields.String,
    'email': fields.String,
    'full_name': fields.String,
    'age': fields.Integer,
    'gender': fields.String,
    'password': fields.String
}


@app.route('/api/register', methods=['POST'])
def register():

    args = parser.parse_args()
    required_fields = ['username', 'email',
                       'full_name', 'age', 'gender', 'password']
    missing_fields = [
        field for field in required_fields if not getattr(args, field, None)]
    if missing_fields:
        error_response = {
            "status": "error",
            "code": "INVALID_REQUEST",
            "message": "Invalid request. Please provide all required fields: {}.".format(", ".join(missing_fields))
        }
        return jsonify(error_response), 400
    
    existing_user = UserData.query.filter_by(username=args['username']).first()
    if existing_user:
        error_response = {
            "status": "error",
            "code": "USERNAME_EXISTS",
            "message": "Username already exists. Please choose a different username."
        }
        return jsonify(error_response), 400
    
    existing_email = UserData.query.filter_by(username=args['username']).first()
    if existing_email:
        error_response = {
            "status": "error",
            "code": "EMAIL_EXISTS",
            "message": "Email already exists. Please choose a different email."
        }
        return jsonify(error_response), 400
    
    if not validate_password(args['password']):
        error_response = {
            "status": "error",
            "code": "INVALID_PASSWORD",
            "message": "Invalid password. Password must be at least 8 characters long and contain a mix of uppercase and lowercase letters, numbers, and special characters."
        }
        return jsonify(error_response), 400
    
    if not isinstance(args['age'],int) or args['age'] <= 0:
        error_response = {
            "status": "error",
            "code": "INVALID_AGE",
            "message": "Invalid age value. Age must be a positive integer."
        }
        return jsonify(error_response), 400
    
    if not args['gender']:
        error_response = {
            "status": "error",
            "code": "GENDER_REQUIRED",
            "message": "Gender field is required. Please specify the gender (e.g., male, female, non-binary)."
        }
        return jsonify(error_response), 400

    new_user = UserData(
        username=request.json['username'],
        email=request.json['email'],
        full_name=request.json['full_name'],
        age=request.json['age'],
        gender=request.json['gender'],
        password=request.json['password']
    )

    db.session.add(new_user)
    db.session.commit()

    response_data = {
        "user_id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "full_name": new_user.full_name,
        "age": new_user.age,
        "gender": new_user.gender
    }

    response = {
        "data": response_data,
        "status": "success",
        "message": "User successfully registered!"

    }

    return jsonify(response), 201


@app.route('/api/token', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'code':'MISSING_FIELDS','message':'Missing fields. Please provide both username and password.'})
    user = UserData.query.filter_by(
        username=username, password=password).first()
    

    if not user:
        return jsonify({'code': 'INVALID_CREDENTIALS','message':'Invalid credentials. The provided username or password is incorrect.'}), 401
  
        

    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                       app.config['SECRET_KEY'], algorithm='HS256')

    user.update_token(token)

    return jsonify({'token': token}), 200


@app.route('/api/data', methods=['POST'])
def store_data():
    user_id = authenticate_user()

    data = request.get_json()
    key = data.get('key')
    value = data.get('value')

    if not key:
        return jsonify({'code':'INVALID_KEY','message': 'The provided key is not valid or missing.'}), 400
    
    if not value:
        return jsonify({'code':'INVALID_VALUE','message': 'The provided value is not valid or missing.'}), 400

    existing_key =  UserData.query.filter_by(key=key).first()
    if existing_key:
        error_response = {
            "status": "error",
            "code": "KEY_EXISTS",
            "message": "The provided key already exists in the database. To update an existing key, use the update API."
        }
        return jsonify(error_response), 400
    user = UserData.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'Invalid user'})
    user.update_data(key, value)

    return jsonify({'message': 'Data stored successfully'}), 201


@app.route('/api/data/<string:key>', methods=['GET'])
def retrieve(key):
    user_id = authenticate_user()

    user = UserData.query.filter_by(id=user_id, key=key).first()
    if not user:
        return jsonify({'code': 'KEY_NOT_FOUND'})

    return jsonify({
        "status": "success",
        "data": {
            "key": key,
            "value": user.value
        }
    }), 200


@app.route('/api/data/<string:key>', methods=['PUT'])
def update(key):

    user_id = authenticate_user()
    user_data = UserData.query.filter_by(id=user_id, key=key).first()
    if not user_data:
        return jsonify({'message': 'KEY_NOT_FOUND'})

    data = request.get_json()
    new_value = data.get('value')

    user_data.value = new_value
    db.session.commit()

    return jsonify({'message': 'Data updated successfully', 'status': 'success'}), 200


@app.route('/api/data/<string:key>', methods=['DELETE'])
def delete_data(key):

    user_id = authenticate_user()
    user = UserData.query.filter_by(id=user_id, key=key).first()
    if not user:
        return jsonify({'message': 'KEY_NOT_FOUND'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Data deleted successfully'})


def authenticate_user():
    token = request.headers.get('Authorization')
    # print("Received headers:", request.headers)
    if not token:
        return jsonify({'message': 'Authorization token missing'}), 401

    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
        return user_id
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


def validate_password(password):

    return len(password) >= 8 and any(char.isupper() for char in password) and any(char.islower() for char in password) and \
            any(char.isdigit() for char in password) and any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?\\" for char in password)


if __name__ == '__main__':
    app.debug = True
    app.run()
