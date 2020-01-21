import requests

class BaseForecastClient:
    def get_city_forecast(city_code):
        raise NotImplementedError

class ClimaTempoClient(BaseForecastClient):

    token = 'b22460a8b91ac5f1d48f5b7029891b53' # TODO: move it to env
    base_url = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/'
    
    def get_city_forecast(self, city_code):
        url = self.base_url + 'locale/{city_code}/days/15?token={token}'.format(
            city_code=city_code,
            token=self.token
        )
        response = requests.get(url)
        if response.status_code == 400:
            raise ValueError('Código da cidade invalido.')
        elif response.status_code != 200:            
            raise RuntimeError('A requisição não foi processada pelo Clima Tempo.')
        return response.json()