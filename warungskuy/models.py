import datetime
from warungskuy import db, login_manager
from warungskuy import bcrypt
from sqlalchemy.sql import func
from flask_login import UserMixin
from flask import session
from sqlalchemy_utils import UUIDType
import uuid


@login_manager.user_loader
def load_user(user_id):
    lender = Lender.query.get(user_id)
    borrower = Borrower.query.get(user_id)

    if(lender):
        return lender
    else:
        return borrower


class User(db.Model):
    __abstract__ = True
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    phone_number = db.Column(db.String(length=15), nullable=False)
    fullname = db.Column(db.String(length=100), nullable=False)
    birth_place = db.Column(db.String(length=50), nullable=False)
    birth_date = db.Column(db.Date(), nullable=False)
    gender = db.Column(db.String(length=1), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Lender(User, UserMixin):
    id = db.Column(db.String(length=32), primary_key=True,
                   default=str(uuid.uuid4()))
    nik = db.Column(db.String(length=16), unique=True)
    address = db.Column(db.String(length=255))
    bank = db.Column(db.String(length=5))
    account_number = db.Column(db.String(length=50))
    account_name = db.Column(db.String(length=100))

    # Relationship
    lendingTr = db.relationship('LendingTransaction', backref='lender', lazy=True)


class Borrower(User, UserMixin):
    id = db.Column(db.String(length=32), primary_key=True, default=str(uuid.uuid4()))

    # Relation to Loan
    loan = db.relationship('Loan', backref='loan_requested', lazy=True)


class Loan(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(length=32), primary_key=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(length=75))
    tenor = db.Column(db.Integer)
    start_loan = db.Column(db.Date)
    end_loan = db.Column(db.Date)

    nominal = db.Column(db.Integer)
    interest = db.Column(db.Numeric(10, 2))

    loan_reason = db.Column(db.String(length=500))
    business_desc = db.Column(db.String(length=500))
    location = db.Column(db.String(length=100))
    start_year = db.Column(db.Integer)
    business_address = db.Column(db.String(length=150))
    gross_income = db.Column(db.Integer)
    net_income = db.Column(db.Integer)
    modal = db.Column(db.Integer)
    # Fund Collected
    # fund_collected = db.Column(db.Integer) # Aggregate value, cek apakah SQLAlchemy ada function aggregate
    # Timestamp
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # Foreign Key
    borrower = db.Column(db.String(length=32), db.ForeignKey('borrower.id'))

    # Relationship
    lendingTr = db.relationship('LendingTransaction', backref='lended_loan', lazy=True)

    def __repr__(self):
        return f"<Loan {self.title}>"


class LendingTransaction(db.Model):
    trans_id = db.Column(db.String(length=32), primary_key=True, default=str(uuid.uuid4()))
    lender_id = db.Column(db.String(length=32), db.ForeignKey('lender.id'), nullable=False)
    loan_id = db.Column(db.String(length=32), db.ForeignKey('loan.id'), nullable=False)
    lending_amount = db.Column(db.Integer(), nullable=False)
