from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# Setting Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warungskuy.db'
app.config['SECRET_KEY'] = '4d3740e2e12c5a57b89bba63'
db = SQLAlchemy(app)

# Setting hashing for password
bcrypt = Bcrypt(app)

# Login manager
login_manager = LoginManager(app)
login_manager.login_view = "login_page" # the name of the login route function
login_manager.login_message_category = "info"

# Import routes
from warungskuy import routes
