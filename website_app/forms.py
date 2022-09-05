from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField , HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from website_app.models import User, Invitation
from flask_wtf import RecaptchaField


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),Length(min=8, max=32), EqualTo('password')])
    invite_code = StringField('invite_code',
                        validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    recaptcha = RecaptchaField()

    def validate_invite_code(self, invite_code):
        invite_code = Invitation.query.filter_by(code=invite_code.data).first()
        if invite_code and not invite_code.is_used:
            return True
        raise ValidationError("invalid invite code. please contact us on telegram to get a valid one.")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            return True
        raise ValidationError("Email is already registred ")


class NewInvitationForm(FlaskForm):
    submit = SubmitField('new invitation')

class NewPasswordForm(FlaskForm):
    password = PasswordField('new Password', validators=[DataRequired(),Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm nre Password',
                                     validators=[DataRequired(),Length(min=8, max=32), EqualTo('password')])
    submit = SubmitField('reset')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    remember = BooleanField('Remember Me')
    recaptcha = RecaptchaField()
    submit = SubmitField('Login')




class ResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    recaptcha = RecaptchaField()

    submit = SubmitField('reset')


class AddLicenceForm(FlaskForm):
    number = IntegerField('number', [DataRequired()])
    user_id = StringField('User',
                        validators=[DataRequired()])


class AddTelegramForm(FlaskForm):
    telegram_username = StringField('telegram username',
                        validators=[DataRequired()])
    submit = SubmitField('change')


class BindIpForm(FlaskForm):
    ip_address = StringField('ip address',
                        validators=[DataRequired()])
    licence = StringField('the_licence',
                             validators=[DataRequired()])
    submit = SubmitField('change')
