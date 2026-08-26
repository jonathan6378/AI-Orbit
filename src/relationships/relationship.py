from dataclasses import dataclass, field


@dataclass
class Relationship:
    source_id: str
    source_type: str
    relationship_type: str
    target_id: str
    target_type: str
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "source_type": self.source_type,
            "relationship_type": self.relationship_type,
            "target_id": self.target_id,
            "target_type": self.target_type,
            "metadata": self.metadata,
        }