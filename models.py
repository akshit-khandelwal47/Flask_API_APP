from app import db
import uuid
from flask_restful import reqparse, fields


class UserData(db.Model):
    id = db.Column(db.String, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __init__(self, username, email, full_name, age, gender):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.age = age
        self.gender = gender

db.create_all()

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='Username is required')
parser.add_argument('email', type=str, required=True, help='Email is required')
parser.add_argument('full_name', type=str, required=True, help='Full name is required')
parser.add_argument('age', type=int, required=True, help='Age is required')
parser.add_argument('gender', type=str, required=True, help='Gender is required')

resource_fields = {
    'user_id': fields.String(attribute='id'),
    'username': fields.String,
    'email': fields.String,
    'full_name': fields.String,
    'age': fields.Integer,
    'gender': fields.String
}