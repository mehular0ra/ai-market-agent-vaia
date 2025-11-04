# AI Market Analyst

Multi-functional AI agent for market research analysis using RAG (Retrieval-Augmented Generation). Built for the VAIA Agentic AI Residency Program.

## Features

### Core Workflows
- **Q&A Workflow**: Answer specific questions about market research documents
- **Summarization Workflow**: Generate executive summaries of market research reports
- **Data Extraction Workflow**: Extract structured JSON data from documents

### Extras
- **1**: Intelligent Query Router - Automatically routes queries to the appropriate workflow (100% accuracy)
- **2**: Comparative Evaluation - Benchmarked embedding models, chunking strategies, and retrieval parameters (see `docs/EVALUATION.md`)
- **3**: Containerization - Docker and docker-compose for easy deployment (see `docker/` directory)
- **4**: Gradio Web UI - Interactive web interface for all workflows

### Infrastructure
- **RESTful API**: FastAPI-based API with 6 endpoints
- **Vector Database**: PostgreSQL with pgvector for efficient similarity search
- **Prompt Management**: Jinja2 templates with YAML frontmatter

## Tech Stack

- **Python 3.13** with `uv` package manager
- **PostgreSQL** with `pgvector` extension for vector similarity search
- **OpenAI API** for embeddings and LLM completions
- **FastAPI** for REST API
- **Jinja2** for prompt template management

## Design Decisions

### Chunking Strategy

**Choice**: Token-based chunking with 250 tokens and 50 token overlap

**Rationale**:
- **250 tokens**: Balances context preservation and granularity
  - Too small (<100): Loses semantic context, fragments ideas
  - Too large (>500): Dilutes relevance, increases noise in retrieval
  - 250 tokens ≈ 1-2 paragraphs, ideal for market research content
- **50 token overlap**: Prevents context loss at chunk boundaries
  - Ensures key information isn't split across chunks
  - 20% overlap is industry standard for RAG systems
- **Token-based vs. character-based**: Ensures consistent chunk sizes for embeddings
  - Character-based chunks vary in semantic content
  - Token-based aligns with LLM processing units

### Embedding Model

**Choice**: OpenAI `text-embedding-3-small`

**Rationale**:
- **Cost-effective**: $0.02 per 1M tokens (62.5% cheaper than text-embedding-ada-002)
- **Performance**: Strong performance on MTEB benchmark (62.3% average)
- **Dimensions**: 1536 dimensions (standard size, good balance)
- **Speed**: Fast inference for real-time applications
- **Simplicity**: No model hosting required, managed API
- **Alternatives considered**:
  - `text-embedding-3-large`: Better performance but 5x more expensive
  - Open-source models (Sentence-BERT): Requires hosting, maintenance
  - Cohere embeddings: Similar cost, less ecosystem support

### Vector Database

**Choice**: PostgreSQL with pgvector extension

**Rationale**:
- **Simplicity**: Single database for both structured and vector data
  - No need to sync between relational DB and vector store
  - Reduces operational complexity
- **Maturity**: Battle-tested, ACID guarantees, robust tooling
- **Cost**: No additional service costs (vs. Pinecone, Weaviate)
- **Performance**: IVFFlat index provides fast approximate nearest neighbor search
- **Scalability**: Sufficient for small-to-medium datasets (<1M vectors)
- **Alternatives considered**:
  - **Pinecone**: Better performance at scale, but adds cost and complexity
  - **Weaviate**: More features, but overkill for this use case
  - **Chroma**: Simpler, but less mature and fewer production deployments
  - **FAISS**: Requires custom integration, no persistence layer

### Data Extraction Prompt Design

**Choice**: Structured prompts with OpenAI JSON mode

**Strategy**:
1. **JSON Mode**: `response_format={"type": "json_object"}`
   - Guarantees valid JSON output (no parsing errors)
   - LLM is constrained to produce only JSON

2. **Temperature 0.0**: Maximum precision and consistency
   - Deterministic output for data extraction
   - Reduces hallucination risk

3. **Explicit Schema in Prompt**: Define exact JSON structure
   - Field names, types, and descriptions
   - Example values for clarity
   - Null handling instructions

4. **Two-Prompt Pattern**: System + User prompts
   - System: Role definition and constraints
   - User: Context + schema + instructions

5. **Validation**: Parse JSON and handle errors gracefully
   - Try/except for JSON parsing
   - Return error details if parsing fails

**Results**: 100% valid JSON output in testing, no parsing errors

### Autonomous Query Routing

**Choice**: LLM-based classification

**Rationale**:
- **Flexibility**: Handles natural language variations
  - Rule-based routing fails on edge cases
  - LLM understands intent, not just keywords
- **Accuracy**: 100% on test set (9/9 queries)
- **Simplicity**: Single prompt, no complex rules
- **Extensibility**: Easy to add new workflow categories
- **Temperature 0.0**: Deterministic routing decisions
- **Fallback**: Defaults to Q&A if classification fails

**Implementation**: See `/query` endpoint and `app/services/router.py`

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

### Option 1: Gradio Web UI 
Interactive web interface for all workflows:

```bash
uv run python app/ui/gradio_app.py
```

Access at: `http://localhost:7860`

**Features:**
- 🔀 **Auto-Route Tab**: Intelligent query routing (Bonus 1)
- 💬 **Q&A Tab**: Ask questions with adjustable top-k
- 📊 **Summarization Tab**: Generate executive summaries
- 📋 **Extraction Tab**: Extract structured JSON data
- ℹ️ **About Tab**: Architecture and tech stack info

### Docker Setup

Run the application using Docker:

```bash
cd docker
./docker-setup.sh
```

This script will:
1. Check for required environment variables
2. Build Docker images
3. Start PostgreSQL + API services
4. Initialize the database
5. Process the sample document

**Access the application:**
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

**Manual Docker commands:**
```bash
cd docker
docker-compose up -d
docker-compose exec api uv run python app/init_db.py
docker-compose exec api uv run python app/process_document.py
```

### Option 3: API Server (Local)

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

## Evaluation & Benchmarking

### Comparative Evaluation (Bonus 2)

Comprehensive benchmarking results are available in:
- **`docs/EVALUATION.md`**: Detailed analysis and recommendations
- **`evaluation_results.json`**: Raw benchmark data

**What was evaluated:**
1. **Embedding Models**: text-embedding-3-small vs. text-embedding-3-large
2. **Chunking Strategies**: 150, 250, and 500 tokens with varying overlap
3. **Retrieval Top-K**: k=1, 3, 5, 10

**Key Findings:**
- text-embedding-3-small is optimal (6.5x cheaper, sufficient quality)
- 250 tokens with 50 overlap provides best balance
- top-k=3 is optimal for retrieval (fastest, sufficient context)

**Run the benchmark:**
```bash
uv run python app/evaluation/benchmark.py
```

See `docs/EVALUATION.md` for detailed analysis, cost comparisons, and recommendations.

---

## Dependencies

Core dependencies (13 total):
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
- `gradio>=5.0.0` - Web UI framework (Bonus 4)

## Development

### Adding New Workflows

1. Create prompt templates in `app/prompts/`
2. Implement workflow class in `app/workflows/`
3. Add endpoint in `app/api/main.py`
4. Update router in `app/prompts/router.j2`
5. Create tests in `tests/`

### Modifying Prompts

Edit the Jinja2 templates in `app/prompts/`
