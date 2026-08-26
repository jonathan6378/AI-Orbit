from src.graph.loader import load_graph
from src.graph.query import GraphQuery


def print_entities(entities):
    if not entities:
        print("No entities found.")
        return

    for entity in entities:
        print(
            f"{entity.entity_type}: "
            f"{entity.name}"
        )


def main():

    graph = load_graph()
    query = GraphQuery(graph)

    print("====================================")
    print("AI Orbit Knowledge Graph")
    print("====================================")
    print(f"Entities: {len(graph.entities)}")
    print(
        f"Relationships: "
        f"{len(graph.relationships)}"
    )

    while True:

        command = input(
            "\nAI Orbit > "
        ).strip()

        if not command:
            continue

        lower = command.lower()

        # -----------------------------------------------------
        # Exit
        # -----------------------------------------------------

        if lower in {"exit", "quit"}:
            break

        # -----------------------------------------------------
        # Stats
        # -----------------------------------------------------

        if lower == "stats":

            print(
                f"Entities: {len(graph.entities)}"
            )

            print(
                f"Relationships: "
                f"{len(graph.relationships)}"
            )

            continue

        # -----------------------------------------------------
        # Analytics
        # -----------------------------------------------------

        if lower == "analytics":

            print("\nGraph Analytics")
            print("----------------")

            print(
                f"Entities: {len(graph.entities)}"
            )

            print(
                f"Relationships: "
                f"{len(graph.relationships)}"
            )

            print("\nRelationship types:")

            statistics = (
                graph.relationship_statistics()
            )

            for relationship_type, count in sorted(
                statistics.items()
            ):
                print(
                    f"  {relationship_type}: "
                    f"{count}"
                )

            print(
                "\nMost connected entities:"
            )

            for entity, degree in (
                graph.most_connected(10)
            ):
                print(
                    f"  {entity.name} "
                    f"({entity.entity_type}) "
                    f"- {degree} connections"
                )

            continue

        # -----------------------------------------------------
        # Find by name
        # -----------------------------------------------------

        if lower.startswith("find "):

            name = command[5:].strip()

            results = query.find_by_name(
                name
            )

            print_entities(results)

            continue

        # -----------------------------------------------------
        # Category
        # -----------------------------------------------------

        if lower.startswith("category "):

            category = command[9:].strip()

            results = query.find_by_category(
                category
            )

            print_entities(results)

            continue

        # -----------------------------------------------------
        # Develops
        # -----------------------------------------------------

        if lower.startswith("develops "):

            name = command[9:].strip()

            matches = query.find_by_name(
                name
            )

            if not matches:
                print("Entity not found.")
                continue

            for entity in matches:

                results = (
                    query.developed_entities(
                        entity.id
                    )
                )

                print(
                    f"{entity.name} develops:"
                )

                print_entities(results)

            continue

        # -----------------------------------------------------
        # Implements
        # -----------------------------------------------------

        if lower.startswith("implements "):

            name = command[11:].strip()

            matches = query.find_by_name(
                name
            )

            if not matches:
                print("Entity not found.")
                continue

            for entity in matches:

                results = (
                    query.implemented_models(
                        entity.id
                    )
                )

                print(
                    f"{entity.name} implements:"
                )

                print_entities(results)

            continue

        # -----------------------------------------------------
        # Solves
        # -----------------------------------------------------

        if lower.startswith("solves "):

            name = command[7:].strip()

            matches = query.find_by_name(
                name
            )

            if not matches:
                print("Entity not found.")
                continue

            for entity in matches:

                results = query.solved_tasks(
                    entity.id
                )

                print(
                    f"{entity.name} solves:"
                )

                print_entities(results)

            continue

        # -----------------------------------------------------
        # Neighbors
        # -----------------------------------------------------

        if lower.startswith("neighbors "):

            name = command[10:].strip()

            matches = query.find_by_name(
                name
            )

            if not matches:
                print("Entity not found.")
                continue

            for entity in matches:

                results = graph.get_neighbors(
                    entity.id
                )

                print(
                    f"{entity.name} neighbors:"
                )

                print_entities(results)

            continue

        # -----------------------------------------------------
        # Help
        # -----------------------------------------------------

        print("Commands:")
        print("  stats")
        print("  analytics")
        print("  find <name>")
        print("  category <category>")
        print("  develops <company>")
        print("  implements <repository>")
        print("  solves <tool>")
        print("  neighbors <entity>")
        print("  exit")


if __name__ == "__main__":
    main()