import os
import json
from PIL import Image
from google import genai
from google.genai import types

from src.tools import reconcile_ledgers
from src.rag_engine import init_policy_rag, query_policy

def run_analyst_agent(ledger_1: str, ledger_2: str, image_path: str) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    print(" [Analyst Agent] Executing ledger reconciliation tool...")
    raw_discrepancies = reconcile_ledgers(ledger_1, ledger_2)
    discrepancy_data = json.loads(raw_discrepancies)

    print(" [Analyst Agent] Querying ChromaDB RAG Knowledge Base...")
    rag_col = init_policy_rag()
    rag_context = query_policy(rag_col, "variance exceeding limit cash equivalence reporting risk")

    print(" [Analyst Agent] Loading BI dashboard image...")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Dashboard image not found at {image_path}")
        
    dashboard_img = Image.open(image_path)

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert Senior Financial Analyst AI.
    
    Relevant GAAP/IFRS Policies (RAG Context):
    {rag_context}

    Raw Ledger Discrepancies (Reconciliation Data):
    {json.dumps(discrepancy_data, indent=2)}
    
    Task:
    - Inspect table values in the dashboard image.
    - Compare visual values against raw ledger discrepancy data provided.
    - Evaluate risk severity based on RAG GAAP policies.
    - Output a clean JSON structure summarizing:
      a) Discrepancies identified between ERP and Audit ledgers.
      b) Mismatches between visual BI dashboard and actual audit facts.
      c) Concise explanation of financial impact.
    
    Respond STRICTLY with valid JSON.
    """
    
    print(" [Analyst Agent] Invoking Gemini Multimodal Vision model...")
    for model_id in ['gemini-3.6-flash', 'gemini-1.5-flash']:
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=[dashboard_img, prompt],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            synthesis = json.loads(response.text)
            return {
                "raw_tool_discrepancies": discrepancy_data,
                "rag_retrieved_policy": rag_context,
                "analyst_multimodal_synthesis": synthesis
            }
        except Exception as e:
            print(f" [Analyst Agent] Model '{model_id}' attempt notice: {e}")
            continue

    raise RuntimeError("Failed to generate audit report with available Gemini models.")