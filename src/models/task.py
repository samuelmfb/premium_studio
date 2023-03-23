from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db
from src.models.project import Project
from src.models.producer import Producer

class Task(db.Model):
    id_task = db.Column(db.Integer, primary_key = True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id_project))
    producer_id = db.Column(db.Integer, db.ForeignKey(Producer.id_producer))
    description = db.Column(db.String(250), nullable = False)
    deadline = db.Column(db.Date, nullable = False)
    started = db.Column(db.DateTime, default=datetime.now())
    finished = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return f'{self.description}'