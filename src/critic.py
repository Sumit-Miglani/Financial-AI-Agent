import os
import json
from google import genai
from google.genai import types

def run_critic_agent(analyst_output: dict) -> dict:
    """
    Critic Agent:
    Recursively audits the Analyst Agent's output for mathematical correctness,
    hallucination prevention, and regulatory risk compliance.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an elite Senior AI Risk & Compliance Critic.

    Review the following Analyst Agent Output:
    {json.dumps(analyst_output)}

    Perform a strict evaluation:
    1. Verify if the recorded variance matches (recorded_amount - verified_amount).
    2. Ensure no hallucinated financial metrics or non-existent accounts were introduced.
    3. Evaluate if the identified variance ($50,000,000) represents a material financial risk.
    4. Determine if the report is approved or requires revision.

    Respond STRICTLY in valid JSON with this exact schema:
    {{
      "audit_status": "APPROVED" | "REJECTED_REVISION_NEEDED",
      "math_accuracy_verified": true | false,
      "risk_severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
      "critic_comments": "Concise justification of the audit evaluation"
    }}
    """

    # Model fallback hierarchy to prevent 503 UNAVAILABLE errors during high demand
    candidate_models = ['gemini-2.5-flash', 'gemini-1.5-flash']

    print(" [Critic Agent] Invoking Gemini verification model...")
    for model_id in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            print(f" [Critic Agent] Verification completed successfully using '{model_id}'.")
            return json.loads(response.text)
        except Exception as e:
            print(f" [Critic Agent] Notice: Model '{model_id}' unavailable/busy: {e}. Trying fallback model...")
            continue

    raise RuntimeError("Critic Agent failed: All fallback Gemini models are currently unavailable.")


if __name__ == "__main__":
    try:
        from src.analyst import run_analyst_agent
    except ImportError:
        from analyst import run_analyst_agent
    
    print(" [Workflow Orchestrator] Running Analyst Agent pipeline...")
    analyst_results = run_analyst_agent("data/financial_1.csv", "data/financial_2.csv", "data/dashboard_bi.png")
    
    print(" [Workflow Orchestrator] Passing findings to Critic Agent for audit validation...")
    critic_results = run_critic_agent(analyst_results)
    
    combined_report = {
        "analyst_findings": analyst_results,
        "critic_validation": critic_results
    }
    
    print("\n--- Multi-Agent Pipeline Output ---")
    print(json.dumps(combined_report, indent=2))