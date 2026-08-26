import uuid

import feedparser

from src.logger import logger
from src.models import Entity, Source
from src.processing.cleaner import clean_text
from src.processing.normalizer import normalize_url


class RSSConnector:

    def fetch_feed(
        self,
        feed_url: str,
        source_name: str,
        limit: int = 10,
    ) -> list[dict]:

        try:
            feed = feedparser.parse(feed_url)

            if feed.bozo and not feed.entries:
                logger.warning(
                    "RSS feed could not be parsed: %s",
                    feed_url,
                )
                return []

            entries = feed.entries[:limit]

            logger.info(
                "RSS feed '%s' returned %d articles",
                source_name,
                len(entries),
            )

            return [
                {
                    "title": entry.get("title", ""),
                    "description": (
                        entry.get("summary")
                        or entry.get("description")
                        or ""
                    ),
                    "url": entry.get("link", ""),
                    "published": entry.get(
                        "published",
                        entry.get("updated", ""),
                    ),
                }
                for entry in entries
            ]

        except Exception as exc:
            logger.error(
                "RSS feed failed '%s': %s",
                feed_url,
                exc,
            )
            return []

    def to_entity(
        self,
        article: dict,
        source_name: str,
        source_url: str,
    ) -> Entity:

        title = clean_text(
            article.get("title")
        ) or "Untitled Article"

        description = clean_text(
            article.get("description")
        )

        url = normalize_url(
            article.get("url")
        )

        entity_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                url or f"{source_name}:{title}",
            )
        )

        metadata = {
            "published": article.get("published"),
        }

        return Entity(
            id=entity_id,
            entity_type="news",
            name=title,
            description=description,
            url=url,
            categories=["news", "ai"],
            source=Source(
                name=source_name,
                url=source_url,
            ),
            metadata=metadata,
        )