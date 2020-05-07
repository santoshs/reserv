from flask import flash
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms.validators import DataRequired, Email

from .models import User, Machine

class LoginForm(FlaskForm):
    username = TextField(u'Username', validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.optional()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if not user or not user.check_password(self.password.data):
            flash('Invalid username or password', 'warning')
            return False

        return True


class MachineAddForm(FlaskForm):
    hostname = TextField(u'Hostname', validators=[validators.required()])
    address = TextField(u'IP Address', validators=[validators.IPAddress(),
                                                   validators.Optional()])
    alias = TextField(u'Alias')
    sys_user = TextField(u'Login user')
    sys_passwd = TextField(u'Login password')
    console_type = SelectField(u'Console Type', choices=Machine.CONSOLE_TYPES,
                               validators=[validators.Optional()])
    console_sys = TextField(u'Console system')
    console_user = TextField(u'Cosole user')
    console_passwd = TextField(u'Console password')
    console_ipmi_user = TextField(u'IPMI user')
    console_ipmi_passwd = TextField(u'IPMI password')
    machine = TextField(u'Machine name')
    pname = TextField(u'Logical partition name')
    tport = TextField(u'Telnet Port')
    line = TextField(u'Line')


class UserForm(FlaskForm):
    email = EmailField('Email Address', validators=[Email()])
    password = PasswordField('Password', [
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
