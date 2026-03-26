# RevAI — AI-Powered Sales Platform

## Setup Instructions

1. **Clone the repository**
2. **Environment Variables**: Copy `.env.example` to `.env` and fill in your API keys
   ```bash
   cp .env.example .env
   ```
3. **Start the application**: Run Docker Compose to build and start the services
   ```bash
   docker-compose up --build
   ```

## Services
- **Frontend**: [http://localhost:3000](http://localhost:3000) (Next.js)
- **Backend API**: [http://localhost:8000](http://localhost:8000) (FastAPI)
- **Postgres**: `localhost:5432`
- **Redis**: `localhost:6379`