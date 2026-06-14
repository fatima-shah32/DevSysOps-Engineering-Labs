import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

class JiraClient:
    def __init__(self):
        self.base_url = os.getenv("JIRA_URL")
        self.email = os.getenv("JIRA_EMAIL")
        self.api_token = os.getenv("JIRA_API_TOKEN")
        self.project_key = os.getenv("PROJECT_KEY")

        if not self.base_url or not self.email or not self.api_token or not self.project_key:
            raise ValueError("Missing .env values. Please check JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, PROJECT_KEY.")

        auth_string = f"{self.email}:{self.api_token}"
        auth_bytes = auth_string.encode("ascii")
        auth_b64 = base64.b64encode(auth_bytes).decode("ascii")

        self.headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def test_connection(self):
        url = f"{self.base_url}/rest/api/3/myself"

        try:
            response = requests.get(url, headers=self.headers, timeout=20)

            if response.status_code == 200:
                user_info = response.json()
                print("Successfully connected to Jira.")
                print("User:", user_info.get("displayName"))
                print("Email:", user_info.get("emailAddress"))
                return True

            print("Connection failed:", response.status_code)
            print(response.text)
            return False

        except requests.exceptions.RequestException as error:
            print("Connection error:", error)
            return False


if __name__ == "__main__":
    jira = JiraClient()
    jira.test_connection()
