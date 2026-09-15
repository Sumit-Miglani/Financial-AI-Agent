import os
import tempfile
import json
import functions_framework
from flask import jsonify

from src.analyst import run_analyst_agent
from src.critic import run_critic_agent
from src.logger import generate_xai_audit_report

@functions_framework.http
def audit_pipeline(request):
    if request.method != "POST":
        return jsonify({"error": "Only POST requests are accepted."}), 455

    if "ledger1" not in request.files or "ledger2" not in request.files or "dashboard" not in request.files:
        return jsonify({
            "error": "Missing required files. Please provide 'ledger1', 'ledger2', and 'dashboard'."
        }), 400

    ledger1_file = request.files["ledger1"]
    ledger2_file = request.files["ledger2"]
    dashboard_file = request.files["dashboard"]

    with tempfile.TemporaryDirectory() as tmp_dir:
        l1_path = os.path.join(tmp_dir, "ledger1.csv")
        l2_path = os.path.join(tmp_dir, "ledger2.csv")
        img_path = os.path.join(tmp_dir, "dashboard.png")

        ledger1_file.save(l1_path)
        ledger2_file.save(l2_path)
        dashboard_file.save(img_path)

        try:
            analyst_findings = run_analyst_agent(
                ledger_1=l1_path,
                ledger_2=l2_path,
                image_path=img_path
            )
            critic_findings = run_critic_agent(analyst_findings)
            audit_report = generate_xai_audit_report(
                analyst_findings=analyst_findings,
                critic_findings=critic_findings
            )

            return jsonify({
                "status": "success",
                "analyst_findings": analyst_findings,
                "critic_findings": critic_findings,
                "audit_report": audit_report
            }), 200

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500