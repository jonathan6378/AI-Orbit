from src.models import Entity, Source
from src.validation.validator import validate_entity


def test_valid_entity():

    entity = Entity(
        id="abc",
        entity_type="model",
        name="Example Model",
        description="Example AI model",
        url="https://example.com/model",
        categories=["ai"],
        source=Source(
            name="Example",
            url="https://example.com",
        ),
    )

    errors = validate_entity(entity)

    assert errors == []


def test_invalid_entity():

    entity = Entity(
        id="",
        entity_type="invalid",
        name="",
        description="",
        url="not-a-url",
        categories=[],
        source=Source(
            name="",
            url="bad",
        ),
    )

    errors = validate_entity(entity)

    assert "Missing required field: id" in errors
    assert "Missing required field: name" in errors
    assert "Invalid entity type: invalid" in errors
    assert "Invalid URL: not-a-url" in errors
    assert "Missing source name" in errors
    assert "Invalid source URL: bad" in errors