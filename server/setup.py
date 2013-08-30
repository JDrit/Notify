from server import app
from models import db, Carrier

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print 'tables created'

        db.session.add(Carrier('at&t', 'txt.att.net'))
        db.session.add(Carrier('Verizon', 'vtext.com'))
        db.session.add(Carrier('T-Mobile', 'tmomail.net'))
        db.session.add(Carrier('Sprint', 'messaging.sprintpcs.com'))
        db.session.add(Carrier('US Cellular', 'email.uscc.net'))
        db.session.add(Carrier('Metro PCS', 'mymetropcs.com'))
        print 'default carriers added'

        db.session.commit()

