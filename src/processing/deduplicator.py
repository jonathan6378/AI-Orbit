from src.models import Entity
from src.processing.normalizer import normalize_url


def deduplicate_entities(
    entities: list[Entity],
) -> list[Entity]:
    """
    Remove duplicate entities.

    Two entities are considered duplicates only when they have:

        1. The same entity type
        2. The same normalized URL

    This allows different entity types to legitimately share
    the same URL.

    Example:

        company + https://www.figure.ai
        device  + https://www.figure.ai

    are NOT duplicates.

    But:

        device + https://bostondynamics.com/atlas/
        device + https://bostondynamics.com/atlas

    ARE duplicates.
    """

    seen: set[tuple[str, str]] = set()
    unique_entities: list[Entity] = []

    for entity in entities:

        normalized_url = normalize_url(
            entity.url
        )

        key = (
            entity.entity_type.strip().lower(),
            normalized_url.strip().lower(),
        )

        if key in seen:
            continue

        seen.add(key)
        unique_entities.append(entity)

    return unique_entities