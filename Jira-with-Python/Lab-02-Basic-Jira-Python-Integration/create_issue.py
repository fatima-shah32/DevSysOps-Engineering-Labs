import json
import requests
from jira_auth import JiraClient

class IssueCreator(JiraClient):
    def create_issue(self, summary, description, issue_type="Task"):
        issue_data = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {
                    "name": issue_type
                }
            }
        }

        url = f"{self.base_url}/rest/api/3/issue"

        try:
            response = requests.post(
                url,
                headers=self.headers,
                data=json.dumps(issue_data),
                timeout=20
            )

            if response.status_code == 201:
                issue_info = response.json()
                issue_key = issue_info["key"]

                print("Issue created successfully.")
                print("Issue Key:", issue_key)
                print("Issue URL:", f"{self.base_url}/browse/{issue_key}")
                return issue_key

            print("Failed to create issue:", response.status_code)
            print(response.text)
            return None

        except requests.exceptions.RequestException as error:
            print("Error creating issue:", error)
            return None


if __name__ == "__main__":
    creator = IssueCreator()

    creator.create_issue(
        summary="Python Integration Test Issue",
        description="This issue was created using Python and Jira REST API.",
        issue_type="Task"
    )
