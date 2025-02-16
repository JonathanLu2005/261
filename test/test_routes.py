# Install pytest pytest-flask: pip install pytest pytest-flask

import pytest
import os
import sys

# Add root directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from app import app


# Create fixture to create a test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Currently only testing response status codes
# Test root route ("/") TODO: after pages implement content - check for content specific terms in response data
def test_model_page(client):
    response = client.get("/")
    assert response.status_code == 200
    #assert b"model page specific content" in response.data

# testing /junctionPage route
def test_junction_page(client):
    response = client.get("/junctionPage")
    assert response.status_code == 200

# testing /helpPage route
def test_help_page(client):
    response = client.get("/helpPage")
    assert response.status_code == 200