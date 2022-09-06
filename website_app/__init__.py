from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'moad_machkouri@outlook.fr'
app.config['MAIL_PASSWORD'] = 'Startx-Startx1997'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeXZbkhAAAAAI_aZ2z_aZP8E0EKdDtGpRqwykrS'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeXZbkhAAAAAFCyLTpO-8oRBLan_hpthPShGKaK'


db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# last thing imported for circular import error
from website_app.routes import admin_routes
from website_app.routes import auth_routes
from website_app.routes import utility_routes
from website_app.routes import user_routes

if not os.path.isfile('./site.db'):
    db.create_all()


