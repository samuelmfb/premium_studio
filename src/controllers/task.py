import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import db
from src.models.task import Task
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
task = Blueprint("task",__name__,url_prefix="/api/v1/task")

@task.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_task():
    current_user = get_jwt_identity()
    if request.method == "POST":
        id_producer = request.get_json().get("id_producer", "")
        id_project = request.get_json().get("id_project", "")
        description = request.get_json().get("description", "")
        deadline = request.get_json().get("deadline", "")
        if deadline:
            deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        else:
            deadline = None

        if Task.query.filter_by(id_project = id_project, id_producer = id_producer, deadline=deadline).first():
            return jsonify({
                "error": "task already exists."
            }), HTTP_409_CONFLICT

        task = Task(
            id_producer = id_producer, 
            id_project = id_project,
            description = description,
            deadline = deadline,
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({
            "id_task": task.id_task,
            "description": task.description
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        tasks = Task.query.paginate(page=page, per_page=per_page)
        
        data = []
        for task in tasks.items:
            data.append({
                "id_task": task.id_task,
                "project": task.project.description,
                "producer": task.producer.name,
                "deadline": task.deadline,
                "started": task.started,
                "finished": task.finished,
                "description": task.description
            })
        meta = {
            "page": tasks.page,
            "pages": tasks.pages,
            "total": tasks.total,
            "prev_page": tasks.prev_num,
            "next_page": tasks.next_num,
            "has_next": tasks.has_next,
            "has_prev": tasks.has_prev
        }
        return jsonify ({
            "data": data,
            "meta": meta
        }), HTTP_200_OK
        
@task.get("/<int:id>")
@jwt_required()
def get_task(id):
    task = Task.query.filter_by(id_task=id).first()
    if not task:
        return jsonify({
            "message": "Item not found."
        })
    return jsonify({
        "id": task.id,
        "description": task.description
    }), HTTP_200_OK

@task.put("/<int:id>")
@task.patch("/<int:id>")
@jwt_required()
def edit_task(id):
    task = Task.query.filter_by(id_task=id).first()
    if not task:
        return jsonify({
            "message": "Item not found."
        })
    
    id_producer = request.get_json().get("id_producer", "")
    id_project = request.get_json().get("id_project", "")
    description = request.get_json().get("description", "")
    deadline = request.get_json().get("deadline", "")
    
    finished = request.get_json().get("finished", "")

    if finished:
        finished = datetime.now()

    if id_producer:
        task.id_producer = id_producer
    if id_project:
        task.id_project = id_project
    if description:
        task.description = description
    if deadline:
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        task.deadline = deadline
    if finished:
        task.finished = finished

    db.session.commit()

    return jsonify({
        "id": task.id_task,
        "name": task.description
    }), HTTP_201_CREATED

@task.delete("/<int:id>")
@jwt_required()
def delete_task(id):
    task = Task.query.filter_by(id_task=id).first()
    if not task:
        return jsonify({
            "message": "Item not found."
        })
    db.session.delete(task)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
