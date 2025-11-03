from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from workflows.qa_workflow import QAWorkflow
from workflows.summarization_workflow import SummarizationWorkflow
from workflows.extraction_workflow import ExtractionWorkflow
from services.router import QueryRouter

app = FastAPI(
    title="AI Market Analyst API",
    description="Multi-functional AI agent for market research analysis",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


class QueryResponse(BaseModel):
    workflow: str
    result: dict


@app.get("/")
def root():
    return {
        "message": "AI Market Analyst API",
        "endpoints": {
            "/health": "Health check endpoint",
            "/query": "Auto-route query to appropriate workflow",
            "/qa": "Question answering workflow",
            "/summarize": "Summarization workflow",
            "/extract": "Data extraction workflow",
        },
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    router = QueryRouter()
    workflow_type = router.route(request.query)

    if workflow_type == "qa":
        qa = QAWorkflow()
        result = qa.run(request.query, top_k=request.top_k)
    elif workflow_type == "summarization":
        summarization = SummarizationWorkflow()
        result = summarization.run()
    elif workflow_type == "extraction":
        extraction = ExtractionWorkflow()
        result = extraction.run()
    else:
        raise HTTPException(status_code=400, detail="Invalid workflow type")

    return {"workflow": workflow_type, "result": result}


@app.post("/qa")
def qa_endpoint(request: QueryRequest):
    qa = QAWorkflow()
    result = qa.run(request.query, top_k=request.top_k)
    return {"workflow": "qa", "result": result}


@app.post("/summarize")
def summarize_endpoint():
    summarization = SummarizationWorkflow()
    result = summarization.run()
    return {"workflow": "summarization", "result": result}


@app.post("/extract")
def extract_endpoint():
    extraction = ExtractionWorkflow()
    result = extraction.run()
    return {"workflow": "extraction", "result": result}
