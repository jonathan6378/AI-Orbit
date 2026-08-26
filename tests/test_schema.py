from src.models import Entity, Source


def test_required_schema():

    entity = Entity(
        id="abc",
        entity_type="model",
        name="Example",
        description="Example AI model",
        url="https://example.com",
        categories=["ai"],
        source=Source(
            name="Example Source",
            url="https://example.com/source",
        ),
    )

    assert entity.entity_type == "model"
    assert entity.categories == ["ai"]
    assert entity.name == "Example"
    assert entity.url == "https://example.com"
