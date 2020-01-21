from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api

db = SQLAlchemy()

ma = Marshmallow()

api = Api()