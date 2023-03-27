from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db
from src.models.project import Project
from src.models.task_type import TaskType

class Task(db.Model):
    id_task = db.Column(db.Integer, primary_key = True)
    id_task_type = db.Column(db.Integer, db.ForeignKey(TaskType.id_task_type), nullable = True)
    id_project = db.Column(db.Integer, db.ForeignKey(Project.id_project))
    project = db.relationship('Project', backref='project_task', foreign_keys=[id_project])
    title = db.Column(db.String(250), nullable = False)
    description = db.Column(db.String(250), nullable = False)
    deadline = db.Column(db.Date, nullable = False)
    started = db.Column(db.DateTime, default=datetime.now())
    finished = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return f'{self.description}'