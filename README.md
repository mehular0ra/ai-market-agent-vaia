# AI Market Analyst

Multi-functional AI agent for market research analysis using RAG (Retrieval-Augmented Generation). Built for the VAIA Agentic AI Residency Program.

## Features

- **Q&A Workflow**: Answer specific questions about market research documents
- **Summarization Workflow**: Generate executive summaries of market research reports
- **Data Extraction Workflow**: Extract structured JSON data from documents
- **Intelligent Query Router**: Automatically routes queries to the appropriate workflow
- **RESTful API**: FastAPI-based API with 6 endpoints

## Tech Stack

- **Python 3.13** with `uv` package manager
- **PostgreSQL** with `pgvector` extension for vector similarity search
- **OpenAI API** for embeddings and LLM completions
- **FastAPI** for REST API
- **Jinja2** for prompt template management

## Architecture

### Project Structure

```
ai-market-agent-vaia/
├── app/
│   ├── api/              # FastAPI application
│   ├── database/         # Database layer (config, connection, repository)
│   ├── prompts/          # Jinja2 prompt templates
│   ├── services/         # Business logic (chunking, embedding, retrieval, router)
│   └── workflows/        # Workflow implementations (Q&A, summarization, extraction)
├── data/                 # Market research documents
├── tests/                # Test suite
└── pyproject.toml        # Dependencies
```

### Design Decisions

1. **Minimal Approach**: Only essential dependencies and files, no optional components
2. **Template-Based Prompts**: All LLM prompts managed via Jinja2 templates with frontmatter metadata
3. **Repository Pattern**: Clean separation between data access and business logic
4. **RAG Architecture**: Document chunking → Embedding → Vector search → Context assembly
5. **Single Source of Truth**: `pyproject.toml` for dependencies

### RAG Pipeline

1. **Document Processing**: Text → Token-based chunks (250 tokens, 50 overlap)
2. **Embedding Generation**: OpenAI `text-embedding-3-small` (1536 dimensions)
3. **Vector Storage**: PostgreSQL with pgvector extension
4. **Retrieval**: Cosine similarity search for relevant chunks
5. **Context Assembly**: Top-k chunks combined for LLM context

## Setup

### Prerequisites

- Python 3.13+
- PostgreSQL with pgvector extension
- OpenAI API key
- `uv` package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-market-agent-vaia
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```
OPENAI_API_KEY=your_openai_api_key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=market_analyst
DB_USER=postgres
DB_PASSWORD=your_password
CHUNK_SIZE=250
CHUNK_OVERLAP=50
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini
```

4. Initialize the database:
```bash
cd app
uv run python init_db.py
```

5. Process the market research document:
```bash
uv run python process_document.py
```

## Usage

### Start the API Server

```bash
uv run python run_api.py
```

Server runs on: `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs`

### API Endpoints

#### 1. Health Check
```bash
GET /health
```

#### 2. Auto-Route Query
```bash
POST /query
{
  "query": "What is the market share?",
  "top_k": 3
}
```

#### 3. Q&A Workflow
```bash
POST /qa
{
  "query": "Who are the main competitors?",
  "top_k": 3
}
```

#### 4. Summarization Workflow
```bash
POST /summarize
```

#### 5. Data Extraction Workflow
```bash
POST /extract
```

### Example Usage

**Q&A:**
```bash
curl -X POST http://localhost:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Innovate Inc'\''s market share?", "top_k": 2}'
```

**Summarization:**
```bash
curl -X POST http://localhost:8000/summarize
```

**Extraction:**
```bash
curl -X POST http://localhost:8000/extract
```

**Auto-routing:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Summarize the key findings", "top_k": 2}'
```

## Testing

Run individual test suites:

```bash
# Prompt management
uv run python tests/test_prompts.py

# RAG retrieval
uv run python tests/test_retrieval.py

# Q&A workflow
uv run python tests/test_qa.py

# Summarization workflow
uv run python tests/test_summarization.py

# Data extraction workflow
uv run python tests/test_extraction.py

# Query router
uv run python tests/test_router.py

# API endpoints
uv run python tests/test_api.py
```

## Workflows

### 1. Q&A Workflow

**Purpose**: Answer specific questions about market research data

**Process**:
1. User asks a question
2. Generate embedding for the question
3. Retrieve top-k similar document chunks
4. Assemble context from chunks
5. Generate answer using LLM with context

**Configuration**:
- Temperature: 0.3 (focused, deterministic)
- Max tokens: 500
- Prompts: `qa_system.j2`, `qa_user.j2`

### 2. Summarization Workflow

**Purpose**: Generate executive summaries of market research reports

**Process**:
1. Retrieve all document chunks
2. Combine into full context
3. Generate summary using LLM

**Configuration**:
- Temperature: 0.5 (more creative)
- Max tokens: 800
- Prompts: `summarization_system.j2`, `summarization_user.j2`

### 3. Data Extraction Workflow

**Purpose**: Extract structured JSON data from documents

**Process**:
1. Retrieve all document chunks
2. Combine into full context
3. Extract data using LLM with JSON mode

**Configuration**:
- Temperature: 0.0 (maximum precision)
- Max tokens: 1000
- Response format: JSON object
- Prompts: `extraction_system.j2`, `extraction_user.j2`

**Output Schema**:
```json
{
  "company_name": "string",
  "product_name": "string",
  "market_share_percent": "number",
  "market_size_billions": "number",
  "projected_market_size_billions": "number",
  "cagr_percent": "number",
  "competitors": [{"name": "string", "market_share_percent": "number"}],
  "strengths": ["string"],
  "weaknesses": ["string"],
  "opportunities": ["string"],
  "threats": ["string"]
}
```

## Prompt Management

All LLM prompts are managed via Jinja2 templates in `app/prompts/`:

- `router.j2` - Query routing classification
- `qa_system.j2`, `qa_user.j2` - Q&A workflow
- `summarization_system.j2`, `summarization_user.j2` - Summarization workflow
- `extraction_system.j2`, `extraction_user.j2` - Data extraction workflow

Each template includes YAML frontmatter with metadata:
```yaml
---
description: Purpose of the prompt
author: AI Market Analyst Team
variables:
  - list_of_variables
---
```

## Dependencies

Core dependencies (11 total):
- `fastapi>=0.121.0` - Web framework
- `uvicorn>=0.35.0` - ASGI server
- `openai>=2.6.1` - OpenAI API client
- `pgvector>=0.4.1` - PostgreSQL vector extension
- `psycopg2-binary>=2.9.10` - PostgreSQL adapter
- `pydantic>=2.11.0` - Data validation
- `python-dotenv>=1.0.1` - Environment variables
- `tiktoken>=0.12.0` - Token counting
- `numpy>=2.2.0` - Numerical operations
- `jinja2>=3.1.6` - Template engine
- `python-frontmatter>=1.1.0` - YAML frontmatter parsing

## Development

### Adding New Workflows

1. Create prompt templates in `app/prompts/`
2. Implement workflow class in `app/workflows/`
3. Add endpoint in `app/api/main.py`
4. Update router in `app/prompts/router.j2`
5. Create tests in `tests/`

### Modifying Prompts

Edit the Jinja2 templates in `app/prompts/` 

