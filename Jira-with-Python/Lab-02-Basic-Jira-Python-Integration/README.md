# Lab 02 - Basic Jira-Python Integration

## Objective

Authenticate Python scripts with Jira REST API and perform basic Jira issue operations such as creating, updating, retrieving, and deleting issues.

## Tools Used

- Ubuntu Linux
- Python 3
- Jira REST API
- Requests
- Python Dotenv
- Git and GitHub

## Project Structure

```text
DevSysOps-Engineering-Labs/
└── Jira-with-Python/
    └── Lab-02-Basic-Jira-Python-Integration/
        ├── README.md
        ├── jira_auth.py
        ├── create_issue.py
        ├── create_multiple_issues.py
        ├── update_issue.py
        ├── retrieve_issues.py
        ├── delete_issue.py
        ├── requirements.txt
        └── .gitignore
Setup
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git nano curl
Virtual Environment
python3 -m venv jira-env
source jira-env/bin/activate
python -m pip install --upgrade pip
pip install requests python-dotenv
pip freeze > requirements.txt
Environment Variables

Create a .env file:

JIRA_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token-here
PROJECT_KEY=TEST
Scripts
Script	Description
jira_auth.py	Tests Jira API authentication
create_issue.py	Creates a Jira issue
create_multiple_issues.py	Creates multiple Jira issues
update_issue.py	Updates an existing issue
retrieve_issues.py	Retrieves issues using JQL
delete_issue.py	Deletes a Jira issue
Run
python jira_auth.py
python create_issue.py
python create_multiple_issues.py
python retrieve_issues.py
python update_issue.py
python delete_issue.py
Outcome

Python was successfully integrated with Jira REST API to authenticate, create issues, retrieve issues, update issues, and delete issues.

Security Note

The .env file is ignored using .gitignore because it contains sensitive Jira credentials.
