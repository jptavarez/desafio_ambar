from sqlalchemy import desc
from sqlalchemy.sql.expression import func
from api.extensions import db
from api.forecast.clients import BaseForecastClient, ClimaTempoClient
from api.models import City, State, Forecast
from api.utils import str_to_date

class ForecastService:
    def __init__(self, client: BaseForecastClient):
        self.client = client

    def get_city_forecast(self, city_code):
        data = self.client.get_city_forecast(city_code)
        self._validate_data(data)
        return self._persist_forecast(data)
    
    def get_city_highest_temperature(self, initial_date, final_date):
        data = db.session.query(City).with_entities(
                func.max(Forecast.max_temperature).label('temperature'),
                City.id.label('city')
            ) \
            .join(Forecast) \
            .filter(Forecast.date >= initial_date) \
            .filter(Forecast.date <= final_date) \
            .group_by(City.id) \
            .first()
        if not data:
            return None
        return City.query.get(data.city)
        
    
    def get_mean_precipitation_by_city(self, initial_date, final_date):
        return db.session.query(City).with_entities(
                City.id.label('city_id'),
                City.name.label('city'),
                State.abbreviation.label('state'),
                func.avg(Forecast.rain_precipitation).label('mean')
            ) \
            .join(State) \
            .join(Forecast) \
            .filter(Forecast.date >= initial_date) \
            .filter(Forecast.date <= final_date) \
            .group_by(City.id) \
            .order_by(desc('mean')).all()

    def _persist_forecast(self, data):
        city = City.get_or_create(data['id'], data['name'], data['state'], data['country'])
        forecasts = []
        for forecast_data in data['data']:
            forecast = Forecast.update_or_create(
                city_id=city.id, 
                date=str_to_date(forecast_data['date']).date(), 
                rain_probability=forecast_data['rain']['probability'], 
                rain_precipitation=forecast_data['rain']['precipitation'],
                min_temperature=forecast_data['temperature']['min'], 
                max_temperature=forecast_data['temperature']['max']
            )
            forecasts.append(forecast)
        db.session.commit()
        return forecasts

    def _validate_data(self, data):
        fields = [
            'id',
            'name',
            'state',
            'country',
            'data'
        ]    
        for field in fields:
            if field not in data:
                raise ValueError('Field {} not found in the json data'.format(field))
        data_fields = [
            'date',
            'rain',
            'temperature'
        ]
        for forecast_data in data['data']:
            for field in data_fields:            
                if field not in forecast_data:
                    raise ValueError('Field data.{} not found in the json data'.format(field))

def get_instance():
    client = ClimaTempoClient()
    return ForecastService(client)