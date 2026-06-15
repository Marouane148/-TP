from flask import Flask, request, render_template, jsonify
from math import sqrt
from datetime import datetime
from typing import Tuple, Dict, List, Any

app = Flask('my_distance')

distance_history: List[Dict[str, Any]] = []
MAX_HISTORY_SIZE = 1000


def calculate_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    """Calculate Euclidean distance between two 2D points using Pythagorean theorem."""
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def parse_coordinates(coord_str: str) -> Tuple[int, int]:
    """Parse coordinate string in format 'x,y' into tuple of integers."""
    try:
        parts = coord_str.strip().split(',')
        if len(parts) < 2:
            raise ValueError("Coordinates must contain at least x and y values")
        x = int(parts[0].strip())
        y = int(parts[1].strip())
        return (x, y)
    except ValueError as e:
        raise ValueError(f"Invalid coordinate format: {str(e)}")


def create_result(x1: int, y1: int, x2: int, y2: int) -> Dict[str, Any]:
    """Create a result object containing the distance calculation and metadata."""
    distance = calculate_distance(x1, y1, x2, y2)
    return {
        'requested_at': datetime.now().isoformat(),
        'result_distance': distance,
        'start_point': [x1, y1],
        'end_point': [x2, y2]
    }


@app.route('/', methods=['GET', 'POST'])
def html_calculate():
    if request.method == 'GET':
        return render_template('index.html', result=None)

    if request.method == 'POST':
        try:
            start_x, start_y = parse_coordinates(request.form['apoint'])
            end_x, end_y = parse_coordinates(request.form['bpoint'])

            result = create_result(start_x, start_y, end_x, end_y)

            if len(distance_history) < MAX_HISTORY_SIZE:
                distance_history.append(result)

            return render_template('index.html', result=result)
        except ValueError as e:
            return render_template('index.html', error=str(e)), 400


@app.route('/api', methods=['GET'])
def api_root():
    """API root endpoint - returns available endpoints."""
    return jsonify({
        'endpoints': {
            'GET /api/distances': 'Retrieve all calculated distances',
            'POST /api/distance': 'Calculate distance between two points'
        }
    })


@app.route('/api/distances', methods=['GET'])
def get_distances():
    """Retrieve all calculated distances from history."""
    return jsonify(distance_history)


@app.route('/api/distances', methods=['DELETE'])
def clear_distances():
    """Clear all distance history."""
    global distance_history
    distance_history = []
    return jsonify({'message': 'Distance history cleared'}), 204


@app.route('/api/distance', methods=['POST'])
def calculate_distance_api():
    """Calculate distance between two points via JSON API."""
    try:
        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({'error': 'Request must contain JSON'}), 400

        if 'start_point' not in data or 'end_point' not in data:
            return jsonify({'error': 'Missing required fields: start_point, end_point'}), 400

        start_x, start_y = parse_coordinates(data['start_point'])
        end_x, end_y = parse_coordinates(data['end_point'])

        result = create_result(start_x, start_y, end_x, end_y)

        if len(distance_history) < MAX_HISTORY_SIZE:
            distance_history.append(result)

        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors."""
    return jsonify({'error': 'Method not allowed'}), 405