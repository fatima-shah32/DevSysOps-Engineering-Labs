# Lab 06 - Automated Cybersecurity Threat Reporting

## Objective

Set up an automated cybersecurity threat reporting workflow using OWASP ZAP, Python, a vulnerable Flask web application, and Jira.

## Tools Used

- Python 3
- Flask
- OWASP ZAP
- Jira Cloud
- Jira Python Library
- Python Dotenv
- Requests

## Project Structure

```text
Lab-06-Automated-Cybersecurity-Threat-Reporting/
├── README.md
├── vulnerable_app.py
├── zap_scanner.py
├── jira_integration.py
├── automated_threat_detection.py
├── requirements.txt
└── .gitignore
Workflow
Run vulnerable Flask application
Start OWASP ZAP in daemon mode
Scan application using Python ZAP script
Generate security report
Create Jira issues for detected threats
Run Commands
python vulnerable_app.py
/opt/zaproxy/zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true
python zap_scanner.py
python jira_integration.py
Outcome

Successfully automated cybersecurity scanning and generated Jira security tickets for detected vulnerabilities.
