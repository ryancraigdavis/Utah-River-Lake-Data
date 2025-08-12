# Utah River Lake Backend

FastAPI backend service for Utah river and lake water level monitoring.

## Features

- Real-time USGS data integration
- River flow and temperature monitoring
- Lake and reservoir water level tracking
- RESTful API endpoints
- CORS support for web frontend

## API Endpoints

- `GET /health` - Health check
- `GET /api/v1/rivers/*` - River data endpoints
- `GET /api/v1/lakes/*` - Lake data endpoints

## Technology Stack

- FastAPI
- Python 3.12+
- Uvicorn/Gunicorn
- HTTPX for API calls
- Pydantic for data validation