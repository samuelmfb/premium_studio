from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db

class Customer(db.Model):
    id_customer = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    phone_num = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    
    def __repr__(self) -> str:
        return f'Customer>>>{self.name}'
