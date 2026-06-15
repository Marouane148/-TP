"""Integration tests for HTML interface."""
import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_history():
    """Reset distance history before each test."""
    from app import distance_history
    distance_history.clear()
    yield
    distance_history.clear()


@pytest.mark.html
class TestHTMLForm:
    """Test the HTML form interface."""

    def test_get_index_page(self, client):
        """Test that GET / returns the form page."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Distance Calculator' in response.data
        assert b'Start Point' in response.data
        assert b'End Point' in response.data

    def test_form_contains_inputs(self, client):
        """Test that form contains required input fields."""
        response = client.get('/')
        assert b'apoint' in response.data
        assert b'bpoint' in response.data
        assert b'Calculate Distance' in response.data

    def test_post_valid_coordinates(self, client):
        """Test posting valid coordinates."""
        response = client.post(
            '/',
            data={'apoint': '2,5', 'bpoint': '1,6'}
        )
        assert response.status_code == 200
        assert b'Calculation Result' in response.data

    def test_post_invalid_coordinates(self, client):
        """Test posting invalid coordinates."""
        response = client.post(
            '/',
            data={'apoint': 'invalid', 'bpoint': '1,6'}
        )
        assert response.status_code == 400
        assert b'Error' in response.data

    def test_post_with_spaces(self, client):
        """Test posting coordinates with spaces."""
        response = client.post(
            '/',
            data={'apoint': '  2 , 5  ', 'bpoint': '  1 , 6  '}
        )
        assert response.status_code == 200
        assert b'Calculation Result' in response.data

    def test_pythagorean_calculation_displayed(self, client):
        """Test that 3-4-5 triangle is correctly calculated."""
        response = client.post(
            '/',
            data={'apoint': '0,0', 'bpoint': '3,4'}
        )
        assert response.status_code == 200
        assert b'Calculation Result' in response.data
        assert b'5.0000' in response.data
