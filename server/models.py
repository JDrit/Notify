from flask.ext.sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Carrier(db.Model):
    """
    This stores information about the various phone carrier providers.
        carrier_name: the string of the name
        domain: the domain used for emailing
        users: the users who use this carrier
    """
    __tablename__ = 'cellCarrierInfo'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = db.Column(db.Integer,  primary_key = True, autoincrement = True)
    carrier_name = db.Column(db.Text, nullable = False)
    domain = db.Column(db.Text, nullable = False)
    users = db.relationship('User', backref='carrier')

    def __init__(self, name, domain):
        self.carrier_name = name
        self.domain = domain

    def __str__(self):
        return str(self.id) + ") " + self.carrier_name + ", " + self.domain

class User(db.Model):
    """
    Holds notify users' information
        uid_number: the uid number of the user as the primary key
        phone_number: the number to use to text the user
        carrier_id: the id of the carrier being used
        subscriptions: the subscriptions that the user has
        admin: if the user is an admin for notify
    """
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    uid_number = db.Column(db.Integer, primary_key = True)
    phone_number = db.Column(db.BigInteger)
    carrier_id = db.Column(db.Integer,
            db.ForeignKey('cellCarrierInfo.id', onupdate='cascade',
                ondelete='cascade'))
    subscriptions = db.relationship('Subscription',
            backref='user')
    admin = db.Column(db.Boolean)

    def __init__(self, uid_number, phone_number = None, carrier = None, admin = False):
        self.uid_number = uid_number
        self.phone_number = phone_number
        self.carrier_id = carrier
        self.admin = admin

    def __str__(self):
        return str(self.uid_number) + ", " + str(self.phone_number) + ", " + str(self.carrier_id)

class Service(db.Model):
    """
    The services that can use notify
        api_key: the key used to authenticate the service to the server
        service_name: the name of the service
        owner: the uid number of the owner of the service
        active: if the service is currently allowed to send notifications
        subscriptions: the subscriptions being used for this service
        logs: the logs that are about these logs
    """
    __tablename__ = 'services'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    api_key = db.Column(db.Text, nullable = False)
    service_name = db.Column(db.Text, nullable = False)
    owner = db.Column(db.Integer, nullable = False)
    subscription_service = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    subscriptions = db.relationship('Subscription',
            backref='service')
    logs = db.relationship('Log', backref='service')

    def __init__(self, api_key, name, owner, subs, active):
        self.api_key = api_key
        self.service_name = name
        self.owner = owner
        self.subscription_service = subs
        self.active = active

class Subscription(db.Model):
    """
    The subscriptions that users have to various serivce. This is used
    to store the list of services that users are using
        uid_number: the uid number of the user
        service_id: the id of the service being subscribed to
        state: 0 = send email, 1 = send text, 2 = send both
    """
    __tablename__ = 'subscriptions'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    uid_number = db.Column(db.Integer, db.ForeignKey(User.uid_number,
        onupdate='cascade', ondelete='cascade'))
    service_id = db.Column(db.Integer, db.ForeignKey(Service.id,
        onupdate='cascade', ondelete='cascade'))
    state = db.Column(db.Integer)

    def __init__(self, user, service, state):
        self.user = user
        self.service = service
        self.state = state

class Log(db.Model):
    """
    Logs of all emails and text messages send
        date: the datetime of the message being sent
        service_id: the id of the service being used
        uid_number: the uid number of the user who was sent the message
        email: the address sent the message
    """
    __tablename__ = 'logs'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.DateTime, default = datetime.datetime.now())
    service_id = db.Column(db.Integer, db.ForeignKey(Service.id,
        onupdate='cascade'))
    uid_number = db.Column(db.Integer, nullable = False)
    email = db.Column(db.Text, nullable = False)

    def __init__(self, service, user, email):
        self.service_id = service
        self.user = user
        self.email = email
