# AI Orbit

AI Orbit is an AI knowledge discovery and relationship-mapping pipeline.

The system collects information from multiple AI-related sources, converts the collected information into a common entity format, cleans and validates the data, removes duplicates, generates relationships between entities, and stores the resulting knowledge graph as JSON.

It also provides a queryable in-memory knowledge graph and a FastAPI interface.

## Final status

- 158 validated entities
- 160 relationships
- 40 automated tests passing
- FastAPI API with Swagger/OpenAPI documentation

## Project structure

```text
AI-Orbit/
├── src/
│   ├── api/
│   ├── connectors/
│   ├── graph/
│   ├── models/
│   ├── processing/
│   └── relationships/
├── data/
│   ├── entities.json
│   └── relationships.json
├── tests/
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Entity types

| Type | Count |
|---|---:|
| Repository | 50 |
| Model | 50 |
| News | 10 |
| Company | 10 |
| Task | 10 |
| Video | 10 |
| Device | 10 |
| Tool | 8 |
| **Total** | **158** |

## Relationships

| Relationship | Count |
|---|---:|
| implements | 124 |
| solves | 24 |
| develops | 12 |
| **Total** | **160** |

## Sources

- GitHub
- Hugging Face
- RSS/news feeds
- Curated catalog records

## Run

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the ingestion pipeline:

```powershell
python run.py
```

Run tests:

```powershell
python -m pytest -q
```

Run the CLI knowledge graph:

```powershell
python -m src.graph.cli
```

Run the API:

```powershell
python -m uvicorn src.api.app:app --reload
```

Swagger UI is available at `http://127.0.0.1:8000/docs`.

## Technical decisions

The project separates data collection, processing, validation, deduplication, relationship generation, graph operations, and API access so each stage can be tested independently.

JSON was selected for the generated entity and relationship outputs because it is portable, human-readable, and easy to inspect. Entity identity uses the entity type together with the normalized URL, allowing different entity types to legitimately share the same URL.

The current graph is stored in memory because the project dataset is small enough for fast dictionary-based lookup. The design can later be migrated to a persistent graph database if required.
