import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import db
from models.project import Project
from flask_jwt_extended import get_jwt_identity, jwt_required
project = Blueprint("project",__name__,url_prefix="/api/v1/project")

@project.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_project():
    current_user = get_jwt_identity()
    if request.method == "POST":
        customer = request.get_json().get("customer", "")
        description = request.get_json().get("description", "")
        full_value = request.get_json().get("full_value", "")
        
        if Project.query.filter_by(customer=customer,description=description, full_value=full_value).first():
            return jsonify({
                "error": "project already exists."
            }), HTTP_409_CONFLICT

        project = Project(
            customer = customer, 
            description = description,
            full_value = full_value
        )

        db.session.add(project)
        db.session.commit()

        return jsonify({
            "customer": project.customer,
            "full_value": project.full_value,
            "description": project.description
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        project = Project.query.paginate(page=page, per_page=per_page)
        
        data = []
        for project in project.items:
            data.append({
                "customer": project.customer,
                "full_value": project.full_value,
                "description": project.description
            })
        meta = {
            "page": project.page,
            "pages": project.pages,
            "total": project.total,
            "prev_page": project.prev_num,
            "next_page": project.next_num,
            "has_next": project.has_next,
            "has_prev": project.has_prev
        }
        return jsonify ({
            "data": data,
            "meta": meta
        }), HTTP_200_OK
        
@project.get("/<int:id>")
@jwt_required()
def get_project(id):
    project = Project.query.filter_by(id=id).first()
    if not project:
        return jsonify({
            "message": "Item not found."
        })
    return jsonify({
        "customer": project.customer,
        "full_value": project.full_value,
        "description": project.description
    }), HTTP_200_OK

@project.put("/<int:id>")
@project.patch("/<int:id>")
@jwt_required()
def edit_project(id):
    project = Project.query.filter_by(id=id).first()
    if not project:
        return jsonify({
            "message": "Item not found."
        })
    
    customer = request.get_json().get("customer", "")
    description = request.get_json().get("description", "")
    full_value = request.get_json().get("full_value", "")
        
    project.customer = customer
    project.description = description
    project.full_value = full_value

    db.session.commit()

    return jsonify({
        "id": project.id,
        "name": project.name
    }), HTTP_201_CREATED

@project.delete("/<int:id>")
@jwt_required()
def delete_project(id):
    project = Project.query.filter_by(id=id).first()
    if not project:
        return jsonify({
            "message": "Item not found."
        })
    db.session.delete(project)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
