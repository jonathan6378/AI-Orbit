import json
from pathlib import Path

from src.models import Entity


def write_entities(
    entities: list[Entity],
    output_file: Path,
) -> None:
    """Write entities to a JSON file."""

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = [
        entity.to_dict()
        for entity in entities
    ]

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )