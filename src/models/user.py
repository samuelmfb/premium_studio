from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key = True)
    user_role = db.Column(db.Integer, nullable = True)
    user_name = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.Text(), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    user_user_role = db.relationship('UserRole', backref = 'user_role')

    def __repr__(self) -> str:
        return f'User>>>{self.user_name}'
