import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import db
from src.models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime
user = Blueprint("user",__name__,url_prefix="/api/v1/user")

@user.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_user():
    current_user = get_jwt_identity()
    if request.method == "POST":
        id_user = request.get_json().get("id_user", "")
        id_user_role = request.get_json().get("id_user_role", "")
        user_name = request.get_json().get("user_name", "")
        email = request.get_json().get("email", "")
        password = request.get_json().get("password", "")

        if User.query.filter_by(id_user = id_user, user_name=user_name).first():
            return jsonify({
                "error": "Usuário já existe."
            }), HTTP_409_CONFLICT

        user = User(
            id_user = id_user,
            id_user_role = id_user_role,
            user_name = user_name,
            email = email,
            password = password
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "id_user": user.id_user,
            "user_role_name": user.user_role_name,
            "user_name": user.user_name,
            "email": user.email,
            "password": user.password,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        users = User.query.paginate(page=page, per_page=per_page)
        
        data = []
        for user in users.items:
            
            data.append({
                "id_user": user.id_user,
                "user_role_name": user.user_role.user_role_name,
                "user_name": user.user_name,
                "email": user.email,
                "password": user.password,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            })
        meta = {
            "page": users.page,
            "pages": users.pages,
            "total": users.total,
            "prev_page": users.prev_num,
            "next_page": users.next_num,
            "has_next": users.has_next,
            "has_prev": users.has_prev
        }
        return jsonify ({
            "data": data,
            "meta": meta
        }), HTTP_200_OK
        
@user.get("/<int:id>")
@jwt_required()
def get_user(id):
    user = User.query.filter_by(id_user=id).first()

    if not user:
        return jsonify({
            "message": "Item não encontrado."
        })
    
    return jsonify({
        "id_user": user.id_user,
        "user_role_name": user.user_role.user_role_name,
        "user_name": user.user_name,
        "email": user.email,
        "password": user.password,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }), HTTP_200_OK

@user.put("/<int:id>")
@user.patch("/<int:id>")
@jwt_required()
def edit_user(id):
    user = User.query.filter_by(id_user=id).first()
    if not user:
        return jsonify({
            "message": "Item não encontrado."
        })
    
    id_user = id
    id_user_role = request.get_json().get("id_user_role", "")
    user_name = request.get_json().get("user_name", "")
    email = request.get_json().get("email", "")
    updated_at = datetime.now()

    
    if user_name:
        user.user_name = user_name
    if id_user_role:
        user.id_user_role = id_user_role
    if email:
        user.email = email

    user.updated_at = updated_at

    db.session.commit()

    return jsonify({
        "id_user": user.id_user,
        "user_role_name": user.user_role_name,
        "user_name": user.user_name,
        "email": user.email,
        "password": user.password,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }), HTTP_201_CREATED

@user.delete("/<int:id>")
@jwt_required()
def delete_user(id):
    user = User.query.filter_by(id_user=id).first()
    if not user:
        return jsonify({
            "message": "Item não encontrado."
        })
    db.session.delete(user)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
