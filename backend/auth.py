from flask_restx import Namespace, Resource, fields
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import request, jsonify

# Namespace as blueprint

auth_ns = Namespace('auth_ns', description='A namespace for Authentication')

signup_model = auth_ns.model(
    'SignUp',
    {
        "username": fields.String(),
        "password": fields.String()
    }
)

login_model = auth_ns.model(
    'Login',
    {
        "username": fields.String(),
        "password": fields.String()
    }
)


@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.marshal_with(signup_model)
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()

        username = data.get("username").lower()

        db_user = User.query.filter(User.username == username).first()
        if db_user:
            return {'message': 'User already Exists'}, 409

        new_user = User(
            username=data.get('username'),
            password=generate_password_hash(data.get('password'))
        )
        new_user.save_to_db()

        return {
            "Message": "User Created Successfully"
        }, 201


@auth_ns.route('/login')
class Login(Resource):

    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Check User and Password
        db_user = User.query.filter(User.username == username).first()
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username, fresh=True)
            refresh_token = create_refresh_token(identity=db_user.username)

            return jsonify({"access_token": access_token, "refresh_token": refresh_token})
