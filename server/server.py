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
    subscription_service = db.Column(BIT)
    active = db.Column(BIT)

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

def check_uid_number(uid_number):
    return True

def get_username(uid_number):
    return "jd"

@app.route("/notify", methods=['GET', 'POST'])
def notify():
    phone_email = csh_email = None
    uid_number = request.args.get("username", "")
    if uid_number == "":
        return "no uid number"
    notification = request.args.get("notification", "")
    if notification == "":
        return "no notification"
    api_key = request.args.get("apiKey", "")
    if api_key == "":
        return "no api key"

    service = Service.query().filter_by(api_key = api_key).first()
    if not service:
        return "invalid API key"
    user = Service.query().filter_by(uid_number = uid_number).first()
    if not user: # make a user entry for the new user
        if check_uid_number(uid_number):
            db.session.add(User(uid_number))
        else:
            return "invalid uid number"
    subscription = Subscription.query().filter(db.and_(Subscription.user == user.uid_number,
        Subscription.service == service.id)).first()
    if not subscription:
        return "no subscription"

    # sends the text message
    if subscription.state == 1 or subscription.state == 2:
        carrier = Carrier.query().filter_by(id = user.carrier).first()
        phone_email = user.phone_number + "@" + carrier.domain

    # sends the email to the csh account
    if subscription.state == 0 or subscription.state == 2:
        csh_email = get_username(user.uid_number) + "@csh.rit.edu"











    return "sent"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = port)
