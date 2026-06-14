#!/usr/bin/env python3

from jira import JIRA
from dotenv import load_dotenv
import os
import sys

load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER", "http://localhost:8080")
JIRA_USERNAME = os.getenv("JIRA_USERNAME", "admin")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD", "your_actual_jira_password")

def test_jira_connection():
    try:
        print("Connecting to Jira server...")

        jira = JIRA(
            server=JIRA_SERVER,
            basic_auth=(JIRA_USERNAME, JIRA_PASSWORD)
        )

        server_info = jira.server_info()

        print("Successfully connected to Jira.")
        print("Jira Version:", server_info.get("version"))
        print("Jira Server Title:", server_info.get("serverTitle"))

        projects = jira.projects()
        print("Projects Found:", len(projects))

        for project in projects:
            print(f"- {project.key}: {project.name}")

        return True

    except Exception as e:
        print("Connection failed:", e)
        print("Make sure Jira is running, setup wizard is completed, and credentials are correct.")
        return False

if __name__ == "__main__":
    success = test_jira_connection()
    sys.exit(0 if success else 1)
