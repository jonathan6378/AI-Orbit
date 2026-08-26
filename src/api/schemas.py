from typing import Any

from pydantic import BaseModel, Field


class EntityResponse(BaseModel):
    id: str
    entity_type: str
    name: str
    description: str
    url: str
    categories: list[str] = Field(default_factory=list)
    source: dict[str, Any]
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class EntityListResponse(BaseModel):
    query: str | None = None
    category: str | None = None
    count: int
    results: list[EntityResponse]


class RelationshipTypeStats(BaseModel):
    implements: int = 0
    solves: int = 0
    develops: int = 0


class StatsResponse(BaseModel):
    entities: int
    relationships: int
    relationship_types: dict[str, int]


class AnalyticsEntity(BaseModel):
    name: str
    entity_type: str
    degree: int


class AnalyticsResponse(BaseModel):
    entities: int
    relationships: int
    relationship_types: dict[str, int]
    most_connected: list[AnalyticsEntity]


class RelationshipResponse(BaseModel):
    entity: str
    relationship: str
    count: int
    results: list[EntityResponse]


class NeighborResponse(BaseModel):
    entity: str
    count: int
    results: list[EntityResponse]


class HealthResponse(BaseModel):
    status: str
    service: str