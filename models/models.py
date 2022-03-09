from collections import UserString
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
    username = db.Column(db.String(255))
    token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(True), default=db.func.now())
    updated_at = db.Column(db.DateTime(
        True), default=db.func.now(), onupdate=db.func.now())
    is_verified = db.Column(db.Boolean, default=False)
    memory = db.Column(db.Float(), default=0.0)
    speed = db.Column(db.Float(), default=0.0)
    reasoning = db.Column(db.Float(), default=0.0)
    Understanding = db.Column(db.Float(), default=0.0)

    def update(self, user_uid, new_info):
        user = db.session.query(UserString).filter_by(uid=user_uid).first()

        # check if values are the same before changing
        # ensure unique email for all users
        if new_info.get("email"):
            if user.email != new_info.get("email"):
                if db.session.query(User).filter_by(email=new_info["email"]).first() is not None:
                    return {"success": "False", "result": "Email déja utilisé"}

        # password only has length if being changed
        if new_info.get("password"):
            if len(new_info.get("password")):
                hashed = bcrypt.hashpw(
                    new_info["password"].encode("utf-8"), bcrypt.gensalt())
                new_info["password"] = hashed.decode("utf-8")

        db.session.query(User).filter_by(uid=user_uid).update(new_info)
        db.session.commit()
        return {"success": "True", "message": "Profile changé avec succes"}

    def tojson(self):
        return {"uid": self.uid,
                "username": self.username,
                "email": self.email,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_verified": self.is_verified,
                "memory": self.memory,
                "speed": self.speed,
                "reasoning": self.reasoning,
                "Understanding": self.Understanding}


class Game(db.Model):
    __tablename__ = 'game'
    uid = db.Column(db.String(255), primary_key=True, default=generate_uid)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(True), default=db.func.now())

    def tojson(self):
        return {"uid": self.uid,
                "name": self.name,
                "url": self.url,
                "created_at": self.created_at}


class Article(db.Model):
    __tablename__ = 'article'
    uid = db.Column(db.String(255), primary_key=True, default=generate_uid)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(True), default=db.func.now())

    def tojson(self):
        return {"uid": self.uid,
                "name": self.name,
                "url": self.url,
                "created_at": self.created_at}


class Favoris(db.Model):
    __tablename__ = 'favoris'
    uid = db.Column(db.String(255), primary_key=True, default=generate_uid)
    user = db.Column(db.String(255))
    game = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(True), default=db.func.now())

    def tojson(self):
        return {"uid": self.uid,
                "user": self.user,
                "game": self.game,
                "created_at": self.created_at}
