from flask import Blueprint, request, jsonify
import jwt
from werkzeug.security import check_password_hash,generate_password_hash
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from src.database import db
from src.models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token,create_refresh_token
from flasgger import Swagger, swag_from
import validators

auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.post("/register")
@swag_from('./docs/auth/register.yaml')
def register():
    user_name = request.json["user_name"]
    email = request.json["email"]
    password = request.json["password"]

    #validates password length
    if len(password) < 6:
        return jsonify({'error': 'Password is too short.'}), HTTP_400_BAD_REQUEST
    
    #validates user_name length
    if len(user_name) < 6:
        return jsonify({'error': 'User name is too short.'}), HTTP_400_BAD_REQUEST
    
    #validates user_name
    if not user_name.isalnum() or " " in user_name:
        return jsonify({'error': 'User name must be alphanumeric, with no spaces.'}), HTTP_400_BAD_REQUEST

    #validates email
    if not validators.email(email):
        return jsonify({'error': 'Email is not valid.'}), HTTP_400_BAD_REQUEST
    
    #checks if email is unique
    if User.query.filter_by(email = email).first() is not None:
        return jsonify({'error': 'Email is already in use.'}), HTTP_409_CONFLICT
    
    #checks if user_name is unique
    if User.query.filter_by(user_name = user_name).first() is not None:
        return jsonify({'error': 'Email is already in use.'}), HTTP_409_CONFLICT
    
    pwd_hash = generate_password_hash(password)
    user = User(
        user_name = user_name,
        password = pwd_hash,
        email = email
    )

    db.session.add(user)
    db.session.commit()


    return jsonify({
        "message": "User created.",
        "user": {
            "user_name": user_name, "email": email
        }
    }), HTTP_201_CREATED

@auth.post("/login")
@swag_from('./docs/auth/register.yaml')
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    user = User.query.filter_by(email = email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)
        if is_pass_correct:
            refresh = create_refresh_token(identity = user.id_user)
            access = create_access_token(identity = user.id_user)

            return jsonify({
                "user": {
                    "refresh": refresh, 
                    "access": access,
                    "user_name": user.user_name,
                    "email": user.email
                }
            })
    return jsonify ({"error": "Wrong credentials."}), HTTP_401_UNAUTHORIZED


@auth.get("/me")
@jwt_required()
def me():
    id_user = get_jwt_identity()
    user = User.query.filter_by(id_user = id_user).first()

    return jsonify({
        "user": user.user_name,
        "email": user.email
    }), HTTP_200_OK

@auth.get("/token/refresh")
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity
    access = create_access_token(identity = identity)

    return jsonify({
        "access": access
    }), HTTP_200_OK    

