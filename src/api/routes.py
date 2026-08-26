from fastapi import APIRouter, HTTPException, Query

from src.api.schemas import (
    AnalyticsResponse,
    EntityListResponse,
    HealthResponse,
    NeighborResponse,
    RelationshipResponse,
    StatsResponse,
)
from src.graph.service import GraphService


router = APIRouter()

service = GraphService()


@router.get(
    "/health",
    response_model=HealthResponse,
)
def health():

    return {
        "status": "ok",
        "service": "AI Orbit Graph API",
    }


@router.get(
    "/stats",
    response_model=StatsResponse,
)
def stats():

    analytics = service.analytics()

    return {
        "entities": analytics["entities"],
        "relationships": analytics[
            "relationships"
        ],
        "relationship_types": analytics[
            "relationship_types"
        ],
    }


@router.get(
    "/entities/search",
    response_model=EntityListResponse,
)
def search_entities(
    q: str = Query(
        ...,
        min_length=1,
    ),
):

    results = service.search(q)

    return {
        "query": q,
        "count": len(results),
        "results": [
            entity.to_dict()
            for entity in results
        ],
    }


@router.get(
    "/entities/category/{category}",
    response_model=EntityListResponse,
)
def category_entities(
    category: str,
):

    results = service.category(category)

    return {
        "category": category,
        "count": len(results),
        "results": [
            entity.to_dict()
            for entity in results
        ],
    }


@router.get(
    "/graph/develops/{name}",
    response_model=RelationshipResponse,
)
def develops(name: str):

    matches = service.search(name)

    if not matches:
        raise HTTPException(
            status_code=404,
            detail=f"Entity not found: {name}",
        )

    results = service.develops(name)

    return {
        "entity": name,
        "relationship": "develops",
        "count": len(results),
        "results": [
            entity.to_dict()
            for entity in results
        ],
    }


@router.get(
    "/graph/implements/{name}",
    response_model=RelationshipResponse,
)
def implements(name: str):

    matches = service.search(name)

    if not matches:
        raise HTTPException(
            status_code=404,
            detail=f"Entity not found: {name}",
        )

    results = service.implements(name)

    return {
        "entity": name,
        "relationship": "implements",
        "count": len(results),
        "results": [
            entity.to_dict()
            for entity in results
        ],
    }


@router.get(
    "/graph/solves/{name}",
    response_model=RelationshipResponse,
)
def solves(name: str):

    matches = service.search(name)

    if not matches:
        raise HTTPException(
            status_code=404,
            detail=f"Entity not found: {name}",
        )

    results = service.solves(name)

    return {
        "entity": name,
        "relationship": "solves",
        "count": len(results),
        "results": [
            entity.to_dict()
            for entity in results
        ],
    }


@router.get(
    "/graph/neighbors/{name}",
    response_model=NeighborResponse,
)
def neighbors(name: str):

    matches = service.search(name)

    if not matches:
        raise HTTPException(
            status_code=404,
            detail=f"Entity not found: {name}",
        )

    results = service.neighbors(name)

    return {
        "entity": name,
        "count": len(results),
        "results": [
            entity.to_dict()
            for entity in results
        ],
    }


@router.get(
    "/graph/analytics",
    response_model=AnalyticsResponse,
)
def analytics():

    return service.analytics()