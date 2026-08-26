from src.models import Entity, Source
from src.relationships.relationship_engine import build_relationships


def make_source():
    return Source(
        name="Test",
        url="https://example.com",
    )


def test_repository_model_relationship():

    source = make_source()

    repository = Entity(
        id="repo-1",
        entity_type="repository",
        name="Test Repository",
        description="Machine learning repository",
        url="https://github.com/test/repo",
        categories=["machine-learning", "pytorch"],
        source=source,
    )

    model = Entity(
        id="model-1",
        entity_type="model",
        name="Test Model",
        description="Machine learning model",
        url="https://huggingface.co/test/model",
        categories=["model", "pytorch"],
        source=source,
    )

    relationships = build_relationships(
        [repository, model]
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source_id == "repo-1"
    assert relationship.target_id == "model-1"
    assert relationship.relationship_type == "implements"
    assert "pytorch" in relationship.metadata["matched_categories"]


def test_no_relationship_without_category_overlap():

    source = make_source()

    repository = Entity(
        id="repo-2",
        entity_type="repository",
        name="Vision Repository",
        description="Computer vision repository",
        url="https://github.com/test/vision",
        categories=["computer-vision"],
        source=source,
    )

    model = Entity(
        id="model-2",
        entity_type="model",
        name="Language Model",
        description="Language model",
        url="https://huggingface.co/test/language",
        categories=["natural-language-processing"],
        source=source,
    )

    relationships = build_relationships(
        [repository, model]
    )

    assert relationships == []


def test_company_develops_tool():

    company = Entity(
        id="company-1",
        entity_type="company",
        name="Anthropic",
        description="AI company",
        url="https://www.anthropic.com/",
        categories=["ai", "company"],
        source=Source(
            name="Anthropic",
            url="https://www.anthropic.com/",
        ),
    )

    tool = Entity(
        id="tool-1",
        entity_type="tool",
        name="Claude",
        description="AI assistant",
        url="https://www.anthropic.com/claude",
        categories=["ai", "tool"],
        source=Source(
            name="Anthropic",
            url="https://www.anthropic.com/",
        ),
    )

    relationships = build_relationships(
        [company, tool]
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source_id == "company-1"
    assert relationship.target_id == "tool-1"
    assert relationship.relationship_type == "develops"
    assert relationship.metadata["evidence"] == "source_match"


def test_company_develops_model():

    company = Entity(
        id="company-2",
        entity_type="company",
        name="Test AI",
        description="AI company",
        url="https://example.com/company",
        categories=["ai", "company"],
        source=Source(
            name="Test AI",
            url="https://example.com/company",
        ),
    )

    model = Entity(
        id="model-3",
        entity_type="model",
        name="Test Model",
        description="AI model",
        url="https://huggingface.co/test/model",
        categories=["ai", "model"],
        source=Source(
            name="Hugging Face",
            url="https://huggingface.co/",
        ),
        metadata={
            "provider": "Test AI",
        },
    )

    relationships = build_relationships(
        [company, model]
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source_id == "company-2"
    assert relationship.target_id == "model-3"
    assert relationship.relationship_type == "develops"
    assert relationship.metadata["evidence"] == (
        "provider_or_source_match"
    )


def test_tool_solves_task():

    tool = Entity(
        id="tool-1",
        entity_type="tool",
        name="Claude",
        description="AI assistant",
        url="https://www.anthropic.com/claude",
        categories=["ai", "tool"],
        source=Source(
            name="Anthropic",
            url="https://www.anthropic.com/",
        ),
    )

    task = Entity(
        id="task-1",
        entity_type="task",
        name="Text Generation",
        description="Generating natural language text.",
        url="https://huggingface.co/tasks/text-generation",
        categories=[
            "ai",
            "task",
            "text-generation",
        ],
        source=Source(
            name="Hugging Face",
            url="https://huggingface.co/",
        ),
    )

    relationships = build_relationships(
        [tool, task]
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source_id == "tool-1"
    assert relationship.target_id == "task-1"
    assert relationship.relationship_type == "solves"
    assert relationship.metadata["evidence"] == (
        "curated_capability_mapping"
    )


def test_company_develops_device():

    company = Entity(
        id="company-device-1",
        entity_type="company",
        name="Boston Dynamics",
        description="Robotics company",
        url="https://bostondynamics.com/",
        categories=[
            "ai",
            "robotics",
            "company",
        ],
        source=Source(
            name="Boston Dynamics",
            url="https://bostondynamics.com/",
        ),
    )

    device = Entity(
        id="device-1",
        entity_type="device",
        name="Atlas",
        description="Humanoid robot",
        url="https://bostondynamics.com/atlas/",
        categories=[
            "ai",
            "robotics",
            "device",
            "humanoid",
        ],
        source=Source(
            name="Boston Dynamics",
            url="https://bostondynamics.com/",
        ),
    )

    relationships = build_relationships(
        [company, device]
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source_id == "company-device-1"
    assert relationship.target_id == "device-1"
    assert relationship.relationship_type == "develops"
    assert relationship.metadata["evidence"] == "source_match"