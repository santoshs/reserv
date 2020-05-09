from flask import flash
from flask_wtf import FlaskForm
from wtforms import (
    TextField, PasswordField, SubmitField, SelectField, BooleanField)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    DataRequired, Email, required, Optional, IPAddress, EqualTo)

from .models import User, Machine

class LoginForm(FlaskForm):
    username = TextField(u'Username', validators=[required()])
    password = PasswordField(u'Password', validators=[Optional()])

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
    hostname = TextField(u'Hostname', validators=[required()])
    address = TextField(u'IP Address', validators=[IPAddress(), Optional()])
    alias = TextField(u'Alias')
    sys_user = TextField(u'Login user')
    sys_passwd = TextField(u'Login password')
    console_type = SelectField(u'Console Type', choices=Machine.CONSOLE_TYPES,
                               validators=[Optional()])
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
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class ReservationForm(FlaskForm):
    DURATION = [
        (u'', 'Select Days'),
        (1, '1 Day'),
        (2, '2 Days'),
        (3, '3 Days'),
        (5, '5 Days'),
        (8, '8 Days'),
        (13, '2 Weeks'),
        (21, '3 Weeks'),
        (24, '1 Month'),
        (55, '2 Months'),
        (89, '3 Months'),
        (144, '4 Months'),
        (233, '8 Months'),
        (377, '1 Year')]

    message = TextField(u'Message', validators=[Optional()])
    duration = SelectField(u'Duration', choices=DURATION,
                           validators=[Optional()])
    forever = BooleanField(u'Reserve Indefinitely')

    def validate(self):
        if self.duration.data == '' and self.forever.data == False:
            flash('Need to specify duration or reserve forever', 'warning')
            return False

        return True
