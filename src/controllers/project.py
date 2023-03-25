import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import db
from src.models.project import Project
from flask_jwt_extended import get_jwt_identity, jwt_required
project = Blueprint("project",__name__,url_prefix="/api/v1/project")

@project.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_project():
    current_user = get_jwt_identity()
    if request.method == "POST":
        id_customer = request.get_json().get("id_customer", "")
        description = request.get_json().get("description", "")
        full_value = request.get_json().get("full_value", "")
        id_producer = request.get_json().get("id_producer", "")
        
        if Project.query.filter_by(id_customer = id_customer).first():
            return jsonify({
                "error": "Projeto já existe."
            }), HTTP_409_CONFLICT

        project = Project(
            id_customer = id_customer, 
            description = description,
            full_value = full_value,
            id_producer = id_producer
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
        projects = Project.query.paginate(page=page, per_page=per_page)
        
        data = []
        for project in projects.items:
            data.append({
                "id_project": project.id_project,
                "customer": project.customer.name,
                "full_value": project.full_value,
                "description": project.description
            })
        meta = {
            "page": projects.page,
            "pages": projects.pages,
            "total": projects.total,
            "prev_page": projects.prev_num,
            "next_page": projects.next_num,
            "has_next": projects.has_next,
            "has_prev": projects.has_prev
        }
        return jsonify ({
            "data": data,
            "meta": meta
        }), HTTP_200_OK
        
@project.get("/<int:id>")
@jwt_required()
def get_project(id):
    project = Project.query.filter_by(id_project=id).first()
    if not project:
        return jsonify({
            "message": "Item não encontrado."
        })
    return jsonify({
        "id_project": project.id_project,
        "customer": project.customer.name,
        "full_value": project.full_value,
        "producer": project.producer.name,
        "description": project.description
    }), HTTP_200_OK

@project.get("/customer/<int:id>")
@jwt_required()
def get_project_by_customer(id):
    projects = Project.query.filter_by(id_customer=id).all()
    if not projects:
        return jsonify({
            "message": "Item não encontrado."
        })
    
    data = []
    if len(projects) == 0:
        return jsonify ({
            "data": None,
        }), HTTP_200_OK
    for project in projects:
        data.append({
            "id_project": project.id_project,
            "customer": project.customer.name,
            "full_value": project.full_value,
            "producer": project.producer.name,
            "description": project.description
        })
    return jsonify ({
        "data": data,
    }), HTTP_200_OK

@project.put("/<int:id>")
@project.patch("/<int:id>")
@jwt_required()
def edit_project(id):
    project = Project.query.filter_by(id_project=id).first()
    if not project:
        return jsonify({
            "message": "Item não encontrado."
        })
    
    id_customer = request.get_json().get("id_customer", "")
    description = request.get_json().get("description", "")
    full_value = request.get_json().get("full_value", "")
    id_project = request.get_json().get("id_project", "")
    
    if id_customer:
        project.id_customer = id_customer
    if description:
        project.description = description
    if full_value:
        project.full_value = full_value
    if id_project:
        project.id_project = id_project


    db.session.commit()

    return jsonify({
        "id": project.id_project,
        "name": project.description
    }), HTTP_201_CREATED

@project.delete("/<int:id>")
@jwt_required()
def delete_project(id):
    project = Project.query.filter_by(id_project=id).first()
    if not project:
        return jsonify({
            "message": "Item não encontrado."
        })
    db.session.delete(project)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
