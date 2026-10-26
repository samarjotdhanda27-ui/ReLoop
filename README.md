# ReLoop — Intelligent Industrial By-Product Exchange

Team Debuggers | Code Yudh 2026 | Chandigarh University

Track: Energy, Environment and Climate Action

## About ReLoop

ReLoop is an Android application that connects industrial
by-product sellers with potential buyers.

It provides:
- Research-backed reuse pathway discovery
- Geographic matching
- Explainable compatibility recommendations
- Digital Material Passports
- QR code access to material records

## Technology

- Android: Kotlin + Jetpack Compose
- Backend: Python + FastAPI
- Database: Supabase PostgreSQL
- Geographic Matching: Haversine formula

## Completed Work

- Fly ash reuse pathway dataset
- Punjab/Haryana demonstration facility dataset
- Geographic matching engine
- Geographic matching API
- Reuse pathway discovery API
- Automated geographic matching tests

## Run Backend

Install dependencies:

    pip install -r requirements.txt

Start server:

    python -m uvicorn backend.main:app --reload

API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

GET /health

GET /geo/matches/{seller_id}

POST /geo/calculate

GET /pathways/{material_name}

## Important

All demonstration facilities and quantities are synthetic.

ReLoop provides decision support, not industrial
safety or compliance certification.