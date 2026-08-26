from src.models import Entity


ENTITY_TYPES = {
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


def classify_entity(entity: Entity) -> Entity:
    """
    Classify an entity using deterministic rules.

    Existing explicit classifications are preserved when valid.
    """

    current_type = entity.entity_type.lower().strip()

    if current_type in ENTITY_TYPES:
        return entity

    text = " ".join(
        [
            entity.name or "",
            entity.description or "",
            " ".join(entity.categories or []),
        ]
    ).lower()

    if "github.com" in entity.url.lower():
        entity.entity_type = "repository"

    elif "mcp" in text:
        entity.entity_type = "mcp"

    elif "model" in text or "llm" in text:
        entity.entity_type = "model"

    elif "robot" in text or "robotics" in text:
        entity.entity_type = "robot"

    elif "device" in text or "hardware" in text:
        entity.entity_type = "device"

    elif "company" in text or "startup" in text:
        entity.entity_type = "company"

    elif "video" in text or "youtube" in entity.url.lower():
        entity.entity_type = "video"

    elif "task" in text:
        entity.entity_type = "task"

    else:
        entity.entity_type = "tool"

    return entity