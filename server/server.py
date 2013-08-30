from flask import Flask, request
import ConfigParser
from mailer import mail
from models import db

config = ConfigParser.ConfigParser()
config.read('config')
uri = config.get('sql', 'uri')
port = config.getint('main', 'port')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db.init_app(app)


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
        mail(phone_email, "CSH Notification - " + service.service_name, notification)
    # sends the email to the csh account
    if subscription.state == 0 or subscription.state == 2:
        csh_email = get_username(user.uid_number) + "@csh.rit.edu"
        mail(csh_email, "CSH Notification - " + service.service_name, notification)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = port)
