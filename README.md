# Weather Aggregation Service

**Production-ready full-stack application** that aggregates weather data from multiple APIs and displays forecasts.

## Tech Stack

**Backend:** FastAPI, Redis  
**Frontend:** React, Tailwind  
**Deployment:** Docker Compose, Nginx, SSL

## Features

- Aggregates data from multiple weather APIs
- Forecasts and interactive charts
- City search with autocomplete
- Auto geolocation discovery
- Redis caching for performance
- Production deployment with SSL and Docker containerization

## Development Setup

1. Clone repository:
   ```bash
   git clone https://github.com/IlyaViz/coursework-4
   cd coursework-4
   ```

2. Create `.env` in `/backend` with API keys:
   ```env
   OPEN_WEATHER_MAP_API_KEY=your_key
   WEATHER_API_KEY=your_key
   GEOCODE_API_KEY=your_key
   ```

3. Start development environment:
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

4. Access application:
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000

## Production Deployment

1. Set domain in `.env`:
   ```env
   DOMAIN=yourdomain.com
   ```

2. Deploy:
   ```bash
   ./run_prod.sh
   ```

3. Access: https://yourdomain.com
