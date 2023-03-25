from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from src.database import db
#from controllers.user import handle_user

task_views = Blueprint('task_views', __name__, template_folder='../templates')

@task_views.route('/tarefa/<id>', methods=['GET'])
def index_page(id):
    return render_template('tasks.html', id_project = id)
