import json
import requests
from jira_auth import JiraClient

class IssueUpdater(JiraClient):
    def update_issue_summary(self, issue_key, new_summary):
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"

        update_data = {
            "fields": {
                "summary": new_summary
            }
        }

        try:
            response = requests.put(
                url,
                headers=self.headers,
                data=json.dumps(update_data),
                timeout=20
            )

            if response.status_code == 204:
                print(f"Issue {issue_key} summary updated successfully.")
                return True

            print("Failed to update issue:", response.status_code)
            print(response.text)
            return False

        except requests.exceptions.RequestException as error:
            print("Error updating issue:", error)
            return False


if __name__ == "__main__":
    issue_key = input("Enter issue key to update, e.g. TEST-1: ").strip()

    updater = IssueUpdater()
    updater.update_issue_summary(
        issue_key,
        "UPDATED: Python Integration Test Issue"
    )
