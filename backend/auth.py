from flask_restx import Namespace, Resource, fields
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
# Line split for PEP8 compliance
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token,
                                get_jwt_identity, jwt_required)
from flask import request, jsonify, Flask, make_response

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
            access_token = create_access_token(identity=db_user.id,
                                               fresh=True)
            refresh_token = create_refresh_token(identity=db_user.id)

            return jsonify({"access_token": access_token,
                            "refresh_token": refresh_token})
        else:
            return jsonify({"message": "Invalid Username or Password"}), 401


@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)

        response = {
            "access_token": new_access_token
        }

        return jsonify(response), 200
