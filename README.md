# ValorTracker - Backend System

ValorTracker is an advanced, full-stack predictive coaching and performance analysis platform for VALORANT players. This repository houses the highly scalable Python FastAPI backend.

## 🚀 Architecture Overview

This backend is designed with production-grade engineering principles, utilizing a decoupled architecture to ensure low-latency API responses even during heavy data processing.

*   **API Layer:** Built with **FastAPI**, providing high-performance, asynchronous endpoints.
*   **Database:** **PostgreSQL** running on Render, storing normalized player statistics and match histories.
*   **Vector Database:** Utilizing the **pgvector** Postgres extension to store thousands of AI-generated situational coaching tips and map strategies.
*   **Caching & Queue Broker:** **Upstash Redis** is used as a lightning-fast data cache (TTL) for API responses and as the message broker for Celery.
*   **Message Queue / Workers:** **Celery** background tasks handle Riot Games API polling. This completely unblocks the main FastAPI thread, preventing bottlenecks when querying massive 20+ match datasets from external Riot servers.
*   **ORM & Migrations:** **SQLModel** (SQLAlchemy) for seamless database transactions and **Alembic** for automated schema migrations.
*   **AI Integration:** Deep integration with the **Google Gemini API** to provide dynamic, personalized coaching insights.

## ⚙️ Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file or cloud provider:

```env
# Database
CONNECTION_STRING=postgresql://username:password@host/database
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_PORT=5432
DB_NAME=...

# Redis & Celery
REDIS_URL=rediss://default:password@host:port

# Third-Party APIs
ACCESS_TOKEN=your_riot_api_token
GEMINI_API_KEY=your_gemini_api_key
```

## 🛠️ Deployment (Render)

This backend is fully containerized and configured for automated deployment on **Render**.

1.  The `start.sh` script acts as the entry point.
2.  It automatically runs `alembic upgrade head` to ensure the Postgres schema is up-to-date.
3.  It spins up the Celery asynchronous worker in the background.
4.  It launches the FastAPI Uvicorn ASGI server on `0.0.0.0:10000`.

*Note: Due to the Render port-binding architecture, Celery and FastAPI run seamlessly on the same Web Service instance.*
