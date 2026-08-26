from src.processing.deduplicator import deduplicate_entities


def make_entity(
    entity_type,
    name,
    url,
):
    from src.models import Entity, Source

    return Entity(
        id=f"{entity_type}-{name}",
        entity_type=entity_type,
        name=name,
        description="Test entity",
        url=url,
        categories=["ai"],
        source=Source(
            name="Test",
            url="https://example.com",
        ),
    )


def test_exact_deduplication():

    records = [
        make_entity(
            "model",
            "A",
            "https://example.com/a",
        ),
        make_entity(
            "model",
            "A duplicate",
            "https://example.com/a/",
        ),
    ]

    result = deduplicate_entities(records)

    assert len(result) == 1


def test_different_entity_types_same_url_are_not_duplicates():

    records = [
        make_entity(
            "company",
            "Figure AI",
            "https://www.figure.ai/",
        ),
        make_entity(
            "device",
            "Figure 02",
            "https://www.figure.ai",
        ),
    ]

    result = deduplicate_entities(records)

    assert len(result) == 2


def test_same_entity_type_normalized_url_is_duplicate():

    records = [
        make_entity(
            "device",
            "Atlas",
            "https://bostondynamics.com/atlas/",
        ),
        make_entity(
            "device",
            "Atlas Duplicate",
            "HTTPS://BOSTONDYNAMICS.COM/atlas",
        ),
    ]

    result = deduplicate_entities(records)

    assert len(result) == 1