from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.database import db
from src.models.expense_type import ExpenseType

class Expense(db.Model):
    id_expense = db.Column(db.Integer, primary_key = True)
    id_expense_type = db.Column(db.Integer, db.ForeignKey(ExpenseType.id_user_role), nullable = True)
    expense_type = db.relationship('ExpenseType', backref='expense_expense_type', foreign_keys=[id_expense_type])
    full_value = db.Column(db.Numeric(20,2), nullable = False)
    due_date = db.Column(db.Date)
    payment = db.Column(db.Date)

    def __repr__(self) -> str:
        return f'Due date>>>{self.due_date}'
