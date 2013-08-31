from server import app
from models import db, Carrier, User
import sys

def create(app):
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

def delete(app):
    with app.app_context():
        db.drop_all()
        print 'tables dropped'

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print 'python setup.py [create|drop]'
    elif sys.argv[1] == 'create':
        create(app)
    elif sys.argv[1] == 'drop':
        delete(app)
    elif sys.argv[1] == 'redo':
        delete(app)
        create(app)
    else:
        print 'python setup.py [create|drop]'

