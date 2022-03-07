"""
The entry point to the backend of Bidjobs app
"""
from flask_cors import CORS
import datetime
from flask import Flask
import logging as log
from flask_jwt_extended import JWTManager
from flask_restful import Api
from models.models import *
log.basicConfig(format='%(levelname)s:%(message)s', level=log.DEBUG)

application = Flask(__name__)
cors = CORS(application)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://reda:ef7zgHFRoln9i8dRLWUS@database-1.cdyguxgp6lky.eu-west-3.rds.amazonaws.com:3307/stimulbrain'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_POOL_RECYCLE'] = 1800
application.config['SQLALCHEMY_POOL_TIMEOUT'] = 50
application.config['SQLALCHEMY_POOL_SIZE'] = 10
application.config['JWT_SECRET_KEY'] = 'mySecret'
application.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
application.config['MAIL_SERVER'] = 'smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USE_SSL'] = True
application.config['MAIL_USERNAME'] = 'redaabdou49@gmail.com'
application.config['MAIL_PASSWORD'] = 'hblnjyhikjcddhli'
application.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(application)
db.init_app(application)  # db defined in api_base

api = Api(application)

if __name__ == "__main__":
    with application.app_context():
        db.create_all()
    application.run()
