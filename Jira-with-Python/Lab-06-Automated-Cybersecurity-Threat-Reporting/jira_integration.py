from jira import JIRA
from dotenv import load_dotenv
import os
import json
import datetime

load_dotenv()

class JiraIntegration:
    def __init__(self):
        self.server = os.getenv("JIRA_SERVER")
        self.email = os.getenv("JIRA_EMAIL")
        self.token = os.getenv("JIRA_API_TOKEN")
        self.project_key = os.getenv("JIRA_PROJECT_KEY")

        self.jira = JIRA(
            server=self.server,
            basic_auth=(self.email, self.token)
        )

    def create_security_issue(self, alert, risk_level):
        priority_map = {
            "High": "Highest",
            "Medium": "High",
            "Low": "Medium",
            "Informational": "Low"
        }

        issue = {
            "project": {"key": self.project_key},
            "summary": f"[SECURITY] {alert.get('name', 'Unknown Vulnerability')}",
            "description": self.format_description(alert, risk_level),
            "issuetype": {"name": "Bug"},
            "priority": {"name": priority_map.get(risk_level, "Medium")},
            "labels": ["security", "automated", f"risk-{risk_level.lower()}"]
        }

        new_issue = self.jira.create_issue(fields=issue)
        print("Created Jira issue:", new_issue.key)
        return new_issue.key

    def format_description(self, alert, risk_level):
        return f"""
Automated Security Alert

Risk Level: {risk_level}
Vulnerability: {alert.get('name', 'Unknown')}
Affected URL: {alert.get('url', 'N/A')}
Parameter: {alert.get('param', 'N/A')}

Description:
{alert.get('description', 'No description available')}

Solution:
{alert.get('solution', 'No solution provided')}

Reference:
{alert.get('reference', 'No reference available')}

Detection Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Detected By: OWASP ZAP Automated Scanner
"""

    def bulk_create_issues(self):
        with open("security_report.json", "r") as file:
            report = json.load(file)

        created = []

        for alert in report.get("high_risk", []):
            created.append(self.create_security_issue(alert, "High"))

        for alert in report.get("medium_risk", []):
            created.append(self.create_security_issue(alert, "Medium"))

        print("Total Jira issues created:", len(created))

if __name__ == "__main__":
    jira = JiraIntegration()
    jira.bulk_create_issues()
