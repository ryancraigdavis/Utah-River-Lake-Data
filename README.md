# Utah River & Lake Data

Real-time water level monitoring for Utah rivers, lakes, and reservoirs using USGS data.

## Features

- 📊 Real-time river flow and temperature data
- 🏔️ Lake and reservoir water levels
- 🌊 Great Salt Lake and Bear Lake monitoring
- 📱 Responsive web interface
- 🔄 Auto-refreshing data feeds

## Architecture

- **Backend**: FastAPI with USGS API integration
- **Frontend**: Svelte with responsive design
- **Deployment**: Docker Compose on TrueNAS Scale

## Development

### Backend
```bash
cd backend
uv sync
hatch run dev-server
# Access: http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Access: http://localhost:3000
```

## Production Deployment

### Docker Compose (TrueNAS Scale)
```bash
docker-compose up -d
```

### Services
- **Backend**: http://104.173.199.40:8000
- **Frontend**: http://104.173.199.40:3000
- **API Docs**: http://104.173.199.40:8000/docs

## API Endpoints

### Rivers
- `GET /api/v1/rivers/sites` - List river monitoring sites
- `GET /api/v1/rivers/current` - Current river data
- `GET /api/v1/rivers/historical` - Historical river data

### Lakes
- `GET /api/v1/lakes/sites` - List lake monitoring sites
- `GET /api/v1/lakes/current` - Current lake data
- `GET /api/v1/lakes/great-salt-lake` - Great Salt Lake data
- `GET /api/v1/lakes/bear-lake` - Bear Lake data

## Data Sources

- **USGS Water Services API**: Real-time and historical water data
- **Monitoring Sites**: 10 Utah river sites, 8 lake/reservoir sites
- **Parameters**: Flow rates, water temperature, gage height, storage volume

## Tech Stack

- **Backend**: Python 3.12, FastAPI, Uvicorn, Gunicorn, httpx
- **Frontend**: Svelte, Vite, JavaScript
- **Deployment**: Docker, Docker Compose
- **Data**: USGS Water Services API