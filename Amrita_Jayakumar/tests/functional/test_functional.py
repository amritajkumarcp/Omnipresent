import pytest
import flaskr

@pytest.fixture
def client():
    # Prepare before your test
    flaskr.app.config["TESTING"] = True
    with flaskr.app.test_client() as client:
        # Give control to your test
        yield client
    # Cleanup after the test run.
    # ... nothing here, for this simple example


    
def test_home_page_route():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client().get('/')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Omni API'

def test_home_page_post():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = client().post("/")

    # Create a test client using the Flask application configured for testing
    assert response.status_code == 405
    assert b"Omni API" not in response.data