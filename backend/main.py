from fastapi import FastAPI

from .geo_routes import router as geo_router
from .pathway_routes import router as pathway_router
from .listing_routes import router as listing_router


app = FastAPI(
    title="ReLoop API",
    description="Intelligent Industrial By-Product Exchange",
    version="1.0"
)


app.include_router(geo_router)
app.include_router(pathway_router)
app.include_router(listing_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "project": "ReLoop",
        "database": "Supabase PostgreSQL"
    }