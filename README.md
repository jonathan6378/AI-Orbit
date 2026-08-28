# AI Orbit

 API-first discovery 

 real discovery adapters while preserving the exact canonical entity schema.

### Canonical schema

```json
{
  "id": "stable-generated-uuid",
  "entity_type": "string",
  "name": "string",
  "description": "string",
  "url": "string",
  "categories": [],
  "source": {
    "name": "string",
    "url": "string"
  }
}
```

### Discovery sources

- GitHub REST API → `REPOSITORY`
- Hugging Face Hub API → `MODEL`

The GitHub adapter uses repository search and supports an optional `GITHUB_TOKEN`.
The Hugging Face adapter uses the Hub models endpoint and supports an optional `HF_TOKEN`.

### Environment

Create a `.env`/shell environment if you want authenticated API access:

```text
GITHUB_TOKEN=your_token
HF_TOKEN=your_token
```

The adapters also work with public endpoints without tokens, subject to source rate limits.

### Run discovery

```bash
python -m src.discovery.run_discovery
```

Or from Python:

```python
from src.discovery.run_discovery import discover, save_discovered_entities

entities = discover(
    github_query="topic:artificial-intelligence",
    github_limit=30,
    hf_search="llm",
    hf_limit=30
)
save_discovered_entities(entities, "data/intermediate/discovered_entities.json")
```

### Run complete Phase 2 pipeline

```bash
python run.py
```

Phase 3 deliberately does not add provider/stars/license/etc. as top-level fields because the project requires the canonical schema above. Those source-specific details can be used internally for later classification and relationship construction without changing the final entity contract.
