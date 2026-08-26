# AI Orbit — Data Ingestion Pipeline

AI Orbit is a Python-based, API-first data ingestion pipeline for aggregating, normalizing, deduplicating, classifying, validating, and relationship-mapping information across the AI ecosystem.

The project specification calls for the workflow:

**Discovery → Extraction → Cleaning → Normalization → Deduplication → Classification → Relationship Mapping → Validation**

## Required data scope

The target is a high-quality representative dataset of **250–300 records** across categories including:

- Tools
- Tasks
- Companies
- News
- Videos
- Robots
- Devices
- Models
- Repositories
- MCP servers/tools
- Collections
- Personal AI assistants
- Creative-generation tools
- Recently added entities

## Data schema

Each entity should include:

```json
{
  "id": "stable-generated-uuid",
  "entity_type": "string",
  "name": "string",
  "description": "string",
  "url": "string",
  "categories": ["string"],
  "source": {
    "name": "string",
    "url": "string"
  }
}
```

Specialized metadata is required where applicable, including model licensing/modalities/provider information, repository stars/language/last-updated information, MCP installation/runtime information, and company founding year/sector/headquarters.

## Relationship mapping

The pipeline must generate `data/relationships.json` containing ecosystem relationships such as:

- Company → develops → Tool/Model
- Tool → solves → Task
- MCP → integrates_with → Tool
- Device → runs → Model

## Repository structure

```text
AI-Orbit/
├── src/                    # Pipeline and application logic
├── data/                   # Generated JSON datasets
│   ├── entities.json
│   └── relationships.json
├── tests/                  # Automated tests
├── run.py                  # Pipeline entry point
├── requirements.txt        # Python dependencies
├── .gitignore              # Files excluded from Git
└── README.md               # Technical documentation
```

## Engineering requirements

The implementation should demonstrate:

- Entity resolution and canonicalization
- URL normalization and redirect handling
- HTML/RSS text sanitization
- Graceful handling of missing fields
- Logging and resilient source connectors
- Modular and reusable pipeline components
- API-first discovery rather than brute-force scraping

## Expected sources

The specification identifies GitHub, Hugging Face, YouTube, News/RSS, official product sites, and AI directories as candidate sources.

## Deliverables

The final submission should contain `src/` for pipeline logic, `data/` for final JSON outputs, `run.py` for execution, and `README.md` documenting technical decisions.

> **Note:** The repository currently contains the README only. The source project files and generated dataset have not yet been uploaded because they are not present as files in this conversation. Upload the project folder/ZIP and the remaining files can be added to this repository without inventing or replacing project code.
