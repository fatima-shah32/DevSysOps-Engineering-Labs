from create_issue import IssueCreator

def create_sample_issues():
    creator = IssueCreator()

    issues = [
        {
            "summary": "Set up development environment",
            "description": "Install and configure all required tools for the project.",
            "issue_type": "Task"
        },
        {
            "summary": "Login page not responsive on mobile",
            "description": "The login page layout breaks on small mobile screens.",
            "issue_type": "Bug"
        },
        {
            "summary": "Add user profile management feature",
            "description": "Users should be able to update their profile information.",
            "issue_type": "Story"
        }
    ]

    created = []

    for issue in issues:
        issue_key = creator.create_issue(**issue)
        if issue_key:
            created.append(issue_key)

    print("Created Issues:", created)

if __name__ == "__main__":
    create_sample_issues()
