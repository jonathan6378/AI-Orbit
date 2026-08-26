from src.graph.graph import KnowledgeGraph
from src.graph.query import GraphQuery
from src.graph.service import GraphService
from src.models import Entity, Source
from src.relationships.relationship import Relationship


def make_entity(
    entity_id,
    entity_type,
    name,
    categories=None,
):
    return Entity(
        id=entity_id,
        entity_type=entity_type,
        name=name,
        description="Test entity",
        url=f"https://example.com/{entity_id}",
        categories=categories or [],
        source=Source(
            name="Test",
            url="https://example.com",
        ),
    )


def test_graph_entity_lookup():

    entity = make_entity(
        "device-1",
        "device",
        "Atlas",
        ["robotics"],
    )

    graph = KnowledgeGraph(
        [entity],
        [],
    )

    assert graph.get_entity(
        "device-1"
    ) == entity


def test_graph_relationship_navigation():

    company = make_entity(
        "company-1",
        "company",
        "Boston Dynamics",
    )

    device = make_entity(
        "device-1",
        "device",
        "Atlas",
    )

    relationship = Relationship(
        source_id="company-1",
        source_type="company",
        relationship_type="develops",
        target_id="device-1",
        target_type="device",
    )

    graph = KnowledgeGraph(
        [company, device],
        [relationship],
    )

    assert graph.get_outgoing(
        "company-1"
    )[0] == relationship

    assert graph.get_incoming(
        "device-1"
    )[0] == relationship


def test_graph_query_developed_entities():

    company = make_entity(
        "company-1",
        "company",
        "Boston Dynamics",
    )

    device = make_entity(
        "device-1",
        "device",
        "Atlas",
    )

    relationship = Relationship(
        source_id="company-1",
        source_type="company",
        relationship_type="develops",
        target_id="device-1",
        target_type="device",
    )

    graph = KnowledgeGraph(
        [company, device],
        [relationship],
    )

    query = GraphQuery(graph)

    results = query.developed_entities(
        "company-1"
    )

    assert len(results) == 1
    assert results[0].name == "Atlas"


def test_graph_category_search():

    device = make_entity(
        "device-1",
        "device",
        "Atlas",
        ["robotics", "humanoid"],
    )

    model = make_entity(
        "model-1",
        "model",
        "Test Model",
        ["machine-learning"],
    )

    graph = KnowledgeGraph(
        [device, model],
        [],
    )

    results = graph.search_category(
        "robotics"
    )

    assert len(results) == 1
    assert results[0].name == "Atlas"


def test_graph_query_find_by_name():

    device = make_entity(
        "device-1",
        "device",
        "Atlas",
    )

    graph = KnowledgeGraph(
        [device],
        [],
    )

    query = GraphQuery(graph)

    results = query.find_by_name(
        "atlas"
    )

    assert len(results) == 1
    assert results[0].name == "Atlas"


def test_graph_degree():

    company = make_entity(
        "company-1",
        "company",
        "Boston Dynamics",
    )

    device = make_entity(
        "device-1",
        "device",
        "Atlas",
    )

    relationship = Relationship(
        source_id="company-1",
        source_type="company",
        relationship_type="develops",
        target_id="device-1",
        target_type="device",
    )

    graph = KnowledgeGraph(
        [company, device],
        [relationship],
    )

    assert graph.degree(
        "company-1"
    ) == 1

    assert graph.degree(
        "device-1"
    ) == 1


def test_relationship_statistics():

    company = make_entity(
        "company-1",
        "company",
        "Boston Dynamics",
    )

    device = make_entity(
        "device-1",
        "device",
        "Atlas",
    )

    relationship = Relationship(
        source_id="company-1",
        source_type="company",
        relationship_type="develops",
        target_id="device-1",
        target_type="device",
    )

    graph = KnowledgeGraph(
        [company, device],
        [relationship],
    )

    statistics = (
        graph.relationship_statistics()
    )

    assert statistics["develops"] == 1


def test_most_connected():

    company = make_entity(
        "company-1",
        "company",
        "Boston Dynamics",
    )

    device_1 = make_entity(
        "device-1",
        "device",
        "Atlas",
    )

    device_2 = make_entity(
        "device-2",
        "device",
        "Spot",
    )

    relationship_1 = Relationship(
        source_id="company-1",
        source_type="company",
        relationship_type="develops",
        target_id="device-1",
        target_type="device",
    )

    relationship_2 = Relationship(
        source_id="company-1",
        source_type="company",
        relationship_type="develops",
        target_id="device-2",
        target_type="device",
    )

    graph = KnowledgeGraph(
        [
            company,
            device_1,
            device_2,
        ],
        [
            relationship_1,
            relationship_2,
        ],
    )

    results = graph.most_connected(
        limit=1
    )

    assert len(results) == 1
    assert results[0][0].name == "Boston Dynamics"
    assert results[0][1] == 2


def test_graph_service_search():

    service = GraphService()

    results = service.search(
        "Atlas"
    )

    assert len(results) >= 1

    assert any(
        entity.name == "Atlas"
        for entity in results
    )


def test_graph_service_category():

    service = GraphService()

    results = service.category(
        "robotics"
    )

    assert len(results) >= 1

    assert any(
        entity.name == "Atlas"
        for entity in results
    )


def test_graph_service_develops():

    service = GraphService()

    results = service.develops(
        "Boston Dynamics"
    )

    assert len(results) >= 1

    assert any(
        entity.name == "Atlas"
        for entity in results
    )


def test_graph_service_neighbors():

    service = GraphService()

    results = service.neighbors(
        "Atlas"
    )

    assert isinstance(
        results,
        list,
    )


def test_graph_service_analytics():

    service = GraphService()

    result = service.analytics()

    assert result["entities"] == 158
    assert result["relationships"] == 160

    assert (
        result["relationship_types"][
            "implements"
        ] == 124
    )

    assert (
        result["relationship_types"][
            "solves"
        ] == 24
    )

    assert (
        result["relationship_types"][
            "develops"
        ] == 12
    )

    assert len(
        result["most_connected"]
    ) > 0