import json
from pathlib import Path

from src.relationships.relationship import Relationship


def write_relationships(
    relationships: list[Relationship],
    output_path: Path,
) -> None:
    """Write relationships to a UTF-8 JSON file."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = [
        relationship.to_dict()
        for relationship in relationships
    ]

    output_path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )