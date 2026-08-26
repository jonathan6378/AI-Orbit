from src.graph.graph import KnowledgeGraph


class GraphQuery:
    """
    High-level query interface for the AI Orbit knowledge graph.
    """

    def __init__(
        self,
        graph: KnowledgeGraph,
    ):
        self.graph = graph

    # ---------------------------------------------------------
    # Find entities by name
    # ---------------------------------------------------------

    def find_by_name(
        self,
        name: str,
    ):

        name = name.lower()

        return [
            entity
            for entity in self.graph.entities
            if name in entity.name.lower()
        ]

    # ---------------------------------------------------------
    # Find entities by type
    # ---------------------------------------------------------

    def find_by_type(
        self,
        entity_type: str,
    ):

        return self.graph.get_by_type(
            entity_type
        )

    # ---------------------------------------------------------
    # Find entities by category
    # ---------------------------------------------------------

    def find_by_category(
        self,
        category: str,
    ):

        return self.graph.search_category(
            category
        )

    # ---------------------------------------------------------
    # What does an entity develop?
    # ---------------------------------------------------------

    def developed_by(
        self,
        entity_id: str,
    ):

        relationships = self.graph.get_incoming(
            entity_id,
            "develops",
        )

        return [
            self.graph.get_entity(
                relationship.source_id
            )
            for relationship in relationships
            if self.graph.get_entity(
                relationship.source_id
            )
        ]

    # ---------------------------------------------------------
    # What does a company develop?
    # ---------------------------------------------------------

    def developed_entities(
        self,
        entity_id: str,
    ):

        relationships = self.graph.get_outgoing(
            entity_id,
            "develops",
        )

        return [
            self.graph.get_entity(
                relationship.target_id
            )
            for relationship in relationships
            if self.graph.get_entity(
                relationship.target_id
            )
        ]

    # ---------------------------------------------------------
    # What models does a repository implement?
    # ---------------------------------------------------------

    def implemented_models(
        self,
        repository_id: str,
    ):

        relationships = self.graph.get_outgoing(
            repository_id,
            "implements",
        )

        return [
            self.graph.get_entity(
                relationship.target_id
            )
            for relationship in relationships
            if self.graph.get_entity(
                relationship.target_id
            )
        ]

    # ---------------------------------------------------------
    # What tasks can a tool solve?
    # ---------------------------------------------------------

    def solved_tasks(
        self,
        tool_id: str,
    ):

        relationships = self.graph.get_outgoing(
            tool_id,
            "solves",
        )

        return [
            self.graph.get_entity(
                relationship.target_id
            )
            for relationship in relationships
            if self.graph.get_entity(
                relationship.target_id
            )
        ]