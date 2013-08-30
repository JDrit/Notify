"""
    Author: Kevin J Dolan
    Project: Notify
    File Name: notifyServer.py
    Purpose: Get information from the webserver via json and then send out emails.
    Date: 12/29/12

"""

from sys import argv
import json
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import ConfigParser
import os

#Email Credentials
config = ConfigParser.ConfigParser()
config.read('config')
gmail_user = config.get('email', 'user')
gmail_pwd = config.get('email', 'password')

def mail(to, subject, text):
    """
    Sends the email out to the given person
    to:      the email address to send to
    subject: the subject of the message
    text:    the actual body of the message
    """
    msg = MIMEText(text)
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

