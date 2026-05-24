# uplevel_ai

**Daily leadership impact agent for engineering leaders.**

uplevel_ai helps engineering managers build broader leadership impact by observing daily activity signals, scoring them against a leadership growth rubric, and surfacing personalised reflection prompts and weekly impact narratives.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Ingestion Layer                                            │
│  calendar · transcripts · ADO/Jira · GitHub                 │
└──────────────────────┬──────────────────────────────────────┘
                       │ raw events
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  LangGraph Agent Pipeline                                   │
│                                                             │
│  observe → score → reflect → build_report                   │
│                                                             │
│  • observe:      normalises raw events → Observations       │
│  • score:        classifies against leadership growth rubric │
│  • reflect:      synthesises prompts + narrative (Claude)   │
│  • build_report: assembles DailyReport                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌─────────────────┐       ┌──────────────────────┐
│  Postgres       │       │  Neo4j               │
│  event_log      │       │  influence graph     │
│  daily_reports  │       │  Person · Team ·     │
└─────────────────┘       │  Decision nodes      │
                          └──────────────────────┘
                                    │
                       ┌────────────▼────────────┐
                       │  FastAPI                │
                       │  POST /reflection       │
                       │  GET  /report/daily     │
                       │  GET  /report/weekly    │
                       └─────────────────────────┘
```

---

## Leadership Growth Scoring Rubric

Each day is scored across 10 dimensions on a 1–5 scale:

| Dimension | Growth Expectation |
|-----------|---------------|
| **Strategic Influence** | Contributes to multi-quarter technical strategy and helps align stakeholders |
| **Org Leverage** | Prioritises high-leverage work while balancing direct contribution and enablement |
| **Delegation Effectiveness** | Delegates meaningful ownership with clear outcomes, not just tasks |
| **Executive Alignment** | Surfaces risks and trade-offs early to keep partners aligned |
| **Visibility** | Makes engineering impact visible across product, finance, and leadership partners |
| **Ambiguity Reduction** | Makes pragmatic calls with incomplete information and drives action |
| **Artifact Creation** | Creates clear written artefacts that support consistency across teams |
| **Cross-Team Impact** | Supports cross-functional initiatives and helps teams connect effectively |
| **Risk Anticipation** | Maintains forward-looking risk awareness and helps drive mitigations |
| **Decision Leadership** | Encourages decisions at the appropriate level and focuses on highest-leverage calls |

Score 1 = developing consistency in leadership habits  
Score 3 = strong, consistent leadership across team scope  
Score 5 = broad, high-leverage leadership impact across the organisation

---

## Project Structure

```
src/
  config.py               # pydantic-settings configuration
  ingestion/
    calendar.py           # Google Calendar / Outlook fetcher
    transcripts.py        # Otter / Teams / Zoom transcript parser
    ado_jira.py           # ADO and Jira work-item ingestion
    github.py             # GitHub PR and event ingestion
  agents/
    graph.py              # LangGraph StateGraph wiring
    observation.py        # observe node: raw events → Observations
    scoring.py            # score node: Observations → ScoredObservations
    reflection.py         # reflect node: synthesis + prompts
    report.py             # build_report node: DailyReport assembly
  memory/
    postgres.py           # SQLAlchemy async ORM + event log models
    neo4j.py              # Neo4j async client + influence graph helpers
  scoring/
    rubric.py             # leadership growth rubric dataclasses (10 dimensions)
    classifier.py         # Anthropic SDK classifier with prompt caching
  reports/
    daily.py              # Markdown + JSON daily report renderer
    weekly.py             # Weekly narrative generator
  api/
    main.py               # FastAPI app factory
    routes/
      reflection.py       # /reflection and /report endpoints
tests/                    # mirrors src structure
```

---

## Quick Start

### 1. Start infrastructure

```bash
docker compose up -d
# wait for postgres and neo4j to be healthy
docker compose ps
```

### 2. Configure environment

```bash
cp .env.example .env
# edit .env — at minimum set ANTHROPIC_API_KEY
```

### 3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 4. Run the API

```bash
uvicorn src.api.main:app --reload
# → http://localhost:8000
# → http://localhost:8000/docs  (Swagger UI)
```

### 5. Submit a daily reflection

```bash
curl -X POST http://localhost:8000/api/v1/reflection \
  -H "Content-Type: application/json" \
  -d '{"reflection_text": "Led the quarterly roadmap review with the CPO. Unblocked the platform team on the auth migration decision."}'
```

### 6. Run tests

```bash
pytest tests/ -v
```

---

## Neo4j Browser

Open [http://localhost:7474](http://localhost:7474) and connect with `neo4j` / `uplevel_ai`.

Useful queries:
```cypher
// See all people the leader has collaborated with
MATCH (l:Person)-[r:COLLABORATED_WITH]->(p:Person) RETURN l, r, p

// Find decision nodes
MATCH (p:Person)-[:MADE_DECISION]->(d:Decision) RETURN p, d
```

---

## Development Roadmap

### V1 (this scaffold)
- [x] LangGraph agent pipeline wired
- [x] Leadership rubric defined (10 dimensions)
- [x] FastAPI endpoints scaffolded
- [x] Postgres + Neo4j infrastructure
- [ ] Implement Anthropic classifier with prompt caching
- [ ] Implement observation extraction per ingestion source
- [ ] Persist reports to Postgres

### V2
- [ ] Google Calendar OAuth2 ingestion
- [ ] GitHub ingestion
- [ ] Jira / ADO ingestion
- [ ] Email delivery of daily report
- [ ] Trend charts in weekly narrative
- [ ] Neo4j influence graph visualisation

---

## Stack

- **Python 3.11+**
- **LangGraph** — agent graph orchestration
- **Anthropic SDK** — Claude for classification and narrative generation (with prompt caching)
- **FastAPI** — async REST API
- **SQLAlchemy (async) + asyncpg** — Postgres ORM
- **Neo4j** — influence relationship graph
- **Pydantic v2** — settings and request/response validation
- **Pytest + pytest-asyncio** — testing
