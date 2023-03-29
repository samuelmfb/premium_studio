from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db
#from src.models.user import User

class UserRole(db.Model):
    id_user_role = db.Column(db.Integer, unique = True, primary_key = True)
    user_role = db.Column(db.String(80), unique = True, nullable = False)

    def __repr__(self) -> str:
        return f'UserRole>>>{self.user_role}'