from urllib.parse import urlparse

from src.models import Entity


VALID_ENTITY_TYPES = {
    "repository",
    "tool",
    "task",
    "company",
    "news",
    "video",
    "robot",
    "device",
    "model",
    "mcp",
    "collection",
    "personal",
    "creative",
}


REQUIRED_FIELDS = {
    "id",
    "entity_type",
    "name",
    "url",
    "source",
}


def validate_url(url: str) -> bool:
    """Return True when the URL has a valid HTTP/HTTPS structure."""

    if not url:
        return False

    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.netloc)
        )

    except Exception:
        return False


def validate_entity(entity: Entity) -> list[str]:
    """
    Validate one Entity.

    Returns a list of validation errors.
    An empty list means the entity passed validation.
    """

    errors = []

    data = entity.to_dict()

    # Required fields
    for field in REQUIRED_FIELDS:
        value = data.get(field)

        if value is None or value == "":
            errors.append(
                f"Missing required field: {field}"
            )

    # Entity type
    if entity.entity_type not in VALID_ENTITY_TYPES:
        errors.append(
            f"Invalid entity type: {entity.entity_type}"
        )

    # URL
    if entity.url and not validate_url(entity.url):
        errors.append(
            f"Invalid URL: {entity.url}"
        )

    # Source validation
    if entity.source is None:
        errors.append("Missing source")

    else:
        if not entity.source.name:
            errors.append("Missing source name")

        if entity.source.url and not validate_url(
            entity.source.url
        ):
            errors.append(
                f"Invalid source URL: {entity.source.url}"
            )

    return errors


def validate_entities(
    entities: list[Entity],
) -> dict:

    valid = []
    invalid = []

    for entity in entities:

        errors = validate_entity(entity)

        if errors:
            invalid.append(
                {
                    "entity": entity.to_dict(),
                    "errors": errors,
                }
            )
        else:
            valid.append(entity)

    return {
        "valid": valid,
        "invalid": invalid,
        "total": len(entities),
        "valid_count": len(valid),
        "invalid_count": len(invalid),
    }