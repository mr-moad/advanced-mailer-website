from flask import url_for, redirect, request
from website_app import app, db
from website_app.models import Licence, Invitation
from flask import jsonify


@app.route("/verify/<lis>/<ip>", methods=['GET', 'POST'])
def verify_liscence(lis, ip):
    lis = Licence.query.filter_by(licence=str(lis)).first()
    print("===============================")
    # print(lis.licence_user.is_suspended)
    print(lis)
    print(ip)
    # print(request.remote_addr)
    print("===============================")
    if lis and not lis.licence_user.is_suspended and str(ip) == str(lis.ip_address):
        return jsonify({
            'status': 'ok'
        })
    else:
        return jsonify({
            'status': 'nu'
        })


@app.route("/generate")
def generate_invitation():
    invitation = Invitation(code="123")
    db.session.add(invitation)
    db.session.commit()
    return redirect(url_for('login'))


