from api.extensions import db

class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(10), nullable=False, unique=True)

    @staticmethod 
    def get_or_create(abbreviation):
        country = Country.query.filter_by(abbreviation=abbreviation).first()
        if country:
            return country 
        country = Country()
        country.abbreviation = abbreviation
        db.session.add(country)
        db.session.flush()
        return country

class State(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(10), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('abbreviation', 'country_id', name='_state_country_id_uc'),
    )

    @staticmethod
    def get_or_create(abbreviation, country):
        state = State.query.filter_by(abbreviation=abbreviation) \
            .join(Country) \
            .filter(Country.abbreviation == country) \
            .first() 
        if state:
            return state 
        country = Country.get_or_create(country)
        state = State()
        state.abbreviation = abbreviation
        state.country_id = country.id
        db.session.add(state)
        db.session.flush()
        return state

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    @staticmethod
    def get_or_create(code, name, state, country):
        city = City.query.filter_by(code=code).first() 
        if city:
            return city 
        state = State.get_or_create(state, country)
        city = City()
        city.code = code
        city.name = name 
        city.state_id = state.id 
        db.session.add(city)
        db.session.flush()
        return city

class Forecast(db.Model):
    __tablename__ = 'forecast'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    rain_probability = db.Column(db.Integer, nullable=False)
    rain_precipitation = db.Column(db.Integer, nullable=False)
    min_temperature = db.Column(db.Integer, nullable=False)
    max_temperature = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('city_id', 'date', name='_forecast_city_id_date_uc'),
    )

    @staticmethod
    def update_or_create(
        city_id, date, rain_probability, rain_precipitation, 
        min_temperature, max_temperature):
        forecast = Forecast.query.filter_by(city_id=city_id, date=date).first()
        forecast = forecast if forecast else Forecast()
        forecast.city_id = city_id
        forecast.date = date
        forecast.rain_probability = rain_probability
        forecast.rain_precipitation = rain_precipitation
        forecast.min_temperature = min_temperature
        forecast.max_temperature = max_temperature
        db.session.add(forecast)
        db.session.flush()
        return forecast    