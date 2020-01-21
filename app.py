import os
from flask import Flask 
from flask_restplus import Api
from api.resources.forecast import CityForecast, ForecastAnalysis
from api.extensions import db, ma, api

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db.init_app(app)
ma.init_app(app)
api.init_app(app)

from api.models import *

if __name__ == '__main__':
    app.run(debug=True)