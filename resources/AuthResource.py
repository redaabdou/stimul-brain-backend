import flask
from flask import request, render_template

from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token

from werkzeug.exceptions import InternalServerError
from flask_restful import Resource
from models.models import *
import bcrypt
import datetime
import random
import string
import re
from flask_cors import cross_origin
import urllib

# for validating an Email
regex = "[^@]+@[^@]+\.[^@]{2,3}$"


def checkLogin(newUser):
    email = newUser["email"]
    password = newUser["password"]

    user = User.query.filter_by(email=email).first()

    if user is not None:
        if (not (bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')))):
            return ""
        return user

    else:
        return ""


class AuthLoginResource(Resource):
    @cross_origin()
    def post(self):
        if not request.is_json or request.content_length >= 50_000_000:
            return flask.make_response(flask.jsonify(success=False, message="Please send a valid json"), 400)
        obj = request.get_json()
        resultUser = checkLogin(obj)
        if resultUser != "":
            delta = datetime.timedelta(days=1)
            access_token = create_access_token(
                identity=resultUser.uid, expires_delta=delta)
            try:
                return flask.make_response(flask.jsonify(success=True,
                                                         expiration_date=(datetime.datetime.now() + delta).strftime(
                                                             '%Y-%m-%dT%H:%M:%SZ'),
                                                         Token=access_token.decode(
                                                             "utf-8"),
                                                         refresh_token=create_refresh_token(
                                                             identity=resultUser.uid).decode("utf-8"),
                                                         user=resultUser.tojson()
                                                         ), 200)
            except:
                return flask.make_response(flask.jsonify(success=True,
                                                         expiration_date=(datetime.datetime.now() + delta).strftime(
                                                             '%Y-%m-%dT%H:%M:%SZ'),
                                                         Token=access_token,
                                                         refresh_token=create_refresh_token(
                                                             identity=resultUser.uid),
                                                         user=resultUser.tojson()
                                                         ), 200)
        else:
            return flask.make_response(flask.jsonify(success=False, message="Email ou mot de passe incorrect"), 404)

    @jwt_required()
    @cross_origin()
    def delete(self):
        user_uid = get_jwt_identity()

        user = User.query.filter_by(uid=user_uid).first()

        if user is not None:
            user.refresh_token = None
        db.session.commit()
        return flask.jsonify(response="Successfully logged out", success=True)


class AuthRegisterResource(Resource):
    @cross_origin()
    def post(self):
        user = request.get_json()
        token = ''.join(random.choice(string.octdigits +
                                      string.ascii_letters) for x in range(8))
        try:
            if re.search(regex, user["email"]):
                if db.session.query(User).filter_by(email=user["email"]).first():
                    hashed = bcrypt.hashpw(
                        user["password"].encode("utf-8"), bcrypt.gensalt())

                    newUser = User(password=hashed.decode(
                        "utf-8"), email=user["email"], username=user["username"])
                    message = Mail(
                        from_email='contact@bidjobs.io',
                        to_emails=user["email"],
                        subject='Welcome to Stimul Brain',
                        html_content=render_template('welcome.html'))
                    try:
                        sg = SendGridAPIClient(SendGrid_API_Client)
                        sg.send(message)
                    except Exception as e:
                        print(e.message)
                    db.session.add(newUser)
                    db.session.commit()
                    return flask.make_response(flask.jsonify(resultat=user, success=True), 200)
                else:
                    return flask.make_response(flask.jsonify(success=False, message="Email déja utilisé"), 409)
            else:
                return flask.make_response(flask.jsonify(success=False, message="Merci d'utiliser un email valide"), 400)
        except KeyError:
            return flask.make_response(flask.jsonify(success=False, message="Merci de remplire toutes les informations"), 400)
