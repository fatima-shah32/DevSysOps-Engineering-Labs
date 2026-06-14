import requests
from jira_auth import JiraClient

class IssueRetriever(JiraClient):
    def search_issues(self, jql_query=None, max_results=10):
        if jql_query is None:
            jql_query = f"project = {self.project_key} ORDER BY created DESC"

        url = f"{self.base_url}/rest/api/3/search"

        params = {
            "jql": jql_query,
            "maxResults": max_results,
            "fields": "summary,status,priority,issuetype,created"
        }

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=20
            )

            if response.status_code == 200:
                result = response.json()
                issues = result.get("issues", [])

                print(f"Issues Found: {len(issues)}")

                for issue in issues:
                    fields = issue["fields"]

                    print("-" * 40)
                    print("Key:", issue["key"])
                    print("Summary:", fields.get("summary"))
                    print("Status:", fields.get("status", {}).get("name"))
                    print("Priority:", fields.get("priority", {}).get("name"))
                    print("Type:", fields.get("issuetype", {}).get("name"))

                return issues

            print("Search failed:", response.status_code)
            print(response.text)
            return []

        except requests.exceptions.RequestException as error:
            print("Error searching issues:", error)
            return []


if __name__ == "__main__":
    retriever = IssueRetriever()
    retriever.search_issues()
