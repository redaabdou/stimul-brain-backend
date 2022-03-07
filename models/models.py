from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import bcrypt
import base64
import json
from flask import Flask
from flask import current_app

from werkzeug.exceptions import InternalServerError
from threading import Thread
import bcrypt
from flask_mail import Mail, Message
import os
import os.path
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

db = SQLAlchemy()
app = Flask(__name__)
SendGrid_API_Client = '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'
TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/AC63731bfc55e3419b38c1035d7fddd876/Messages.json"
account_sid = 'AC63731bfc55e3419b38c1035d7fddd876'
auth_token = '1096d67cb96ca574516d5d8034aca42d'


def generate_uid(jsn: dict):
    return str(uuid4())


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.String(255), primary_key=True, default=generate_uid)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(True), default=db.func.now())
    updated_at = db.Column(db.DateTime(
        True), default=db.func.now(), onupdate=db.func.now())
    is_verified = db.Column(db.Boolean, default=False)
