from src.graph.loader import load_graph
from src.graph.query import GraphQuery


class GraphService:
    """
    High-level service interface for the AI Orbit knowledge graph.

    This class hides graph loading and low-level traversal logic
    from applications using the knowledge graph.
    """

    def __init__(
        self,
        entities_path="data/entities.json",
        relationships_path="data/relationships.json",
    ):
        self.graph = load_graph(
            entities_path=entities_path,
            relationships_path=relationships_path,
        )

        self.query = GraphQuery(
            self.graph
        )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(self, name: str):

        return self.query.find_by_name(
            name
        )

    # ---------------------------------------------------------
    # Category
    # ---------------------------------------------------------

    def category(self, category: str):

        return self.query.find_by_category(
            category
        )

    # ---------------------------------------------------------
    # Develops
    # ---------------------------------------------------------

    def develops(self, name: str):

        matches = self.query.find_by_name(
            name
        )

        results = []

        for entity in matches:

            results.extend(
                self.query.developed_entities(
                    entity.id
                )
            )

        return results

    # ---------------------------------------------------------
    # Implements
    # ---------------------------------------------------------

    def implements(self, name: str):

        matches = self.query.find_by_name(
            name
        )

        results = []

        for entity in matches:

            results.extend(
                self.query.implemented_models(
                    entity.id
                )
            )

        return results

    # ---------------------------------------------------------
    # Solves
    # ---------------------------------------------------------

    def solves(self, name: str):

        matches = self.query.find_by_name(
            name
        )

        results = []

        for entity in matches:

            results.extend(
                self.query.solved_tasks(
                    entity.id
                )
            )

        return results

    # ---------------------------------------------------------
    # Neighbors
    # ---------------------------------------------------------

    def neighbors(self, name: str):

        matches = self.query.find_by_name(
            name
        )

        results = []

        for entity in matches:

            results.extend(
                self.graph.get_neighbors(
                    entity.id
                )
            )

        return results

    # ---------------------------------------------------------
    # Analytics
    # ---------------------------------------------------------

    def analytics(self):

        return {
            "entities": len(
                self.graph.entities
            ),
            "relationships": len(
                self.graph.relationships
            ),
            "relationship_types":
                self.graph.relationship_statistics(),
            "most_connected":
                [
                    {
                        "name": entity.name,
                        "entity_type":
                            entity.entity_type,
                        "degree": degree,
                    }
                    for entity, degree
                    in self.graph.most_connected(
                        10
                    )
                ],
        }