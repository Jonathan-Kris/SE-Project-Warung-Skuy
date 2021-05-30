import datetime
from warungskuy import db, login_manager
from warungskuy import bcrypt
from sqlalchemy.sql import func
from flask_login import UserMixin
from flask import session

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

@login_manager.user_loader
def load_user(user_id):
  if session['account_type'] == 'Investor':
      return Investor.query.get(int(user_id))
  elif session['account_type'] == 'Peminjam':
      return Peminjam.query.get(int(user_id))
  else:
      return None


class User(db.Model):
    __abstract__ = True
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    phone_number = db.Column(db.String(length=15), nullable=False)
    fullname = db.Column(db.String(length=100), nullable=False)
    birth_place = db.Column(db.String(length=50))
    birth_date = db.Column(db.Date())
    gender = db.Column(db.String(length=1), nullable=False)
    
    time_created = db.Column(db.DateTime(), server_default=func.now())

    @property
    def password(self):
        return self.password

    @password.setter 
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Investor(User, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(length=16), unique=True)
    address = db.Column(db.String(length=255))
    bank = db.Column(db.String(length=50))
    account_number = db.Column(db.String(length=50))
    account_name = db.Column(db.String(length=100))

class Peminjam(User, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
