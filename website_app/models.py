from datetime import datetime
from website_app import db,  login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_type = db.Column(db.String(120), nullable=False, default="regular")
    password = db.Column(db.String(60), nullable=False)
    invite_code = db.Column(db.Integer, db.ForeignKey('invitation.id'))
    licence = db.relationship('Licence', backref='licence_user', lazy=True)
    is_suspended = db.Column(db.Boolean, default=False, nullable=False)


    def __repr__(self):
        return f"User('{self.email}')"


class Licence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    licence = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(20))
    is_restricted = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Licence('{self.licence}', '{self.date_created}')"


class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    invited_user = db.relationship('User', backref='invited', lazy=True)

    def __repr__(self):
        return f"Licence('{self.code}')"


class Telegram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Telegram('{self.username}')"
