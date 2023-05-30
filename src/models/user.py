from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db
from src.models.user_role import UserRole

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key = True)
    id_user_role = db.Column(db.Integer, db.ForeignKey(UserRole.id_user_role), default = 5, nullable = True)
    user_role = db.relationship('UserRole', backref='user_user_role', foreign_keys=[id_user_role])
    user_name = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.Text(), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f'User>>>{self.user_name}'
