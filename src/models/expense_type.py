from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db
from src.models.user_role import UserRole

class ExpenseType(db.Model):
    id_expense_type = db.Column(db.Integer, unique = True, primary_key = True)
    expense_type = db.Column(db.String(80), unique = True, nullable = False)

    def __repr__(self) -> str:
        return f'ExpenseType>>>{self.expense_type}'