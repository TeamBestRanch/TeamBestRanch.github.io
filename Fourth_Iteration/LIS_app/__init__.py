from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__, template_folder='templates')
# Database configurations
app.config['SECRET_KEY'] = 'faef9429c2bad94dfadbf9f24276e00f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# User Authentication
bcrypt = Bcrypt(app)

# Manages the login sessions
login_manager = LoginManager(app)

from LIS_app import routing
