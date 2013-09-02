from flask import Flask, request
import ConfigParser
from mailer import mail
from models import *
import ldap

config = ConfigParser.ConfigParser()
config.read('config')
uri = config.get('sql', 'uri')
port = config.getint('main', 'port')
ldap_host = config.get('ldap', 'host')
base_dn = config.get('ldap', 'base_dn')
password = config.get('ldap', 'password')
search_dn = config.get('ldap', 'search_dn')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.debug = True
db.init_app(app)

class PyLDAP():

    def __init__(self, host, base_dn, password):
            self.host = host
            self.base_dn = base_dn
            self.password = password

            try:
                self.conn = ldap.initialize(self.host)
                self.conn.simple_bind_s(self.base_dn, self.password)
            except ldap.LDAPError, e:
                print e

    def search(self, search_dn, search_filter):
        try:
            ldap_result_id = self.conn.search(search_dn,
                    ldap.SCOPE_SUBTREE, search_filter, None)
            result_type, result_data = self.conn.result(
                    ldap_result_id, 0)
            if result_type == ldap.RES_SEARCH_ENTRY:
                return result_data
        except ldap.LDAPError, e:
            print e

    def close(self):
        self.conn.unbind()

def check_uid_number(uid_number):
    return True

def get_username(uid_number):
    global ldap_host, base_dn, password, search_dn
    conn = PyLDAP(ldap_host, base_dn, password)
    result = conn.search(search_dn, "uidNumber=" + str(uid_number))
    conn.close()
    return result[0][1]['uid'][0]


@app.route("/notify", methods=['GET', 'POST'])
def notify():
    phone_email = csh_email = username = None

    # checks for valid input in the GET request
    uid_number = request.args.get("uid_number", "")
    if uid_number == "":
        username = request.args.get("username", "")
        if username == "":
            return "no uid number or username given"
    notification = request.args.get("notification", "")
    if notification == "":
        return "no notification"
    api_key = request.args.get("apiKey", "")
    if api_key == "":
        return "no api key"

    service = Service.query.filter_by(api_key = api_key).first()
    if not service:
        return "invalid API key"
    user = User.query.filter_by(uid_number = uid_number).first()
    if user == None: # make a user entry for the new user
        if check_uid_number(uid_number):
            user = User(uid_number)
            db.session.add(user)
        else:
            return "invalid uid number"
    subscription = Subscription.query.filter(
            db.and_(Subscription.uid_number == user.uid_number,
                Subscription.service_id == service.id)).first()
    if not subscription:
        return "user not subscribed to service"

    # sends the text message
    if subscription.state == 1 or subscription.state == 2:
        carrier = Carrier.query.filter_by(id = user.carrier).first()
        print user, carrier
        phone_email = str(user.phone_number) + "@" + carrier.domain
        mail(phone_email, "CSH Notification - " + service.service_name, notification)
        db.session.add(Log(service.id, user.uid_number, phone_email))
    # sends the email to the csh account
    if subscription.state == 0 or subscription.state == 2:
        if username != None:
            csh_email = username + "@csh.rit.edu"
        else:
            csh_email = get_username(user.uid_number) + "@csh.rit.edu"
        mail(csh_email, "CSH Notification - " + service.service_name, notification)
        db.session.add(Log(service.id, user.uid_number, csh_email))
    db.session.commit()
    return "good"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = port)
