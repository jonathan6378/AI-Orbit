from src.models import Entity
from src.relationships.relationship import Relationship


def _shared_categories(
    first: Entity,
    second: Entity,
) -> set[str]:
    """Return categories shared by two entities."""

    return (
        set(first.categories)
        & set(second.categories)
    )


def build_relationships(
    entities: list[Entity],
) -> list[Relationship]:
    """
    Build deterministic relationships from entity metadata.

    Supported relationships:

    Repository → implements → Model
    Company → develops → Tool
    Company → develops → Model
    Company → develops → Device
    Tool → solves → Task
    """

    relationships = []

    # ---------------------------------------------------------
    # Separate entities by type
    # ---------------------------------------------------------

    repositories = [
        entity
        for entity in entities
        if entity.entity_type == "repository"
    ]

    models = [
        entity
        for entity in entities
        if entity.entity_type == "model"
    ]

    tools = [
        entity
        for entity in entities
        if entity.entity_type == "tool"
    ]

    companies = [
        entity
        for entity in entities
        if entity.entity_type == "company"
    ]

    tasks = [
        entity
        for entity in entities
        if entity.entity_type == "task"
    ]

    devices = [
        entity
        for entity in entities
        if entity.entity_type == "device"
    ]

    # ---------------------------------------------------------
    # Repository → implements → Model
    # ---------------------------------------------------------

    for repository in repositories:

        for model in models:

            overlap = _shared_categories(
                repository,
                model,
            )

            if overlap:

                relationships.append(
                    Relationship(
                        source_id=repository.id,
                        source_type=repository.entity_type,
                        relationship_type="implements",
                        target_id=model.id,
                        target_type=model.entity_type,
                        metadata={
                            "matched_categories": sorted(
                                overlap
                            ),
                        },
                    )
                )

    # ---------------------------------------------------------
    # Company → develops → Tool
    # ---------------------------------------------------------

    for company in companies:

        company_name = company.name.lower()

        for tool in tools:

            tool_source = tool.source.name.lower()

            if company_name in tool_source:

                relationships.append(
                    Relationship(
                        source_id=company.id,
                        source_type=company.entity_type,
                        relationship_type="develops",
                        target_id=tool.id,
                        target_type=tool.entity_type,
                        metadata={
                            "evidence": "source_match",
                        },
                    )
                )

    # ---------------------------------------------------------
    # Company → develops → Model
    # ---------------------------------------------------------

    for company in companies:

        company_name = company.name.lower()

        for model in models:

            provider = str(
                model.metadata.get(
                    "provider",
                    "",
                )
            ).lower()

            source_name = model.source.name.lower()

            if (
                company_name in provider
                or company_name in source_name
            ):

                relationships.append(
                    Relationship(
                        source_id=company.id,
                        source_type=company.entity_type,
                        relationship_type="develops",
                        target_id=model.id,
                        target_type=model.entity_type,
                        metadata={
                            "evidence": (
                                "provider_or_source_match"
                            ),
                        },
                    )
                )

    # ---------------------------------------------------------
    # Company → develops → Device
    # ---------------------------------------------------------

    for company in companies:

        company_name = company.name.lower()

        for device in devices:

            device_source = device.source.name.lower()

            if company_name in device_source:

                relationships.append(
                    Relationship(
                        source_id=company.id,
                        source_type=company.entity_type,
                        relationship_type="develops",
                        target_id=device.id,
                        target_type=device.entity_type,
                        metadata={
                            "evidence": "source_match",
                        },
                    )
                )

    # ---------------------------------------------------------
    # Tool → solves → Task
    # ---------------------------------------------------------

    tool_task_map = {
        "claude": {
            "text generation",
            "question answering",
            "summarization",
            "translation",
        },

        "gemini": {
            "text generation",
            "image generation",
            "question answering",
            "summarization",
            "translation",
        },

        "google ai studio": {
            "text generation",
            "question answering",
            "summarization",
        },

        "google flow": {
            "image generation",
        },

        "gemini api": {
            "text generation",
            "question answering",
            "summarization",
            "translation",
        },

        "google antigravity": {
            "text generation",
        },

        "gemini robotics": {
            "image classification",
            "object detection",
        },

        "replicate": {
            "text generation",
            "image generation",
            "text classification",
            "speech recognition",
            "computer vision",
        },
    }

    task_lookup = {
        task.name.lower(): task
        for task in tasks
    }

    for tool in tools:

        supported_tasks = tool_task_map.get(
            tool.name.lower(),
            set(),
        )

        for task_name in supported_tasks:

            task = task_lookup.get(task_name)

            if task is None:
                continue

            relationships.append(
                Relationship(
                    source_id=tool.id,
                    source_type=tool.entity_type,
                    relationship_type="solves",
                    target_id=task.id,
                    target_type=task.entity_type,
                    metadata={
                        "evidence": (
                            "curated_capability_mapping"
                        ),
                    },
                )
            )

    return relationships