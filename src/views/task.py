from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from src.database import db
from src.models.task import Task
#from controllers.user import handle_user

task_views = Blueprint('task_views', __name__, template_folder='../templates')

@task_views.route('/tarefa/<id>', methods=['GET'])
def index_page(id):
    return render_template('tasks.html', id_project = id)

@task_views.route('/editar_tarefa/<id>', methods=['GET'])
def edit_page(id):
    task = Task.query.filter_by(id_task=id).first()
    if not task:
        return jsonify({
            "task": None
        })
    deadline = task.deadline
    deadline = deadline.strftime("%d/%m/%Y")
    ts = {
            "id_task": task.id_task,
            "id_project": task.id_project,
            "title": task.title,
            "deadline": deadline,
            "description": task.description
        }
    return render_template('edit_task.html', task = ts)