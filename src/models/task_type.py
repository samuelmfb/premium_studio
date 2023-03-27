from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db
#from src.models.user import User

class TaskType(db.Model):
    id_task_type = db.Column(db.Integer, unique = True, primary_key = True)
    task_type = db.Column(db.String(80), unique = True, nullable = False)

    def __repr__(self) -> str:
        return f'UserRole>>>{self.role_name}'