from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db
from src.models.user import User

class UserRole(db.Model):
    id_role = db.Column(db.Integer, db.ForeignKey(User.user_role), primary_key = True)
    role_name = db.Column(db.String(80), unique = True, nullable = False)

    def __repr__(self) -> str:
        return f'User>>>{self.role_name}'