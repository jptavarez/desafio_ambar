import os
import tempfile
import pytest
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

def test_dummy(client):
    assert 1 == 1, 'Erro ateste'
    