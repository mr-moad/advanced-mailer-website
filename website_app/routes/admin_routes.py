from flask import render_template, url_for, flash, redirect, request
from website_app import app, db
from website_app.forms import AddLicenceForm, AddTelegramForm, NewInvitationForm
from website_app.models import User, Invitation, Telegram, Licence
from flask_login import current_user

import random


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


@app.route("/admin/delete/<user_email>", methods=['GET', 'POST'])
def admin_delete_user(user_email):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.user_type != 'admin':
        return redirect(url_for('home'))
    user = User.query.filter_by(email=user_email).first()
    licences = Licence.query.filter_by(user_id=user.id).all()
    for licence in licences:
        db.session.delete(licence)
        db.session.commit()
    user_to_delete = User.query.filter_by(email=user_email).first()
    invitation_id = user_to_delete.invite_code
    db.session.delete(user_to_delete)
    db.session.commit()
    invitation = Invitation.query.get(invitation_id)
    db.session.delete(invitation)
    db.session.commit()
    flash('user Deleted successfully', 'success')
    return redirect(url_for('admin'))


@app.route("/admin/upgrade/<user_email>", methods=['GET', 'POST'])
def admin_upgrade_user(user_email):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.user_type != 'admin':
        return redirect(url_for('home'))
    user_to_upgrade = User.query.filter_by(email=user_email).first()
    user_to_upgrade.user_type = 'admin'
    db.session.commit()
    flash('user Upgraded successfully', 'success')
    return redirect(url_for('admin'))

@app.route("/admin/downgrade/<user_email>", methods=['GET', 'POST'])
def admin_downgrade_user(user_email):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.user_type != 'admin':
        return redirect(url_for('home'))
    user_to_downgrade = User.query.filter_by(email=user_email).first()
    if str(user_to_downgrade.invited.code) != '123':
        user_to_downgrade.user_type = 'regular'
        db.session.commit()
    flash('user Downgraded successfully', 'success')
    return redirect(url_for('admin'))


@app.route("/admin/reactivate/<user_email>", methods=['GET', 'POST'])
def admin_reactivate_user(user_email):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.user_type != 'admin':
        return redirect(url_for('home'))
    user_to_reactivate = User.query.filter_by(email=user_email).first()
    user_to_reactivate.is_suspended = False
    db.session.commit()
    flash('user reactivated successfully', 'success')
    return redirect(url_for('admin'))


@app.route("/admin/add_licence/<user_email>/<int:number_of_licences>", methods=['GET', 'POST'])
def add_licence(user_email, number_of_licences):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.user_type != 'admin':
        return redirect(url_for('home'))
    user = User.query.filter_by(email=user_email).first()
    for i in range(int(number_of_licences)):
        key = generate_key()
        licence_key = Licence.query.filter_by(licence=key).first()
        while licence_key:
            key = generate_key()
            licence_key = Licence.query.filter_by(licence=key).first()
        added_licence = Licence(licence=str(key), user_id=user.id)
        db.session.add(added_licence)
        db.session.commit()
    flash('licences added successfully', 'success')
    return redirect(url_for('admin'))


@app.route("/admin/suspend/<user_email>", methods=['GET', 'POST'])
def admin_suspend_user(user_email):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.user_type != 'admin':
        return redirect(url_for('home'))
    user_to_suspend = User.query.filter_by(email=user_email).first()
    user_to_suspend.is_suspended = True
    db.session.commit()
    flash('user Suspended successfully', 'success')
    return redirect(url_for('admin'))


@app.route("/admin/telegram", methods=['GET', 'POST'])
def admin_telegram():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.user_type != 'admin':
        return redirect(url_for('home'))
    form = AddTelegramForm()
    if form.validate_on_submit():
        telegram_username = Telegram.query.all()
        if telegram_username:
            telegram_username[0].username = form.telegram_username.data
            db.session.commit()
        else:
            telegram = Telegram(username=form.telegram_username.data)
            db.session.add(telegram)
            db.session.commit()
        flash('Telegram account changed successfully', 'success')
        return redirect(url_for('admin_telegram'))

    username = ''
    telegram_username = Telegram.query.all()
    if telegram_username:
        username = telegram_username[0].username
    return render_template('admin_telegram.html', title='admin Panel', form=form, telegram_username=username)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    invitation_code = None
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.user_type != 'admin':
        return redirect(url_for('home'))
    users = User.query.all()
    add_licence_form = AddLicenceForm()
    new_invitation_form = NewInvitationForm()
    if new_invitation_form.validate_on_submit():
        invitation_code = admin_codes_generator()
        flash(f"your invitation code is : {invitation_code}")
        return redirect(url_for('admin'))
    if add_licence_form.number.data:
        for i in range(int(add_licence_form.number.data)):
            key = generate_key()
            licence_key = Licence.query.filter_by(licence=key).first()
            while licence_key:
                key = generate_key()
                licence_key = Licence.query.filter_by(licence=key).first()
            added_licence = Licence(licence=str(key), user_id=int(add_licence_form.user_id.data))
            db.session.add(added_licence)
            db.session.commit()
    return render_template('admin.html', title='Admin Panel',new_invitation_form=new_invitation_form , add_licence_form=add_licence_form, users=users, invitation_code=invitation_code)


def admin_codes_generator():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.user_type != 'admin':
        return redirect(url_for('home'))
    key = ''
    alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
    while len(key) < 11:
        key += random.choice(alphabet)
    while Invitation.query.filter_by(code=key).first():
        key = ''
        alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
        while len(key) < 11:
            key += random.choice(alphabet)
    invite = Invitation(code=key)
    db.session.add(invite)
    db.session.commit()
    return key
