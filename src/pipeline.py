from src.connectors.github import GitHubConnector
from src.connectors.huggingface import HuggingFaceConnector
from src.connectors.rss import RSSConnector
from src.connectors.catalog import CatalogConnector

from src.logger import logger

from src.processing.classifier import classify_entity
from src.processing.deduplicator import deduplicate_entities
from src.processing.entity_processor import process_entity

from src.validation.validator import validate_entities


class AIPipeline:

    def __init__(self):
        self.github = GitHubConnector()
        self.huggingface = HuggingFaceConnector()
        self.rss = RSSConnector()
        self.catalog = CatalogConnector()

    def process_entity(self, entity):
        """Run an entity through the common processing pipeline."""

        entity = process_entity(entity)
        entity = classify_entity(entity)

        return entity

    def collect_github_repositories(
        self,
        queries: list[str],
        per_query: int = 10,
    ):

        entities = []

        for query in queries:

            logger.info(
                "Starting GitHub collection for query: %s",
                query,
            )

            repositories = self.github.search_repositories(
                query=query,
                limit=per_query,
            )

            for repository in repositories:

                try:
                    entity = self.github.to_entity(repository)
                    entity = self.process_entity(entity)

                    entities.append(entity)

                except Exception as exc:

                    logger.error(
                        "Failed to process GitHub repository: %s",
                        exc,
                    )

        return entities

    def collect_huggingface_models(
        self,
        queries: list[str],
        per_query: int = 10,
    ):

        entities = []

        for query in queries:

            logger.info(
                "Starting Hugging Face collection for query: %s",
                query,
            )

            models = self.huggingface.search_models(
                query=query,
                limit=per_query,
            )

            for model in models:

                try:
                    model_id = model.get("id")

                    if not model_id:
                        continue

                    details = self.huggingface.get_model_details(
                        model_id
                    )

                    if details:
                        model.update(details)

                    entity = self.huggingface.to_entity(model)
                    entity = self.process_entity(entity)

                    entities.append(entity)

                except Exception as exc:

                    logger.error(
                        "Failed to process Hugging Face model: %s",
                        exc,
                    )

        return entities

    def collect_rss_news(
        self,
        feeds: list[dict],
        per_feed: int = 10,
    ):

        entities = []

        for feed in feeds:

            feed_url = feed["url"]
            source_name = feed["name"]
            source_url = feed["source_url"]

            logger.info(
                "Starting RSS collection for source: %s",
                source_name,
            )

            articles = self.rss.fetch_feed(
                feed_url=feed_url,
                source_name=source_name,
                limit=per_feed,
            )

            for article in articles:

                try:

                    entity = self.rss.to_entity(
                        article=article,
                        source_name=source_name,
                        source_url=source_url,
                    )

                    entity = self.process_entity(entity)

                    entities.append(entity)

                except Exception as exc:

                    logger.error(
                        "Failed to process RSS article: %s",
                        exc,
                    )

        return entities

    def collect_catalog_entities(
        self,
        records: list[dict],
    ):

        entities = []

        logger.info(
            "Starting catalog collection: %d records",
            len(records),
        )

        for record in records:

            try:

                entity = self.catalog.to_entity(record)

                entity = self.process_entity(entity)

                entities.append(entity)

            except Exception as exc:

                logger.error(
                    "Failed to process catalog entity: %s",
                    exc,
                )

        return entities

    def run(
        self,
        github_queries: list[str],
        huggingface_queries: list[str],
        rss_feeds: list[dict],
        catalog_records: list[dict],
        per_source: int = 10,
    ):

        github_entities = self.collect_github_repositories(
            github_queries,
            per_source,
        )

        huggingface_entities = self.collect_huggingface_models(
            huggingface_queries,
            per_source,
        )

        rss_entities = self.collect_rss_news(
            rss_feeds,
            per_source,
        )

        catalog_entities = self.collect_catalog_entities(
            catalog_records
        )

        all_entities = (
            github_entities
            + huggingface_entities
            + rss_entities
            + catalog_entities
        )

        logger.info(
            "Collected %d entities before deduplication",
            len(all_entities),
        )

        unique_entities = deduplicate_entities(
            all_entities
        )

        logger.info(
            "Remaining entities after deduplication: %d",
            len(unique_entities),
        )

        validation_result = validate_entities(
            unique_entities
        )

        logger.info(
            "Validation: %d valid, %d invalid",
            validation_result["valid_count"],
            validation_result["invalid_count"],
        )

        for invalid in validation_result["invalid"]:

            logger.warning(
                "Invalid entity: %s | Errors: %s",
                invalid["entity"].get("name"),
                invalid["errors"],
            )

        return validation_result["valid"]