import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import os
import json
import gradio as gr
from dotenv import load_dotenv

from app.workflows.qa_workflow import QAWorkflow
from app.workflows.summarization_workflow import SummarizationWorkflow
from app.workflows.extraction_workflow import ExtractionWorkflow
from app.services.router import QueryRouter

load_dotenv()


def qa_interface(query: str, top_k: int):
    if not query.strip():
        return "Please enter a question.", ""

    try:
        workflow = QAWorkflow()
        result = workflow.run(query, top_k=top_k)

        answer = result.get("answer", "No answer generated")

        context_info = f"**Retrieved Chunks:** {result.get('chunks_used', 0)}\n\n"
        if "context_chunks" in result:
            context_info += "**Context:**\n\n"
            for i, chunk in enumerate(result["context_chunks"], 1):
                similarity = chunk.get("similarity", 0)
                content = chunk.get("content", "")
                context_info += f"**Chunk {i}** (Similarity: {similarity:.4f}):\n{content}\n\n---\n\n"

        return answer, context_info

    except Exception as e:
        return f"Error: {str(e)}", ""


def summarization_interface():
    try:
        workflow = SummarizationWorkflow()
        result = workflow.run()

        summary = result.get("summary", "No summary generated")
        metadata = f"**Chunks Used:** {result.get('chunks_used', 0)}\n**Model:** {result.get('model', 'N/A')}"

        return summary, metadata

    except Exception as e:
        return f"Error: {str(e)}", ""


def extraction_interface():
    try:
        workflow = ExtractionWorkflow()
        result = workflow.run()

        if "error" in result:
            return f"Error: {result['error']}", ""

        extracted_data = result.get("extracted_data", {})
        formatted_json = json.dumps(extracted_data, indent=2)

        metadata = f"**Chunks Used:** {result.get('chunks_used', 0)}\n**Model:** {result.get('model', 'N/A')}"

        return formatted_json, metadata

    except Exception as e:
        return f"Error: {str(e)}", ""


def auto_route_interface(query: str, top_k: int):
    if not query.strip():
        return "Please enter a query.", "", ""

    try:
        router = QueryRouter()
        workflow_type = router.route(query)

        if workflow_type == "qa":
            workflow = QAWorkflow()
            result = workflow.run(query, top_k=top_k)
            answer = result.get("answer", "No answer generated")
            metadata = f"**Workflow:** Q&A\n**Chunks Used:** {result.get('chunks_used', 0)}"
            return answer, metadata, workflow_type

        elif workflow_type == "summarization":
            workflow = SummarizationWorkflow()
            result = workflow.run()
            summary = result.get("summary", "No summary generated")
            metadata = f"**Workflow:** Summarization\n**Chunks Used:** {result.get('chunks_used', 0)}"
            return summary, metadata, workflow_type

        elif workflow_type == "extraction":
            workflow = ExtractionWorkflow()
            result = workflow.run()
            extracted_data = result.get("extracted_data", {})
            formatted_json = json.dumps(extracted_data, indent=2)
            metadata = f"**Workflow:** Extraction\n**Chunks Used:** {result.get('chunks_used', 0)}"
            return formatted_json, metadata, workflow_type

        else:
            return f"Unknown workflow type: {workflow_type}", "", workflow_type

    except Exception as e:
        return f"Error: {str(e)}", "", "error"


with gr.Blocks(title="AI Market Analyst", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
    # 🤖 AI Market Analyst
    
    Multi-functional AI agent for market research analysis using RAG (Retrieval-Augmented Generation).
    
    **Features:**
    - 💬 Q&A: Ask specific questions about market research
    - 📊 Summarization: Generate executive summaries
    - 📋 Extraction: Extract structured JSON data
    - 🔀 Auto-Route: Automatically select the right workflow
    """
    )

    with gr.Tabs():
        with gr.Tab("🔀 Auto-Route (Bonus 1)"):
            gr.Markdown(
                """
            ### Intelligent Query Routing
            
            Enter any query and the system will automatically route it to the appropriate workflow.
            
            **Examples:**
            - "What is the market share?" → Q&A
            - "Summarize the key findings" → Summarization
            - "Extract all competitors as JSON" → Extraction
            """
            )

            with gr.Row():
                with gr.Column():
                    auto_query = gr.Textbox(
                        label="Your Query",
                        placeholder="Enter any question, summary request, or extraction task...",
                        lines=2,
                    )
                    auto_topk = gr.Slider(
                        minimum=1,
                        maximum=10,
                        value=3,
                        step=1,
                        label="Top-K (for Q&A queries)",
                    )
                    auto_btn = gr.Button("Submit", variant="primary")

                with gr.Column():
                    auto_result = gr.Textbox(label="Result", lines=15)
                    auto_metadata = gr.Markdown(label="Metadata")
                    auto_workflow = gr.Textbox(label="Selected Workflow", interactive=False)

            auto_btn.click(
                fn=auto_route_interface,
                inputs=[auto_query, auto_topk],
                outputs=[auto_result, auto_metadata, auto_workflow],
            )

        with gr.Tab("💬 Q&A"):
            gr.Markdown(
                """
            ### Question Answering
            
            Ask specific questions about the market research document.
            The system retrieves relevant chunks and generates an answer.
            """
            )

            with gr.Row():
                with gr.Column():
                    qa_query = gr.Textbox(
                        label="Question",
                        placeholder="What is Innovate Inc's market share?",
                        lines=2,
                    )
                    qa_topk = gr.Slider(
                        minimum=1, maximum=10, value=3, step=1, label="Top-K Chunks"
                    )
                    qa_btn = gr.Button("Ask", variant="primary")

                with gr.Column():
                    qa_answer = gr.Textbox(label="Answer", lines=8)

            qa_context = gr.Markdown(label="Retrieved Context")

            qa_btn.click(
                fn=qa_interface,
                inputs=[qa_query, qa_topk],
                outputs=[qa_answer, qa_context],
            )

        with gr.Tab("📊 Summarization"):
            gr.Markdown(
                """
            ### Executive Summary
            
            Generate a comprehensive summary of the market research report.
            """
            )

            with gr.Row():
                with gr.Column():
                    sum_btn = gr.Button("Generate Summary", variant="primary")

                with gr.Column():
                    sum_result = gr.Textbox(label="Summary", lines=15)
                    sum_metadata = gr.Markdown(label="Metadata")

            sum_btn.click(
                fn=summarization_interface, inputs=[], outputs=[sum_result, sum_metadata]
            )

        with gr.Tab("📋 Data Extraction"):
            gr.Markdown(
                """
            ### Structured Data Extraction
            
            Extract structured JSON data from the market research document.
            Includes company info, market data, competitors, and SWOT analysis.
            """
            )

            with gr.Row():
                with gr.Column():
                    ext_btn = gr.Button("Extract Data", variant="primary")

                with gr.Column():
                    ext_result = gr.Code(label="Extracted JSON", language="json", lines=20)
                    ext_metadata = gr.Markdown(label="Metadata")

            ext_btn.click(
                fn=extraction_interface, inputs=[], outputs=[ext_result, ext_metadata]
            )

        with gr.Tab("ℹ️ About"):
            gr.Markdown(
                """
            ## About AI Market Analyst
            
            This application demonstrates a multi-functional AI agent built for the VAIA Agentic AI Residency Program.
            
            ### Architecture
            
            - **RAG Pipeline**: Document chunking → Embedding → Vector search → Context assembly
            - **Vector Database**: PostgreSQL with pgvector extension
            - **Embedding Model**: OpenAI text-embedding-3-small (1536 dimensions)
            - **LLM**: OpenAI gpt-4o-mini
            - **Chunking**: 250 tokens with 50 token overlap
            
            ### Workflows
            
            1. **Q&A**: Answers specific questions using retrieved context
            2. **Summarization**: Generates executive summaries
            3. **Extraction**: Extracts structured JSON data
            
            ### Bonus Features Implemented
            
            - ✅ **Bonus 1**: Autonomous Query Routing (100% accuracy)
            - ✅ **Bonus 2**: Comparative Evaluation (see EVALUATION.md)
            - ✅ **Bonus 3**: Containerization (Docker + docker-compose)
            - ✅ **Bonus 4**: Gradio UI (this interface)
            
            ### Tech Stack
            
            - Python 3.13
            - FastAPI
            - Gradio
            - PostgreSQL + pgvector
            - OpenAI API
            - Jinja2 (prompt templates)
            
            ---
            
            **Built for**: VAIA Agentic AI Residency Program  
            **Repository**: [GitHub Link]
            """
            )

    gr.Markdown(
        """
    ---
    💡 **Tip**: Try the Auto-Route tab to see intelligent query routing in action!
    """
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

