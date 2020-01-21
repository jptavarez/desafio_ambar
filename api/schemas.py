from marshmallow_sqlalchemy import field_for
from flask_marshmallow.fields import fields
from api.extensions import ma
from api.models import Forecast, City

class PrecipitationSchema(ma.Schema):
    city_id = fields.Int()
    city = fields.Str()
    state = fields.Str()
    mean = fields.Float()

precipitations_schema = PrecipitationSchema(many=True)

class CitySchema(ma.ModelSchema):
    id = field_for(City, 'id', dump_only=True)
    class Meta:
        model = City
    
city_schema = CitySchema()

class ForecastSchema(ma.ModelSchema):
    id = field_for(Forecast, 'id', dump_only=True)
    class Meta:
        model = Forecast
    
forecasts_schema = ForecastSchema(many=True)