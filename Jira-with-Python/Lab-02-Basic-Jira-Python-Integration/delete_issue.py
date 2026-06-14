import requests
from jira_auth import JiraClient

class IssueDeleter(JiraClient):
    def delete_issue(self, issue_key):
        confirm = input(f"Type DELETE to confirm deletion of {issue_key}: ").strip()

        if confirm != "DELETE":
            print("Deletion cancelled.")
            return False

        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"

        try:
            response = requests.delete(
                url,
                headers=self.headers,
                timeout=20
            )

            if response.status_code == 204:
                print(f"Issue {issue_key} deleted successfully.")
                return True

            print("Failed to delete issue:", response.status_code)
            print(response.text)
            return False

        except requests.exceptions.RequestException as error:
            print("Error deleting issue:", error)
            return False


if __name__ == "__main__":
    issue_key = input("Enter issue key to delete, e.g. TEST-1: ").strip()

    deleter = IssueDeleter()
    deleter.delete_issue(issue_key)
