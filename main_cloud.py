import functions_framework
from src.analyst import run_analyst_agent
from src.critic import run_critic_agent
from src.logger import generate_xai_audit_report
from src.workspace_exporter import export_audit_to_sheets

@functions_framework.http
def audit_pipeline_http(request):
    request_json = request.get_json(silent=True) or {}
    
    ledger_1 = request_json.get("ledger_1", "data/financial_1.csv")
    ledger_2 = request_json.get("ledger_2", "data/financial_2.csv")
    image_path = request_json.get("image_path", "data/dashboard_bi.png")
    spreadsheet_id = request_json.get("spreadsheet_id", "")

    # Execute agent pipeline
    analyst_findings = run_analyst_agent(ledger_1, ledger_2, image_path)
    critic_validation = run_critic_agent(analyst_findings)
    
    combined = {
        "analyst_findings": analyst_findings,
        "critic_validation": critic_validation
    }
    
    report_path = generate_xai_audit_report(combined)

    # Optional Google Sheets export
    if spreadsheet_id:
        row = [
            critic_validation.get("audit_status", "N/A"),
            critic_validation.get("risk_severity", "N/A"),
            f"-50000000.00"
        ]
        export_audit_to_sheets(spreadsheet_id, row)

    return {
        "status": "SUCCESS",
        "audit_status": critic_validation.get("audit_status"),
        "risk_severity": critic_validation.get("risk_severity"),
        "report_generated": report_path
    }, 200

if __name__ == "__main__":
    print("To test locally as serverless function, run:\nfunctions-framework --target=audit_pipeline_http --debug")
