# Lab 04 - Monitoring SysOps Alerts with Python-Jira

## Objective

Set up Prometheus monitoring and integrate it with Jira using Python to automatically create tickets for system alerts.

## Tools Used

- Ubuntu Linux
- Python 3
- Prometheus
- Node Exporter
- Jira Cloud
- Jira Python Library
- Requests
- Python Dotenv

## Project Structure

```text
DevSysOps-Engineering-Labs/
└── Jira-with-Python/
    └── Lab-04-Monitoring-SysOps-Alerts-with-Python-Jira/
        ├── README.md
        ├── jira_alert_integration.py
        ├── test_alerts.py
        ├── requirements.txt
        └── .gitignore
Setup
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git nano wget curl tar net-tools
Python Environment
python3 -m venv venv
source venv/bin/activate
pip install requests jira python-dotenv prometheus-client
pip freeze > requirements.txt
Environment Variables
JIRA_SERVER=https://fatimadanyal123.atlassian.net
JIRA_EMAIL=fatimadanyal123@gmail.com
JIRA_API_TOKEN=your-api-token
JIRA_PROJECT_KEY=KAN
PROMETHEUS_URL=http://localhost:9090
Scripts
Script	Purpose
jira_alert_integration.py	Reads Prometheus alerts and creates Jira tickets
test_alerts.py	Simulates CPU load to trigger alerts
Run
python jira_alert_integration.py
python test_alerts.py
Outcome

Prometheus monitored system alerts successfully, and Python automatically created Jira tickets for active alerts.

Security Note

The .env file is ignored because it contains sensitive Jira credentials.
