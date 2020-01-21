from flask import abort
from flask_restplus import Resource
from api.extensions import db, api
from api.models import Forecast, City 
from api.schemas import forecasts_schema, city_schema, precipitations_schema
from api.forecast.services import get_instance
from api.utils import str_to_date

@api.route('/cidade/<int:city_code>')
class CityForecast(Resource):
    def get(self, city_code):
        try:
            forecast_service = get_instance()
            forecasts = forecast_service.get_city_forecast(city_code)            
        except ValueError as e:
            return {
                'message': str(e)
            }, 400
        except RuntimeError as e:
            # a api de forecast não processou a requisição corretamente.
            return {
                'message': 'Serviço indisponível no momento. Por favor, tente novamente mais tarde.'
            }, 503    
        return forecasts_schema.dump(forecasts)      

@api.route('/analise/<string:initial_date>/<string:final_date>')
class ForecastAnalysis(Resource):
    def get(self, initial_date, final_date): 
        initial_date = str_to_date(initial_date).date()
        final_date = str_to_date(final_date).date()
        forecast_service = get_instance()
        city = forecast_service.get_city_highest_temperature(initial_date, final_date)   
        precipitations = forecast_service.get_mean_precipitation_by_city(initial_date, final_date)
        return {
            'city_highest_temperature': city_schema.dump(city),
            'mean_precipitation_by_city': precipitations_schema.dump(precipitations),
        }  