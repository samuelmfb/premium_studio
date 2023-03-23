import json
from flask import Flask, jsonify
import os
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.controllers.auth import auth
from src.controllers.customer import customer
from src.controllers.producer import producer
from src.controllers.project import project
from src.controllers.task import task
from src.controllers.user_role import user_role
from src.controllers.user import user
from src.database import db
from flask_jwt_extended import JWTManager
# from flasgger import Swagger, swag_from
# from src.config.swagger import template, swagger_config
from src.views import views
app = Flask(__name__,
    instance_relative_config = True)

app.config.from_mapping(
    SECRET_KEY = os.environ.get("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI"),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY"),
    SWAGGER = {
        "title": "Premium Studio",
        "uiversion": 3
    }
)

for view in views:
    app.register_blueprint(view)

db.app = app
db.init_app(app)

JWTManager(app)
# Swagger(app, config=swagger_config, template=template)
app.register_blueprint(auth)
app.register_blueprint(customer)
app.register_blueprint(producer)
app.register_blueprint(project)
app.register_blueprint(task)
app.register_blueprint(user_role)
app.register_blueprint(user)

@app.errorhandler(HTTP_404_NOT_FOUND)
def handle_404(e):
    return jsonify({"error": "Not found."}), HTTP_404_NOT_FOUND

@app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def handle_500(e):
    return jsonify({"error": "Server error."}), HTTP_500_INTERNAL_SERVER_ERROR

#Run
if __name__ == '__main__':
    app.run(debug = True)