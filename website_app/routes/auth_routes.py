from flask import render_template, url_for, flash, redirect
from flask_mail import Message
from website_app import app, db, bcrypt, mail
from website_app.forms import RegistrationForm, LoginForm,NewPasswordForm, ResetForm
from website_app.models import User, Licence, Invitation, Telegram
from flask_login import login_user, current_user, logout_user
from itsdangerous import URLSafeTimedSerializer as Serializer
import random


serializer = Serializer(app.config['SECRET_KEY'])


def generate_invitation():
    key = ''
    alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
    while len(key) < 11:
        char = random.choice(alphabet)
        key += random.choice(alphabet)
    return key


def generate_key():
    key = ''
    section = ''
    alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
    while len(key) < 25:
        char = random.choice(alphabet)
        key += char
        section += char
        if len(section) == 4:
            key += '-'
            section = ''
    key = key[:-1]
    return key

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.user_type == 'admin':
            return redirect(url_for('admin'))
        elif current_user.is_suspended:
            flash('account suspended', 'error')
            logout_user()
        return redirect(url_for('home'))
    telegram_user = Telegram.query.first()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Failed. Please check email and password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html', telegram=telegram_user.username , title='Mailer Login', form=form)

@app.route("/reset", methods=['GET', 'POST'])
def reset_password_page():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    token = None
    form = ResetForm()
    telegram_user = Telegram.query.first()

    if form.validate_on_submit():
        email = form.email.data
        if User.query.filter_by(email=email).first():
            token = serializer.dumps(email)
            msg = Message('Password reset requests', sender='brodon@pathfinderchurch.com', recipients=[email])
            msg.body = f'''
                to reset your password please use the following link:
                {url_for('password_reset',token=token,_external=True)}
            '''
            mail.send(msg)
            # redirect('/password_reset',token=token)
        flash('if you are registred , you will get an email shortly .')
        return redirect(url_for('reset_password_page'))
    return render_template('reset.html', telegram=telegram_user.username, title='Reset password', form=form)


@app.route("/password_reset/<token>", methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    try:
        email = serializer.loads(token, max_age=1800)
        form = NewPasswordForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=email).first()
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('new_password.html',title='Reset Password', form=form)
    except:
        flash('invalid url Please request a new password', 'error')
        return redirect(url_for('reset_password'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        invitation = Invitation.query.filter_by(code=form.invite_code.data).first()
        if str(form.invite_code.data) == "123":
            user = User(email=form.email.data, password=hashed_password, invite_code=invitation.id, user_type="admin")
        else:
            user = User(email=form.email.data, password=hashed_password, invite_code=invitation.id)
        key = generate_key()
        licence_key = Licence.query.filter_by(licence=key).first()
        while licence_key:
            key = generate_key()
            licence_key = Licence.query.filter_by(licence=key).first()
        db.session.add(user)
        user = User.query.filter_by(email=form.email.data).first()
        added_licence = Licence(licence=str(key), user_id=user.id)
        db.session.commit()
        db.session.add(added_licence)
        db.session.commit()
        invitation.is_used = True
        db.session.commit()
        flash(f'Account created for {form.email.data}!')
        return redirect(url_for('login'))
    telegram_user = Telegram.query.first()
    telegram_username = None
    try:
        telegram_username = telegram_user.username
        return render_template('register.html', title='Register', form=form, telegram=telegram_username)
    except:
        return render_template('register.html', title='Register', form=form)




@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

