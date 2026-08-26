import argparse
from src.discovery.run_discovery import discover, save_discovered_entities

parser = argparse.ArgumentParser(description="AI Orbit API-first discovery")
parser.add_argument("--github-query", default="topic:artificial-intelligence")
parser.add_argument("--github-limit", type=int, default=30)
parser.add_argument("--hf-search", default="llm")
parser.add_argument("--hf-limit", type=int, default=30)
parser.add_argument("--output", default="data/intermediate/discovered_entities.json")
args = parser.parse_args()

entities = discover(
    github_query=args.github_query,
    github_limit=args.github_limit,
    hf_search=args.hf_search,
    hf_limit=args.hf_limit,
)
save_discovered_entities(entities, args.output)

print(f"Discovered entities: {len(entities)}")
print(f"Saved to: {args.output}")
