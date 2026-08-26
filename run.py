import json
from pathlib import Path

from src.config import ENTITIES_FILE
from src.logger import logger
from src.pipeline import AIPipeline
from src.processing.writer import write_entities
from src.relationships.relationship_engine import build_relationships
from src.relationships.writer import write_relationships


RELATIONSHIPS_FILE = Path("data/relationships.json")

CATALOG_FILE = Path("data/catalog.json")
TASKS_FILE = Path("data/tasks.json")
VIDEOS_FILE = Path("data/videos.json")
DEVICES_FILE = Path("data/devices.json")


def main():

    logger.info("====================================")
    logger.info("AI Orbit Data Ingestion Pipeline")
    logger.info("====================================")

    pipeline = AIPipeline()

    # ---------------------------------------------------------
    # GitHub queries
    # ---------------------------------------------------------

    github_queries = [
        "artificial intelligence",
        "machine learning",
        "generative AI",
        "large language model",
        "AI agents",
    ]

    # ---------------------------------------------------------
    # Hugging Face queries
    # ---------------------------------------------------------

    huggingface_queries = [
        "text generation",
        "image generation",
        "text classification",
        "speech recognition",
        "computer vision",
    ]

    # ---------------------------------------------------------
    # RSS feeds
    # ---------------------------------------------------------

    rss_feeds = [
        {
            "name": "MIT Technology Review",
            "url": "https://www.technologyreview.com/feed/",
            "source_url": "https://www.technologyreview.com/",
        },
    ]

    # ---------------------------------------------------------
    # Load catalog records
    # ---------------------------------------------------------

    with CATALOG_FILE.open(
        "r",
        encoding="utf-8",
    ) as f:

        catalog_records = json.load(f)

    logger.info(
        "Loaded %d catalog records",
        len(catalog_records),
    )

    # ---------------------------------------------------------
    # Load task records
    # ---------------------------------------------------------

    with TASKS_FILE.open(
        "r",
        encoding="utf-8",
    ) as f:

        task_records = json.load(f)

    logger.info(
        "Loaded %d task records",
        len(task_records),
    )

    catalog_records.extend(task_records)

    # ---------------------------------------------------------
    # Load video records
    # ---------------------------------------------------------

    with VIDEOS_FILE.open(
        "r",
        encoding="utf-8",
    ) as f:

        video_records = json.load(f)

    logger.info(
        "Loaded %d video records",
        len(video_records),
    )

    catalog_records.extend(video_records)

    # ---------------------------------------------------------
    # Load device / robot records
    # ---------------------------------------------------------

    with DEVICES_FILE.open(
        "r",
        encoding="utf-8",
    ) as f:

        device_records = json.load(f)

    logger.info(
        "Loaded %d device records",
        len(device_records),
    )

    catalog_records.extend(device_records)

    # ---------------------------------------------------------
    # Final curated record count
    # ---------------------------------------------------------

    logger.info(
        "Loaded %d catalog/task/video/device records",
        len(catalog_records),
    )

    # ---------------------------------------------------------
    # Run ingestion pipeline
    # ---------------------------------------------------------

    entities = pipeline.run(
        github_queries=github_queries,
        huggingface_queries=huggingface_queries,
        rss_feeds=rss_feeds,
        catalog_records=catalog_records,
        per_source=10,
    )

    # ---------------------------------------------------------
    # Write entities
    # ---------------------------------------------------------

    write_entities(
        entities,
        ENTITIES_FILE,
    )

    logger.info(
        "Successfully wrote %d entities to %s",
        len(entities),
        ENTITIES_FILE,
    )

    # ---------------------------------------------------------
    # Build relationships
    # ---------------------------------------------------------

    relationships = build_relationships(
        entities
    )

    logger.info(
        "Generated %d relationships",
        len(relationships),
    )

    # ---------------------------------------------------------
    # Write relationships
    # ---------------------------------------------------------

    write_relationships(
        relationships,
        RELATIONSHIPS_FILE,
    )

    logger.info(
        "Successfully wrote %d relationships to %s",
        len(relationships),
        RELATIONSHIPS_FILE,
    )


if __name__ == "__main__":
    main()