from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from src.database import db
#from controllers.user import handle_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route('/gestao', methods=['GET'])
def management_page():
    return render_template('management.html')

@index_views.route('/acessos', methods=['GET'])
def permissions_page():
    return render_template('permissions.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    #handle_user('bob', 'bobpass')
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})