from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from src.database import db
#from controllers.user import handle_user

project_views = Blueprint('project_views', __name__, template_folder='../templates')

@project_views.route('/projetos', methods=['GET'])
def index_page():
    return render_template('projects.html')

@project_views.route('/adicionar_projeto', methods=['GET'])
def create_project_page():
    return render_template('create_project.html')


@project_views.route('/exibir_projeto/<id>', methods=['GET'])
def show_project_page(id):
    return render_template('show_project.html', id_project = id)