from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db
from src.models.customer import Customer
from src.models.producer import Producer

class Project(db.Model):
    id_project = db.Column(db.Integer, primary_key = True)
    customer = db.Column(db.Integer, db.ForeignKey(Customer.id_customer))
    description = db.Column(db.String(250), nullable = False)
    full_value = db.Column(db.Numeric(20,2), nullable = False)
    producer = db.Column(db.Integer, db.ForeignKey(Producer.id_producer))

    project_tasks = db.relationship('Task', backref = 'project')
    
    def __repr__(self) -> str:
        return f'{self.description}'