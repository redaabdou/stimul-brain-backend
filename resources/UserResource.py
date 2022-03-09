from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import flask
from models.models import *
from flask_cors import cross_origin


class UserResource(Resource):
    @jwt_required()
    @cross_origin()
    def get(self):
        user_uid = get_jwt_identity()

        user = User.query.filter_by(uid=user_uid).first()

        if user is not None:
            return flask.jsonify({"data": user.tojson(), "success": True})
        else:
            return flask.make_response(flask.jsonify(success=False, message="utilisateur non trouvé"), 400)

    @jwt_required()
    @cross_origin()
    def put(self):
        new_info = request.get_json()
        user_uid = get_jwt_identity()

        user = User.query.filter_by(uid=user_uid).first()

        if user is not None:
            user.update(user_uid, new_info)
        else:
            return flask.make_response(flask.jsonify(success=False, message="utilisateur non trouvé"), 400)
        db.session.commit()
        return flask.jsonify(success=True, result="informations changées avec succes")

    @jwt_required()
    @cross_origin()
    def delete(self):
        user_uid = get_jwt_identity()

        user = User.query.filter_by(uid=user_uid).first()

        if user is not None:
            db.session.query(User).filter_by(uid=user_uid).delete()
        else:
            return flask.make_response(flask.jsonify(success=False, message="utilisateur non trouvé"), 400)
        db.session.commit()
        return flask.jsonify(data=user_uid, success=True)
