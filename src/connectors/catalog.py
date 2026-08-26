import uuid

from src.models import Entity, Source


class CatalogConnector:

    SOURCE_NAME = "AI Orbit Catalog"
    SOURCE_URL = "https://ai-orbit.local/catalog"

    def __init__(self, records: list[dict] | None = None):
        self.records = records or []

    def get_records(self) -> list[dict]:
        return self.records

    def to_entity(self, record: dict) -> Entity:

        url = record["url"]

        entity_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                url,
            )
        )

        return Entity(
            id=entity_id,
            entity_type=record["entity_type"],
            name=record["name"],
            description=record["description"],
            url=url,
            categories=record.get("categories", []),
            source=Source(
                name=record.get(
                    "source_name",
                    self.SOURCE_NAME,
                ),
                url=record.get(
                    "source_url",
                    self.SOURCE_URL,
                ),
            ),
            metadata=record.get("metadata", {}),
        )