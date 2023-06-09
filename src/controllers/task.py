import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_403_FORBIDDEN
from src.database import db
from src.models.task import Task
from src.models.user import User
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
task = Blueprint("task",__name__,url_prefix="/api/v1/task")

@task.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_task():
    current_user = get_jwt_identity()
    if request.method == "POST":
        id_project = request.get_json().get("id_project", "")
        title = request.get_json().get("title", "")
        description = request.get_json().get("description", "")
        deadline = request.get_json().get("deadline", "")
        started = datetime.now()
        if deadline:
            deadline = datetime.strptime(deadline, '%d/%m/%Y').date()
        else:
            deadline = None

        if Task.query.filter_by(title = title, id_project = id_project).first():
            return jsonify({
                "error": "A tarefa já existe."
            }), HTTP_409_CONFLICT

        task = Task(
            id_project = id_project,
            description = description,
            deadline = deadline,
            title = title,
            started = started
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({
            "id_task": task.id_task,
            "title": task.title,
            "description": task.description
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        tasks = Task.query.paginate(page=page, per_page=per_page)
        
        data = []
        for task in tasks.items:
            data.append({
                "id_task": task.id_task,
                #"project": task.project.description,
                #"producer": task.producer.name,
                "deadline": task.deadline,
                "started": task.started,
                "finished": task.finished,
                "title": task.title,
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
            "message": "Item não encontrado."
        })
    return jsonify({
        "id": task.id_task,
        "description": task.description
    }), HTTP_200_OK

@task.get("/project/<int:id>")
@jwt_required()
def list_tasks_by_project(id):
    tasks = Task.query.filter_by(id_project = id).all()
    
    data = []
    if len(tasks) == 0:
        return jsonify ({
            "data": None,
        }), HTTP_200_OK
    for task in tasks:
        deadline = task.deadline
        deadline = deadline.strftime('%Y-%m-%d')
        data.append({
            "id_task": task.id_task,
            "project": task.project.description,
            "deadline": deadline,
            "started": task.started,
            "finished": task.finished,
            "title": task.title,
            "description": task.description
        })
    return jsonify ({
        "data": data,
    }), HTTP_200_OK

@task.put("/<int:id>")
@task.patch("/<int:id>")
@jwt_required()
def edit_task(id):
    task = Task.query.filter_by(id_task=id).first()
    if not task:
        return jsonify({
            "message": "Item não encontrado."
        })
    
    id_producer = request.get_json().get("id_producer", "")
    id_project = request.get_json().get("id_project", "")
    description = request.get_json().get("description", "")
    title = request.get_json().get("title", "")
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
        deadline = datetime.strptime(deadline, '%d/%m/%Y').date()
        task.deadline = deadline
    if finished:
        task.finished = finished
    if title:
        task.title = title

    db.session.commit()

    return jsonify({
        "id": task.id_task,
        "name": task.description
    }), HTTP_200_OK

@task.delete("/<int:id>")
@jwt_required()
def delete_task(id):
    id_user = get_jwt_identity()
    user = User.query.filter_by(id_user = id_user).first()
    
    if user.user_role.user_role != "Gerente":
        return jsonify({
            "message": "Usuário não possui privilégio de acesso para excluir tarefas."
        })
    task = Task.query.filter_by(id_task=id).first()
    if not task:
        return jsonify({
            "message": "Item não encontrado."
        })
    db.session.delete(task)
    db.session.commit()

    return jsonify({"message" : "Tarefa excluída."}), HTTP_204_NO_CONTENT

@task.post("/toggle/")
@jwt_required()
def toggle_task():
    id_user = get_jwt_identity()
    user = User.query.filter_by(id_user = id_user).first()
    if user.user_role.user_role not in ("Gerente", "Produtor"):
        return jsonify({
            "error": "Usuário não possui privilégio de acesso para concluir tarefas."
        }), HTTP_403_FORBIDDEN
    
    id_task = request.get_json().get("id_task", "")
    finished = request.get_json().get("finished", "")
    task = Task.query.filter_by(id_task=id_task).first()
    if not task:
        return jsonify({
            "message": "Item não encontrado."
        })
    if finished:
        finished = datetime.now()
    else:
        finished = None    

    task.finished = finished

    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT