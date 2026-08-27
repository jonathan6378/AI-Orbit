
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router


app = FastAPI(
    title="AI Orbit Graph API",
    description=(
        "AI Orbit Knowledge Graph API for discovering "
        "and querying AI repositories, models, companies, "
        "tools, tasks, videos, devices, and relationships."
    ),
    version="1.1.0",
)

# ---------------------------------------------------------
# CORS
# Allows the React/Vite frontend to communicate with
# the FastAPI backend.
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# API routes
# ---------------------------------------------------------

app.include_router(router)