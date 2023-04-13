import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import db
from src.models.user_role import UserRole
from flask_jwt_extended import get_jwt_identity, jwt_required
user_role = Blueprint("user_role",__name__,url_prefix="/api/v1/user_role")

@user_role.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_user_role():
    current_user = get_jwt_identity()
    if request.method == "POST":
        id_user_role = request.get_json().get("id_user_role", "")
        user_role = request.get_json().get("user_role", "")

        if UserRole.query.filter_by(user_role=user_role).first():
            return jsonify({
                "error": "Papel já existe."
            }), HTTP_409_CONFLICT

        user_role = UserRole(
            user_role = user_role
        )

        db.session.add(user_role)
        db.session.commit()

        return jsonify({
            "id_user_role": user_role.id_user_role,
            "user_role": user_role.user_role
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        user_roles = UserRole.query.paginate(page=page, per_page=per_page)
        
        data = []
        for user_role in user_roles.items:
            data.append({
                "id_user_role": user_role.id_user_role,
                "user_role": user_role.user_role
            })
        meta = {
            "page": user_roles.page,
            "pages": user_roles.pages,
            "total": user_roles.total,
            "prev_page": user_roles.prev_num,
            "next_page": user_roles.next_num,
            "has_next": user_roles.has_next,
            "has_prev": user_roles.has_prev
        }
        return jsonify ({
            "data": data,
            "meta": meta
        }), HTTP_200_OK
        
@user_role.get("/<int:id>")
@jwt_required()
def get_user_role(id):
    user_role = UserRole.query.filter_by(id_user_role=id).first()
    if not user_role:
        return jsonify({
            "message": "Item não encontrado."
        })
    return jsonify({
        "id_user_role": user_role.id_user_role,
        "user_role": user_role.user_role
    }), HTTP_200_OK

@user_role.put("/<int:id>")
@user_role.patch("/<int:id>")
@jwt_required()
def edit_user_role(id):
    user_role = UserRole.query.filter_by(id_user_role=id).first()
    if not user_role:
        return jsonify({
            "message": "Item não encontrado."
        })
    
    user_role = request.get_json().get("user_role", "")

    user_role.user_role = user_role

    db.session.commit()

    return jsonify({
        "id_user_role": user_role.id_user_role,
        "user_role": user_role.user_role
    }), HTTP_200_OK

@user_role.delete("/<int:id>")
@jwt_required()
def delete_user_role(id):
    user_role = UserRole.query.filter_by(id_user_role=id).first()
    if not user_role:
        return jsonify({
            "message": "Item não encontrado."
        })
    db.session.delete(user_role)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
