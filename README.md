# Wimbledon Finals API

A REST API that provides information about Wimbledon finals by year with secure authentication.

## 🔐 Authentication Required

This API requires authentication to access all endpoints (except `/health`). You can use either:
- **API Key** (recommended)
- **Basic Authentication** (username/password)

## 🚀 Live API

**Deployed on Render.com:** https://tennis-winner-api-5yhm.onrender.com

**Note:** All endpoints require authentication. See [Getting API Access](#-getting-api-access) section below.

## 🔑 Getting API Access

This API is hosted on Render.com's free tier with limited resources. To get your personal API credentials:

**Contact:** [titantheven@gmail.com](mailto:titantheven@gmail.com)

**Please include:**
- Your name
- Intended use case
- Expected usage volume
- Preferred authentication method

**You'll receive within 24 hours:**
- Your unique API key
- Basic Auth credentials (if preferred)
- Usage guidelines

## API Endpoints

### Authentication Methods

#### Method 1: API Key (Recommended)
```bash
# Via Header
curl -H "X-API-Key: YOUR_API_KEY" "https://tennis-winner-api-5yhm.onrender.com/wimbledon?year=2021"

# Via Query Parameter
curl "https://tennis-winner-api-5yhm.onrender.com/wimbledon?year=2021&api_key=YOUR_API_KEY"
```

#### Method 2: Basic Authentication
```bash
curl -u username:password "https://tennis-winner-api-5yhm.onrender.com/wimbledon?year=2021"
```

### Endpoints

#### `GET /health`
Health check endpoint (no authentication required).

**Example:**
```
GET https://tennis-winner-api-5yhm.onrender.com/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Wimbledon API is running"
}
```

#### `GET /wimbledon?year={year}`
Returns information about the Wimbledon final for the specified year.

**Example Request:**
```
GET /wimbledon?year=2021&api_key=YOUR_API_KEY
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

#### `GET /wimbledon/player/{player_name}`
Get statistics for a specific player's Wimbledon finals.

**Example Request:**
```
GET /wimbledon/player/federer?api_key=YOUR_API_KEY
```

**Example Response:**
```json
{
  "player_search": "federer",
  "total_finals": 12,
  "wins": 8,
  "losses": 4
}
```

## Features

- Historical Wimbledon finals data (1877-2024)
- Player statistics and search functionality
- Secure API with dual authentication methods
- Production-ready with proper error handling
- Health check endpoint
- CORS enabled for cross-origin requests
- Automatic data extraction from Wikipedia
- CSV data loading
- Pretty-printed JSON responses

## Local Development

### Setup and Installation

1. **Clone the repository:**
```bash
git clone https://github.com/PLUTOLEARNS/tennis-winner-api.git
cd tennis-winner-api
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create a `.env` file** (optional - for authentication):
```env
# API Authentication (optional for local development)
API_KEY=your-local-api-key-here
USERNAME=your-username
PASSWORD=your-password
```

4. **Run the application:**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Running Without Authentication (Local Only)
To disable authentication for local development, comment out the `@require_auth` decorators in `app.py`:

```python
@app.route('/wimbledon', methods=['GET'])
# @require_auth  # Comment this line for local testing
def get_wimbledon_final():
    # ... rest of the code
```

## CSV File Format

The `wimbledon_finals.csv` file should have the following columns:
- `year`: Year of the final
- `champion`: Name of the champion
- `runner_up`: Name of the runner-up
- `score`: Match score
- `sets`: Number of sets played
- `tiebreak`: 1 if tiebreak occurred, 0 otherwise

## Error Handling

The API returns appropriate HTTP status codes:
- **200**: Success
- **400**: Bad Request (invalid year parameter)
- **401**: Unauthorized (missing or invalid authentication)
- **403**: Forbidden (invalid API key or credentials)
- **404**: Not Found (no data for specified year)
- **500**: Internal Server Error

## Security

- All endpoints (except `/health`) require authentication
- API keys should be kept secret and not shared
- HTTPS encryption in production
- Proper input validation and sanitization
- Comprehensive error handling and logging

## Deployment

This API is deployed on Render.com's free tier. For production use considerations:
- Free tier may have cold start delays
- Limited monthly hours and bandwidth
- Automatic sleep after 15 minutes of inactivity
- For high-traffic applications, consider upgrading to a paid tier

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

For API access requests, questions, or support:
- **Email:** [titantheven@gmail.com](mailto:titantheven@gmail.com)
- **GitHub:** [PLUTOLEARNS](https://github.com/PLUTOLEARNS)

---

**⚠️ Important:** This API is hosted on Render.com's free tier. Please be respectful of usage limits and contact for API access before making requests.