# Distance Calculator - 2D Plane

A professional Flask application for calculating Euclidean distances between two points in a 2D plane.

## Features

- ✅ Web interface with modern UI
- ✅ RESTful JSON API
- ✅ Comprehensive input validation
- ✅ 97% test coverage (43 tests)
- ✅ Production-ready error handling

## Quick Start

```bash
pip install flask pytest pytest-cov
python app.py
```

Then visit: `http://localhost:5000`

## API Endpoints

- `POST /api/distance` - Calculate distance (JSON)
- `GET /api/distances` - Retrieve history
- `DELETE /api/distances` - Clear history

## Testing

```bash
pytest --cov=app --cov-report=html
```

## TP Documentation

- `REPONSES_TP.md` - Answers to 7 TP questions
- `ANALYSIS.md` - Detailed code analysis
