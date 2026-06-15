"""Integration tests for API endpoints."""
import pytest
import json
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


@pytest.mark.integration
class TestCalculateDistanceEndpoint:
    """Test the /api/distance POST endpoint."""

    def test_valid_request(self, client):
        """Test valid distance calculation request."""
        payload = {
            'start_point': '0,0',
            'end_point': '3,4'
        }
        response = client.post(
            '/api/distance',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['result_distance'] == 5.0
        assert data['start_point'] == [0, 0]
        assert data['end_point'] == [3, 4]

    def test_missing_start_point(self, client):
        """Test request missing start_point field."""
        payload = {'end_point': '1,1'}
        response = client.post(
            '/api/distance',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_missing_end_point(self, client):
        """Test request missing end_point field."""
        payload = {'start_point': '0,0'}
        response = client.post(
            '/api/distance',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_invalid_coordinate_format(self, client):
        """Test request with invalid coordinate format."""
        payload = {
            'start_point': 'invalid',
            'end_point': '1,1'
        }
        response = client.post(
            '/api/distance',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_negative_coordinates(self, client):
        """Test calculation with negative coordinates."""
        payload = {
            'start_point': '-5,-5',
            'end_point': '5,5'
        }
        response = client.post(
            '/api/distance',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        expected_distance = (10 ** 2 + 10 ** 2) ** 0.5
        assert data['result_distance'] == pytest.approx(expected_distance)


@pytest.mark.integration
class TestGetDistancesEndpoint:
    """Test the /api/distances GET endpoint."""

    def test_empty_history(self, client):
        """Test getting distances when history is empty."""
        response = client.get('/api/distances')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_retrieve_history(self, client):
        """Test retrieving distance history."""
        payload = {'start_point': '0,0', 'end_point': '1,1'}
        client.post(
            '/api/distance',
            data=json.dumps(payload),
            content_type='application/json'
        )

        response = client.get('/api/distances')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1


@pytest.mark.integration
class TestClearDistancesEndpoint:
    """Test the /api/distances DELETE endpoint."""

    def test_clear_empty_history(self, client):
        """Test clearing empty history."""
        response = client.delete('/api/distances')
        assert response.status_code == 204

    def test_clear_with_history(self, client):
        """Test clearing history with data."""
        payload = {'start_point': '0,0', 'end_point': '1,1'}
        client.post(
            '/api/distance',
            data=json.dumps(payload),
            content_type='application/json'
        )

        response = client.delete('/api/distances')
        assert response.status_code == 204

        response = client.get('/api/distances')
        data = json.loads(response.data)
        assert len(data) == 0


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling for various scenarios."""

    def test_404_not_found(self, client):
        """Test 404 response for non-existent endpoint."""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
