from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from src.database import db
#from controllers.user import handle_user

project_views = Blueprint('project_views', __name__, template_folder='../templates')

@project_views.route('/projetos', methods=['GET'])
def index_page():
    link_voltar = "/"
    id_customer = ""
    return render_template('projects.html', link_voltar = link_voltar, id_customer= id_customer)

@project_views.route('/projetos/<id>', methods=['GET'])
def projects_by_customer_page(id):
    link_voltar = "/clientes"
    return render_template('projects.html', id_customer = id, link_voltar = link_voltar)

@project_views.route('/adicionar_projeto', methods=['GET'])
def create_project_page():
    return render_template('create_project.html')


@project_views.route('/exibir_projeto/<id>', methods=['GET'])
def show_project_page(id):
    return render_template('show_project.html', id_project = id)