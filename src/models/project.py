from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db
from src.models.customer import Customer
from src.models.producer import Producer

class Project(db.Model):
    id_project = db.Column(db.Integer, primary_key = True)
    id_customer = db.Column(db.Integer, db.ForeignKey(Customer.id_customer))
    customer = db.relationship('Customer', backref='project_customer', foreign_keys=[id_customer])
    name = db.Column(db.String(250), nullable = False)
    description = db.Column(db.String(250), nullable = False)
    full_value = db.Column(db.Numeric(20,2), nullable = False)
    id_producer = db.Column(db.Integer, db.ForeignKey(Producer.id_producer))
    producer = db.relationship('Producer', backref='project_producer', foreign_keys=[id_producer])

    def __repr__(self) -> str:
        return f'{self.description}'