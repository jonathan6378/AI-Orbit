from fastapi import FastAPI

from src.api.routes import router


app = FastAPI(
    title="AI Orbit Graph API",
    description=(
        "AI Orbit Knowledge Graph API "
        "for discovering and querying AI "
        "repositories, models, companies, "
        "tools, tasks, videos, devices, "
        "and relationships."
    ),
    version="1.1.0",
)


@app.get("/")
def root():
    return {
        "name": "AI Orbit",
        "status": "running",
        "version": "1.1.0",
        "description": "AI Knowledge Graph API",
        "endpoints": {
            "health": "/health",
            "stats": "/stats",
            "search": "/entities/search?q=Atlas",
            "analytics": "/graph/analytics",
            "docs": "/docs",
        },
    }


app.include_router(router)