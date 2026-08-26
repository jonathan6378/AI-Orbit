from src.models import Entity
from src.processing.cleaner import clean_text, clean_categories
from src.processing.normalizer import normalize_name, normalize_url


def process_entity(entity: Entity) -> Entity:
    """
    Clean and normalize an Entity before deduplication
    and final validation.
    """

    entity.name = normalize_name(entity.name)
    entity.description = clean_text(entity.description)
    entity.url = normalize_url(entity.url)
    entity.categories = clean_categories(entity.categories)

    entity.source.name = normalize_name(entity.source.name)
    entity.source.url = normalize_url(entity.source.url)

    return entity