from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert (
        data["service"]
        == "AI Orbit Graph API"
    )


def test_stats():

    response = client.get(
        "/stats"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["entities"] == 158
    assert data["relationships"] == 160

    assert (
        data["relationship_types"][
            "implements"
        ] == 124
    )

    assert (
        data["relationship_types"][
            "solves"
        ] == 24
    )

    assert (
        data["relationship_types"][
            "develops"
        ] == 12
    )


def test_entity_search():

    response = client.get(
        "/entities/search",
        params={"q": "Atlas"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["query"] == "Atlas"
    assert data["count"] >= 1

    assert any(
        entity["name"] == "Atlas"
        for entity in data["results"]
    )


def test_entity_search_no_results():

    response = client.get(
        "/entities/search",
        params={
            "q": "ThisEntityDoesNotExist"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 0
    assert data["results"] == []


def test_category_search():

    response = client.get(
        "/entities/category/robotics"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["category"] == "robotics"
    assert data["count"] >= 1

    assert any(
        entity["name"] == "Atlas"
        for entity in data["results"]
    )


def test_develops_endpoint():

    response = client.get(
        "/graph/develops/Boston%20Dynamics"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["entity"]
        == "Boston Dynamics"
    )

    assert (
        data["relationship"]
        == "develops"
    )

    assert data["count"] >= 1

    assert any(
        entity["name"] == "Atlas"
        for entity in data["results"]
    )


def test_implements_endpoint():

    response = client.get(
        "/graph/implements/Ai-Learn"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["entity"] == "Ai-Learn"
    assert (
        data["relationship"]
        == "implements"
    )

    assert data["count"] >= 1


def test_solves_endpoint():

    response = client.get(
        "/graph/solves/Gemini%20Robotics"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["entity"]
        == "Gemini Robotics"
    )

    assert (
        data["relationship"]
        == "solves"
    )

    assert data["count"] >= 0


def test_neighbors_endpoint():

    response = client.get(
        "/graph/neighbors/Atlas"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["entity"] == "Atlas"
    assert "count" in data
    assert "results" in data


def test_analytics_endpoint():

    response = client.get(
        "/graph/analytics"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["entities"] == 158
    assert data["relationships"] == 160

    assert (
        data["relationship_types"][
            "implements"
        ] == 124
    )

    assert (
        data["relationship_types"][
            "solves"
        ] == 24
    )

    assert (
        data["relationship_types"][
            "develops"
        ] == 12
    )

    assert len(
        data["most_connected"]
    ) > 0


# ============================================================
# 404 / ERROR HANDLING TESTS
# ============================================================


def test_develops_missing_entity():

    response = client.get(
        "/graph/develops/"
        "ThisEntityDoesNotExist"
    )

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data


def test_implements_missing_entity():

    response = client.get(
        "/graph/implements/"
        "ThisEntityDoesNotExist"
    )

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data


def test_solves_missing_entity():

    response = client.get(
        "/graph/solves/"
        "ThisEntityDoesNotExist"
    )

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data


def test_neighbors_missing_entity():

    response = client.get(
        "/graph/neighbors/"
        "ThisEntityDoesNotExist"
    )

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data