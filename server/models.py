from flask.ext.sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Carrier(db.Model):
    __tablename__ = 'cellCarrierInfo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    carrierName = db.Column(db.Text)
    domain = db.Column(db.Text)

    def __init__(self, name, domain):
        self.carrierName = name
        self.domain = domain

class User(db.Model):
    __tablename__ = 'users'
    uid_number = db.Column(db.Integer, primary_key = True)
    phone_number = db.Column(db.BigInteger)
    carrier = db.Column(db.Integer, db.ForeignKey('cellCarrierInfo.id', onupdate="cascade", ondelete="cascade"))
    admin = db.Column(db.Boolean)

    def __init__(self, uid_number, phone_number = None, carrier = None, admin = False):
        self.uid_number = uid_number
        self.phone_number = phone_number
        self.carrier = carrier
        self.admin = admin

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    api_key = db.Column(db.Text)
    service_name = db.Column(db.Text)
    owner = db.Column(db.Integer)
    subscription_service = db.Column(db.Boolean)
    active = db.Column(db.Boolean)

    def __init__(self, api_key, name, owner, subs, active):
        self.api_key = api_key
        self.service_name = name
        self.owner = owner
        self.subscription_service = subs
        self.active = active

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user = db.Column(db.Integer, db.ForeignKey('users.uid_number', onupdate='cascade', ondelete='cascade'))
    service = db.Column(db.Integer, db.ForeignKey('services.id', onupdate='cascade', ondelete='cascade'))
    state = db.Column(db.Integer)

    def __init__(self, user, service, state):
        self.user = user
        self.service = service
        self.state = state

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.DateTime, default = datetime.datetime.now())
    service = db.Column(db.Integer, db.ForeignKey('services.id', onupdate='cascade', ondelete='cascade'))
    user = db.Column(db.Integer, db.ForeignKey('users.uid_number', onupdate='cascade', ondelete='cascade'))
    email = db.Column(db.Text)

    def __init__(self, service, user, email):
        self.service = service
        self.user = user
        self.email = email
