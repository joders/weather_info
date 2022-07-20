import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

# a more decent solution would use a mock remote 
# service instead of relying on tgftp.nws.noaa.gov
# but in the interest of time:

def test_endpoint_with_present_location(client):
    response = client.get('/ASEZ')
    assert response.status_code == 200

def test_endpoint_with_unknown_location(client):
    response = client.get('/NONSENSE')
    assert response.status_code == 404

