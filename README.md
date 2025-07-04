# Wimbledon Finals API

A REST API that provides information about Wimbledon finals by year.

## Features

- Get Wimbledon final information for any year
- Production-ready with proper error handling
- Health check endpoint
- CORS enabled
- CSV data loading

## API Endpoints

### GET /wimbledon?year={year}

Returns information about the Wimbledon final for the specified year.

**Example Request:**
```
GET /wimbledon?year=2021
```

**Example Response:**
```json
{
  "year": 2021,
  "champion": "Novak Djokovic",
  "runner_up": "Matteo Berrettini",
  "score": "6–7(4–7), 6–4, 6–4, 6–3",
  "sets": 4,
  "tiebreak": true
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Wimbledon API is running"
}
```

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd wimbledon-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure you have the `wimbledon_finals.csv` file in the root directory

4. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## CSV File Format

The `wimbledon_finals.csv` file should have the following columns:
- `year`: Year of the final
- `champion`: Name of the champion
- `runner_up`: Name of the runner-up
- `score`: Match score
- `sets`: Number of sets played
- `tiebreak`: 1 if tiebreak occurred, 0 otherwise

## Deployment

This API is designed to be deployed on platforms like:
- Render (free tier)
- Vercel (with Flask adapter)
- PythonAnywhere (free tier)
- Heroku (hobby tier)

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 400: Bad Request (invalid year parameter)
- 404: Not Found (no data for specified year)
- 500: Internal Server Error

## Production Considerations

- Data is loaded from CSV on startup
- Proper logging configuration
- CORS enabled for cross-origin requests
- Input validation and sanitization
- Comprehensive error handling