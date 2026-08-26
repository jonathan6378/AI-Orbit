import requests
import uuid

from src.config import HUGGINGFACE_TOKEN
from src.logger import logger
from src.models import Entity, Source


HUGGINGFACE_API_URL = "https://huggingface.co/api/models"


class HuggingFaceConnector:

    def __init__(self):
        self.headers = {
            "Accept": "application/json",
        }

        if HUGGINGFACE_TOKEN:
            self.headers["Authorization"] = (
                f"Bearer {HUGGINGFACE_TOKEN}"
            )

    def search_models(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict]:

        params = {
            "search": query,
            "limit": min(limit, 100),
        }

        try:
            response = requests.get(
                HUGGINGFACE_API_URL,
                headers=self.headers,
                params=params,
                timeout=20,
            )

            response.raise_for_status()

            models = response.json()

            logger.info(
                "Hugging Face search '%s' returned %d models",
                query,
                len(models),
            )

            return models

        except requests.RequestException as exc:
            logger.error(
                "Hugging Face request failed: %s",
                exc,
            )
            return []

    def get_model_details(self, model_id: str) -> dict:
        """Fetch detailed metadata for a specific model."""

        url = f"{HUGGINGFACE_API_URL}/{model_id}"

        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=20,
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as exc:
            logger.warning(
                "Could not fetch details for model '%s': %s",
                model_id,
                exc,
            )
            return {}

    def to_entity(self, model: dict) -> Entity:

        model_id = model.get("id") or "unknown-model"

        pipeline_tag = model.get("pipeline_tag")
        tags = model.get("tags") or []

        categories = ["model"]

        if pipeline_tag:
            categories.append(pipeline_tag)

        categories.extend(tags[:10])

        url = f"https://huggingface.co/{model_id}"

        metadata = {
            "license": model.get("license"),
         "modalities": [],
            "provider": (
                model_id.split("/")[0]
                if "/" in model_id
                else None
            ),
            "downloads": model.get("downloads"),
            "likes": model.get("likes"),
            "pipeline_tag": pipeline_tag,
        }

        entity_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                url,
            )
        )

        return Entity(
            id=entity_id,
            entity_type="model",
            name=model_id,
            description=(
                model.get("description")
                or f"Hugging Face model: {model_id}"
            ),
            url=url,
            categories=categories,
            source=Source(
                name="Hugging Face",
                url="https://huggingface.co",
            ),
            metadata=metadata,
        )