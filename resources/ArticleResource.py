from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import flask
from models.models import *
from flask_cors import cross_origin


class ArticleResource(Resource):
    @cross_origin()
    def get(self, article_uid):

        article = Article.query.filter_by(uid=article_uid).first()

        if article is not None:
            return flask.jsonify({"data": article.tojson(), "success": True})
        else:
            return flask.make_response(flask.jsonify(success=False, message="article non trouvé"), 400)

    @cross_origin()
    def post(self):
        if not request.is_json or request.content_length >= 50_000_000:
            return flask.make_response(flask.jsonify(success=False, error={"code": 100, "message": "Please send a valid json"}), 400)

        obj = request.get_json()
        per_page = 20

        if obj.get("page"):
            page = obj.get("page")
        else:
            page = 1

        result = db.session.query(Article).paginate(page, per_page, False)
        total = result.total
        record_items = result.items

        data = [article.tojson() for article in record_items]
        return flask.jsonify(data=data, count=total, success=True)
