from datetime import timedelta, date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from sqlalchemy.orm import relation
from sqlalchemy import (create_engine, Column, Integer, DateTime, String,
                        ForeignKey, Table)
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

class Machine(db.Model):
    __tablename__ = 'machine'

    CONSOLE_TYPES = [
        (u'', u'Select Console Type'),
        (u'ipmi', u'Intelligent Platform Management Interface'),
        (u'hmc', u'Hardware Management Console'),
        (u'amc', u'Advaned Management Console'),
    ]

    id = db.Column(db.Integer(), primary_key=True)
    hostname = db.Column(db.String(), unique=True)
    address = db.Column(db.String())
    alias = db.Column(db.String(), unique=True)
    sys_user = db.Column(db.String())
    sys_passwd = db.Column(db.String())
    console_type = db.Column(ChoiceType(CONSOLE_TYPES))
    console_sys = db.Column(db.String())
    console_user = db.Column(db.String())
    console_passwd = db.Column(db.String())
    console_ipmi_user = db.Column(db.String())
    console_ipmi_passwd = db.Column(db.String())
    machine = db.Column(db.String())
    pname = db.Column(db.String())
    tport = db.Column(db.String())
    line = db.Column(db.String())

    def __init__(self, hostname, address, alias=None):
        self.hostname = hostname
        self.address = address
        self.alias = alias


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    last_login = db.Column(db.DateTime())
    email = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, ForeignKey('machine.id'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    end_date = db.Column(db.DateTime)
    message = db.Column(db.String(), nullable=True)

    user = db.relationship(User, backref="reservations")
    machine = db.relationship(Machine, backref="reservation")

    def __init__(self, machine_id, user_id, duration_days, log):
        self.id = machine_id;
        self.user_id = user_id
        self.message = log
        self.update_time(duration_days)

    def update_time(self, duration_days):
        if duration_days and duration_days != '':
            self.end_date = date.today() + timedelta(days=int(duration_days))


class ReservationLog(db.Model):
    __tablename__ = 'reservation_log'

    id = db.Column(db.Integer(), primary_key=True)
    machine_id = db.Column(db.Integer(), db.ForeignKey('machine.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    start = db.Column(db.DateTime(), default=func.now())
    end = db.Column(db.DateTime())

    user = db.relationship(User, innerjoin=True, lazy="joined")
    machine = db.relationship(Machine, innerjoin=True, lazy="joined")

    def __init__(self, machine_id, user_id):
        self.machine_id = machine_id
        self.user_id = user_id

    def __repr__(self):
        return '<ReservationLog %d %s %s' % (self.id, self.user.username, self.machine.alias)
