from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from src.database import db
#from controllers.user import handle_user

customer_views = Blueprint('customer_views', __name__, template_folder='../templates')

@customer_views.route('/customers', methods=['GET'])
def index_page():
    return render_template('customers.html')

@customer_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    #handle_user('bob', 'bobpass')
    return jsonify(message='db initialized!')

@customer_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})