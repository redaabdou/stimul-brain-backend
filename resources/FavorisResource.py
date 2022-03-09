from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import flask
from models.models import *
from flask_cors import cross_origin


class FavorisResource(Resource):
    @jwt_required()
    @cross_origin()
    def post(self, game_uid):
        if not request.is_json or request.content_length >= 50_000_000:
            return flask.make_response(flask.jsonify(success=False, message="Please send a valid json"), 400)
        user_uid = get_jwt_identity()

        newFavoris = Favoris(user=user_uid, game=game_uid)
        db.session.add(newFavoris)
        db.session.commit()
        return flask.make_response(flask.jsonify(success=True), 200)
