import json
from pathlib import Path

from src.graph.graph import KnowledgeGraph
from src.models import Entity, Source
from src.relationships.relationship import Relationship


def load_entities(
    path: str | Path,
) -> list[Entity]:

    path = Path(path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        records = json.load(file)

    entities = []

    for record in records:

        source_data = record["source"]

        source = Source(
            name=source_data["name"],
            url=source_data["url"],
        )

        entity = Entity(
            id=record["id"],
            entity_type=record["entity_type"],
            name=record["name"],
            description=record["description"],
            url=record["url"],
            categories=record.get(
                "categories",
                [],
            ),
            source=source,
            metadata=record.get(
                "metadata",
                {},
            ),
        )

        entities.append(entity)

    return entities


def load_relationships(
    path: str | Path,
) -> list[Relationship]:

    path = Path(path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        records = json.load(file)

    relationships = []

    for record in records:

        relationship = Relationship(
            source_id=record["source_id"],
            source_type=record["source_type"],
            relationship_type=record[
                "relationship_type"
            ],
            target_id=record["target_id"],
            target_type=record["target_type"],
            metadata=record.get(
                "metadata",
                {},
            ),
        )

        relationships.append(
            relationship
        )

    return relationships


def load_graph(
    entities_path: str | Path = "data/entities.json",
    relationships_path: str | Path = "data/relationships.json",
) -> KnowledgeGraph:

    entities = load_entities(
        entities_path
    )

    relationships = load_relationships(
        relationships_path
    )

    return KnowledgeGraph(
        entities=entities,
        relationships=relationships,
    )