from dataclasses import dataclass, field
from typing import Any


@dataclass
class Source:
    name: str
    url: str


@dataclass
class Entity:
    id: str
    entity_type: str
    name: str
    description: str
    url: str
    categories: list[str]
    source: Source
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "entity_type": self.entity_type,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "categories": self.categories,
            "source": {
                "name": self.source.name,
                "url": self.source.url,
            },
            "metadata": self.metadata,
        }