import requests
import uuid

from src.config import GITHUB_TOKEN
from src.logger import logger
from src.models import Entity, Source


GITHUB_API_URL = "https://api.github.com"


class GitHubConnector:

    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        if GITHUB_TOKEN:
            self.headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    def search_repositories(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict]:

        url = f"{GITHUB_API_URL}/search/repositories"

        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": min(limit, 100),
        }

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=20,
            )

            response.raise_for_status()

            data = response.json()
            repositories = data.get("items", [])

            logger.info(
                "GitHub search '%s' returned %d repositories",
                query,
                len(repositories),
            )

            return repositories

        except requests.RequestException as exc:
            logger.error(
                "GitHub request failed: %s",
                exc,
            )
            return []

    def to_entity(self, repository: dict) -> Entity:
        """
        Convert a raw GitHub repository response
        into the common AI Orbit Entity format.
        """

        name = repository.get("name") or "Unknown Repository"

        description = repository.get("description") or ""

        url = repository.get("html_url") or ""

        topics = repository.get("topics") or []

        categories = ["repository"]

        if topics:
            categories.extend(topics)

        metadata = {
            "stars": repository.get("stargazers_count", 0),
            "primary_language": repository.get("language"),
            "last_updated": repository.get("updated_at"),
            "forks": repository.get("forks_count", 0),
            "open_issues": repository.get("open_issues_count", 0),
            "license": (
                repository.get("license", {}).get("spdx_id")
                if repository.get("license")
                else None
            ),
        }

        entity_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                url or f"github:{repository.get('full_name', name)}",
            )
        )

        return Entity(
            id=entity_id,
            entity_type="repository",
            name=name,
            description=description,
            url=url,
            categories=categories,
            source=Source(
                name="GitHub",
                url="https://github.com",
            ),
            metadata=metadata,
        )