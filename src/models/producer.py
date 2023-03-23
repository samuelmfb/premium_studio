from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db

class Producer(db.Model):
    id_producer = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    area = db.Column(db.String(120), nullable = False)

    def __repr__(self) -> str:
        return f'Producer>>>{self.name} - {self.area}'