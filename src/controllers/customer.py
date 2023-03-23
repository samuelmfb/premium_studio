import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import db
from src.models.customer import Customer
from flask_jwt_extended import get_jwt_identity, jwt_required
customer = Blueprint("customer",__name__,url_prefix="/api/v1/customer")

@customer.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_customer():
    current_user = get_jwt_identity()
    
    if request.method == "POST":
        name = request.get_json().get("name", "")
        email = request.get_json().get("email", "")
        phone_num = request.get_json().get("phone_num", "")
        #checks if email is valid
        if not validators.email(email):
            return jsonify({
                "error": "Email is invalid."
            }), HTTP_400_BAD_REQUEST

        if Customer.query.filter_by(name=name).first():
            return jsonify({
                "error": "Customer already exists."
            }), HTTP_409_CONFLICT

        customer = Customer(
            name = name, 
            phone_num = phone_num,
            email = email
        )

        db.session.add(customer)
        db.session.commit()

        return jsonify({
            "id_customer": customer.id_customer,
            "name": customer.name
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        customers = Customer.query.paginate(page=page, per_page=per_page)
        
        data = []
        for customer in customers.items:
            data.append({
                "id_customer": customer.id_customer,
                "name": customer.name,
                "email": customer.email,
                "phone_num": customer.phone_num
            })
        meta = {
            "page": customers.page,
            "pages": customers.pages,
            "total": customers.total,
            "prev_page": customers.prev_num,
            "next_page": customers.next_num,
            "has_next": customers.has_next,
            "has_prev": customers.has_prev
        }
        return jsonify ({
            "data": data,
            "meta": meta
        }), HTTP_200_OK
        
@customer.get("/<int:id>")
@jwt_required()
def get_Customer(id_customer):
    customer = Customer.query.filter_by(id_customer=id_customer).first()
    if not customer:
        return jsonify({
            "message": "Item not found."
        })
    return jsonify({
        "name": customer.name,
        "email": customer.email,
        "phone_num": customer.phone_num
    }), HTTP_200_OK

@customer.put("/<int:id>")
@customer.patch("/<int:id>")
@jwt_required()
def edit_customer(id):
    customer = Customer.query.filter_by(id_customer=id).first()

    if not customer:
        return jsonify({
            "message": "Item not found."
        })
    
    name = request.get_json().get("name", "")
    email = request.get_json().get("email", "")
    phone_num = request.get_json().get("phone_num", "")
    if not validators.email(email):
        return jsonify({
            "error": "Email is invalid."
        }), HTTP_400_BAD_REQUEST

    customer.name = name
    customer.email = email
    customer.phone_num = phone_num

    db.session.commit()

    return jsonify({
        "id_customer": customer.id_customer,
        "name": customer.name
    }), HTTP_201_CREATED

@customer.delete("/<int:id>")
@jwt_required()
def delete_customer(id):
    customer = Customer.query.filter_by(id_customer=id).first()
    if not Customer:
        return jsonify({
            "message": "Item not found."
        })
    db.session.delete(customer)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
