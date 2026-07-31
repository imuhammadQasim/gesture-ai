# Gesture AI Backend

This is the FastAPI backend for the Gesture AI SaaS Platform. It provides a clean, simple, and modular architecture designed for real-time hand gesture interaction, style transformation, background removal, and AI image generation.

## Project Structure

The project is organized following Domain-Driven Design and layered architecture principles:

- `app/api/`: API Routers and endpoints.
- `app/core/`: Core application configuration, Database connection, Cloudinary init.
- `app/models/`: Database ORM models using SQLModel.
- `app/schemas/`: Pydantic models for API request/response validation.
- `app/services/`: Business logic layer.
- `app/ai/`: Placeholders for AI model implementation.
- `app/utils/`: Generic helper functions.

## Prerequisites

- Python 3.10+
- `pip` or another package manager

## Configuration

The application uses Pydantic Settings to manage configuration via environment variables.

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Update the values in `.env`:
   - **Database**: By default, it uses a local SQLite database (`sqlite:///./database.db`) for easy development. For production, change `DATABASE_URL` to a PostgreSQL connection string (e.g., `postgresql+psycopg2://user:password@localhost/dbname`).
   - **Cloudinary**: Fill in `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET` to enable image/video uploading.

## Installation & Running Locally

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or `venv\Scripts\activate` on Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

The server will automatically start on `http://127.0.0.1:8000`. The Swagger UI documentation is available at `http://127.0.0.1:8000/docs`.

On startup, the app automatically initializes the database tables and Cloudinary based on your environment variables.
