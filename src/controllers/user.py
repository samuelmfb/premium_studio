import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import db
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required
user = Blueprint("user",__name__,url_prefix="/api/v1/user")

@user.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_user():
    current_user = get_jwt_identity()
    if request.method == "POST":
        id_user = request.get_json().get("id_user", "")
        user_role = request.get_json().get("user_role", "")
        user_name = request.get_json().get("user_name", "")
        email = request.get_json().get("email", "")
        password = request.get_json().get("password", "")
        created_at = request.get_json().get("created_at", "")
        updated_at = request.get_json().get("updated_at", "")

        if user.query.filter_by(id_role = id_user, role_name=user_name).first():
            return jsonify({
                "error": "user already exists."
            }), HTTP_409_CONFLICT

        user = User(
            id_user = id_user,
            user_role = user_role,
            user_name = user_name,
            email = email,
            password = password,
            created_at = created_at,
            updated_at = updated_at
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "id_user": user.id_user,
            "user_role": user.user_role,
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
                "user_role": user.user_role,
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
def get_user(id_role):
    user = User.query.filter_by(id_role=id_role).first()
    if not user:
        return jsonify({
            "message": "Item not found."
        })
    return jsonify({
        "id_user": user.id_user,
        "user_role": user.user_role,
        "user_name": user.user_name,
        "email": user.email,
        "password": user.password,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }), HTTP_200_OK

@user.put("/<int:id>")
@user.patch("/<int:id>")
@jwt_required()
def edit_user(id_role):
    user = User.query.filter_by(id_role=id_role).first()
    if not user:
        return jsonify({
            "message": "Item not found."
        })
    
    id_user = request.get_json().get("id_user", "")
    user_role = request.get_json().get("user_role", "")
    user_name = request.get_json().get("user_name", "")
    email = request.get_json().get("email", "")
    password = request.get_json().get("password", "")
    created_at = request.get_json().get("created_at", "")
    updated_at = request.get_json().get("updated_at", "")

    user.id_user = id_user
    user.user_role = user_role
    user.user_name = user_name
    user.email = email
    user.password = password
    user.created_at = created_at
    user.updated_at = updated_at

    db.session.commit()

    return jsonify({
        "id_user": user.id_user,
        "user_role": user.user_role,
        "user_name": user.user_name,
        "email": user.email,
        "password": user.password,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }), HTTP_201_CREATED

@user.delete("/<int:id>")
@jwt_required()
def delete_user(id_role):
    user = User.query.filter_by(id_role=id_role).first()
    if not user:
        return jsonify({
            "message": "Item not found."
        })
    db.session.delete(user)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
