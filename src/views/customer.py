from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from src.database import db
#from controllers.user import handle_user

customer_views = Blueprint('customer_views', __name__, template_folder='../templates')

@customer_views.route('/clientes', methods=['GET'])
def index_page():
    return render_template('customers.html')

@customer_views.route('/adicionar_cliente', methods=['GET'])
def create_customer_page():
    return render_template('create_customer.html')
