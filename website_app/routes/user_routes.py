from flask import render_template, url_for, flash, redirect
from website_app import app, db
from website_app.forms import BindIpForm
from website_app.models import User, Licence
from flask_login import current_user, logout_user

import ipaddress

@app.route("/", methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated or current_user.user_type == 'admin':
        return redirect(url_for('login'))
    elif current_user.is_suspended:
        flash('account suspended', 'danger')
        logout_user()
        return redirect(url_for('login'))
    form = BindIpForm()
    if form.validate_on_submit():
        try:
            if ipaddress.ip_address(str(form.ip_address.data)):
                licence = Licence.query.get(form.licence.data)
                licence.ip_address = form.ip_address.data
                db.session.add(licence)
                db.session.commit()
                flash("ipaddress binded successfully", "danger")
                return redirect(url_for('home'))
        except:
            flash("invalid ip address", "danger")
            return redirect(url_for('home'))

    user = User.query.get(current_user.id)
    form.ip_address.data = ''
    return render_template('home.html', title='user dashboard',licences=user.licence, form=form)
