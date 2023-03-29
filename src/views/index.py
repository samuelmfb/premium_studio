from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from src.database import db
from src.init_db import init_db
from src.models.user import User
from src.models.user_role import UserRole
#from controllers.user import handle_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route('/novo_usuario', methods=['GET'])
def new_user_page():
    return render_template('new_user.html')

@index_views.route('/gestao', methods=['GET'])
def management_page():
    return render_template('management.html')

@index_views.route('/acessos', methods=['GET'])
def permissions_page():
    users = User.query.all()
        
    
    usr = []
    for user in users:
        user_role = None
        if user.id_user_role != None:
            user_role = user.user_role.user_role

        usr.append({
            "id_user": user.id_user,
            "user_role": user_role,
            "user_name": user.user_name,
            "email": user.email,
            "password": user.password,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        })

    user_roles = UserRole.query.all()
    roles = []
    for user_role in user_roles:
        roles.append({
            "id_user_role": user_role.id_user_role,
            "user_role": user_role.user_role,
        })
        
    return render_template('permissions.html', user_role = roles, users = usr)

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    response_db = init_db()
    #handle_user('bob', 'bobpass')
    return jsonify(message=response_db)

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})