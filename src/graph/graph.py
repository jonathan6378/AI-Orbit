from collections import defaultdict

from src.models import Entity
from src.relationships.relationship import Relationship


class KnowledgeGraph:
    """
    In-memory representation of the AI Orbit knowledge graph.

    Stores:
        - entities
        - relationships
        - outgoing relationships
        - incoming relationships
    """

    def __init__(
        self,
        entities: list[Entity],
        relationships: list[Relationship],
    ):
        self.entities = entities
        self.relationships = relationships

        # -----------------------------------------------------
        # Entity index
        # -----------------------------------------------------

        self.entity_index = {
            entity.id: entity
            for entity in entities
        }

        # -----------------------------------------------------
        # Relationship indexes
        # -----------------------------------------------------

        self.outgoing = defaultdict(list)
        self.incoming = defaultdict(list)

        for relationship in relationships:

            self.outgoing[
                relationship.source_id
            ].append(relationship)

            self.incoming[
                relationship.target_id
            ].append(relationship)

    # ---------------------------------------------------------
    # Entity lookup
    # ---------------------------------------------------------

    def get_entity(
        self,
        entity_id: str,
    ):
        """Return an entity by ID."""

        return self.entity_index.get(
            entity_id
        )

    # ---------------------------------------------------------
    # Outgoing relationships
    # ---------------------------------------------------------

    def get_outgoing(
        self,
        entity_id: str,
        relationship_type: str | None = None,
    ):
        """Return relationships leaving an entity."""

        relationships = self.outgoing.get(
            entity_id,
            [],
        )

        if relationship_type is None:
            return relationships

        return [
            relationship
            for relationship in relationships
            if relationship.relationship_type
            == relationship_type
        ]

    # ---------------------------------------------------------
    # Incoming relationships
    # ---------------------------------------------------------

    def get_incoming(
        self,
        entity_id: str,
        relationship_type: str | None = None,
    ):
        """Return relationships entering an entity."""

        relationships = self.incoming.get(
            entity_id,
            [],
        )

        if relationship_type is None:
            return relationships

        return [
            relationship
            for relationship in relationships
            if relationship.relationship_type
            == relationship_type
        ]

    # ---------------------------------------------------------
    # Neighbours
    # ---------------------------------------------------------

    def get_neighbors(
        self,
        entity_id: str,
    ):
        """
        Return entities connected to the given entity.

        Both incoming and outgoing relationships are considered.
        """

        neighbors = []

        for relationship in self.outgoing.get(
            entity_id,
            [],
        ):

            entity = self.get_entity(
                relationship.target_id
            )

            if entity:
                neighbors.append(entity)

        for relationship in self.incoming.get(
            entity_id,
            [],
        ):

            entity = self.get_entity(
                relationship.source_id
            )

            if entity:
                neighbors.append(entity)

        return neighbors

    # ---------------------------------------------------------
    # Entity type search
    # ---------------------------------------------------------

    def get_by_type(
        self,
        entity_type: str,
    ):
        """Return all entities of a given type."""

        entity_type = entity_type.lower()

        return [
            entity
            for entity in self.entities
            if entity.entity_type.lower()
            == entity_type
        ]

    # ---------------------------------------------------------
    # Category search
    # ---------------------------------------------------------

    def search_category(
        self,
        category: str,
    ):
        """Return entities containing a category."""

        category = category.lower()

        return [
            entity
            for entity in self.entities
            if any(
                category == item.lower()
                for item in entity.categories
            )
        ]

    # ---------------------------------------------------------
    # Degree
    # ---------------------------------------------------------

    def degree(
        self,
        entity_id: str,
    ) -> int:
        """
        Return total incoming + outgoing relationships
        for an entity.
        """

        return (
            len(
                self.outgoing.get(
                    entity_id,
                    [],
                )
            )
            + len(
                self.incoming.get(
                    entity_id,
                    [],
                )
            )
        )

    # ---------------------------------------------------------
    # Most connected entities
    # ---------------------------------------------------------

    def most_connected(
        self,
        limit: int = 10,
    ):
        """
        Return entities ordered by total graph connectivity.

        Result format:

            [
                (Entity, degree),
                ...
            ]
        """

        ranked = [
            (
                entity,
                self.degree(entity.id),
            )
            for entity in self.entities
        ]

        ranked.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return ranked[:limit]

    # ---------------------------------------------------------
    # Relationship statistics
    # ---------------------------------------------------------

    def relationship_statistics(self):
        """
        Return relationship counts grouped by type.

        Example:

            {
                "implements": 124,
                "solves": 24,
                "develops": 12
            }
        """

        statistics = {}

        for relationship in self.relationships:

            relationship_type = (
                relationship.relationship_type
            )

            statistics[relationship_type] = (
                statistics.get(
                    relationship_type,
                    0,
                )
                + 1
            )

        return statistics