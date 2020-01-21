import os
import tempfile
import pytest
from datetime import datetime, timedelta
from app import app, db

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db_test.sqlite')
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()                     
        yield client
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])    

def test_cidade(client):
    response = client.get('/cidade/6731')
    data = response.get_json()
    assert response.status_code == 200, 'Erro ao buscar forecast da cidade'
    for forecast in data:
        assert 'id' in forecast, 'id não encontrado no json retornado'
        assert 'date' in forecast, 'date não encontrado no json retornado'
        assert 'rain_precipitation' in forecast, 'rain_precipitation não encontrado no json retornado'
        assert 'rain_probability' in forecast, 'rain_probability não encontrado no json retornado'
        assert 'min_temperature' in forecast, 'min_temperature não encontrado no json retornado'
        assert 'max_temperature' in forecast, 'max_temperature não encontrado no json retornado'
    
    # testando cidade invalida
    response = client.get('/cidade/56565656565656')
    assert response.status_code == 400, 'Erro ao buscar forecast da cidade'
    data = response.get_json()
    assert 'message' in data, 'Mensagem de erro não encontrada no json retornado'
    
def test_analise(client):
    initial_date = datetime.now()
    final_date = initial_date + timedelta(days=15)
    initial_date = initial_date.strftime("%Y-%m-%d")
    final_date = final_date.strftime("%Y-%m-%d")
    
    client.get('/cidade/6731')
    client.get('/cidade/3477')
    client.get('/cidade/6730')
    
    response = client.get('/analise/{}/{}'.format(initial_date, final_date))
    assert response.status_code == 200, 'Erro ao buscar a analise'
    
    data = response.get_json()
    assert 'city_highest_temperature' in data, 'city_highest_temperature não encontrado no json retornado'
    assert 'mean_precipitations' in data, 'mean_precipitations não encontrado no json retornado'
    
    city_highest_temperature = data['city_highest_temperature']
    assert 'id' in city_highest_temperature, 'city_highest_temperature.id não encontrado no json retornado'
    assert 'code' in city_highest_temperature, 'city_highest_temperature.code não encontrado no json retornado'
    assert 'name' in city_highest_temperature, 'city_highest_temperature.name não encontrado no json retornado'
    
    mean_precipitations = data['mean_precipitations']
    assert len(mean_precipitations) == 3, 'Quantidade de médias de precipitação incorreta'
    for precipitation in mean_precipitations:
        assert 'city' in precipitation, 'mean_precipitations.city não encontrado no json retornado'
        assert 'city_id' in precipitation, 'mean_precipitations.city_id não encontrado no json retornado'
        assert 'state' in precipitation, 'mean_precipitations.state não encontrado no json retornado'
        assert 'mean' in precipitation, 'mean_precipitations.mean não encontrado no json retornado'
    

    
    