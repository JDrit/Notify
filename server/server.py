"""
This is the new server that will be used to send the emails to the users.
It uses Flask and sqlalchemy to send the emails without buffering to the
database.
"""

from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
import ConfigParser
import datetime
from sqlalchemy.dialects.mysql import BIT

config = ConfigParser.ConfigParser()
config.read('config')
uri = config.get('sql', 'uri')
port = config.getint('main', 'port')

app = Flask("notify")
app.config['sql_uri'] = port
db = SQLAlchemy(app)

class carrier(db.Model):
    __tablename__ = 'cellCarrierInfo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    carrierName = db.Column(db.Text)
    domain = db.Column(db.Text)

    def __init__(self, name, domain):
        self.carrierName = name
        self.domain = domain

class user(db.Model):
    __tablename__ = 'users'
    uid_number = db.Column(db.Integer, primary_key = True)
    phone_number = db.Column(db.BigInteger)
    carrier = db.Column(db.Integer, db.ForeignKey('cellCarrierInfo.id', onupdate="cascade", ondelete="cascade"))
    admin = db.Column(db.Boolean)

    def __init__(self, uid_number, phone_number, carrier, admin):
        self.uid_number = uid_number
        self.phone_number = phone_number
        self.carrier = carrier
        self.admin = admin

class service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    api_key = db.Column(db.Text)
    service_name = db.Column(db.Text)
    owner = db.Column(db.Integer)
    subscription_service = db.Column(BIT)
    active = db.Column(BIT)

    def __init__(self, api_key, name, owner, subs, active):
        self.api_key = api_key
        self.service_name = name
        self.owner = owner
        self.subscription_service = subs
        self.active = active

class subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user = db.Column(db.Integer, db.ForeignKey('users.uid_number', onupdate='cascade', ondelete='cascade'))
    service = db.Column(db.Integer, db.ForeignKey('services.id', onupdate='cascade', ondelete='cascade'))
    state = db.Column(db.Integer)

    def __init__(self, user, service, state):
        self.user = user
        self.service = service
        self.state = state

class log(db.Model):
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


@app.route("/notify", methods=['GET', 'POST'])
def notify():
    username = request.args.get("username", "")
    if username == "":
        return "no username"
    notification = request.args.get("notification", "")
    if notification == "":
        return "no notification"
    api_key = request.args.get("apiKey", "")
    if api_key == "":
        return "no api key"



    return "hello"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = port)
