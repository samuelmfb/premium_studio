from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from src.database import db
from src.controllers.producer import Producer
from src.controllers.customer import Customer
from src.controllers.task import Task
from src.controllers.project import Project
#from controllers.user import handle_user
from datetime import datetime

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
    producers = Producer.query.all()
        
    prods = []
    for producer in producers:
        prods.append({
            "id_producer": producer.id_producer,
            "name": producer.name,
        })

    customers = Customer.query.all()
        
    custs = []
    for customer in customers:
        custs.append({
            "id_customer": customer.id_customer,
            "name": customer.name
        })
    return render_template('create_project.html', producers = prods, customers = custs)


@project_views.route('/exibir_projeto/<id>', methods=['GET'])
def show_project_page(id):
    project = Project.query.filter_by(id_project = id).first()
    
    pj = {
        "name": project.name,
        "id_project": project.id_project,
        "customer": project.customer.name,
        "producer": project.producer.name,
        "full_value": project.full_value,
        "description": project.description,
    }

    tasks = Task.query.filter_by(id_project = id).all()
    
    ts = []
    if len(tasks) == 0:
        return render_template('show_project.html', project = pj, tasks = None)
    for task in tasks:
        checked = ""
        if task.finished != None:
            checked = "checked"

        deadline = task.deadline
        deadline = deadline.strftime("%d/%m/%Y")
        #deadline = datetime.strptime(deadline, "%d/%m/%Y")
        ts.append({
            "id_task": task.id_task,
            "checked": checked,
            "title": task.title,
            "deadline": deadline,
            "description": task.description
        })

    


    return render_template('show_project.html', tasks = ts, project = pj)