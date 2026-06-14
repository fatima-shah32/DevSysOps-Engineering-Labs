import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

def run_command(command):
    print("Running:", command)
    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print("Command failed:", command)
        return False

    return True

def main():
    print("Starting Automated Cybersecurity Threat Detection")

    if not os.path.exists("security_report.json"):
        print("Running ZAP scanner first...")
        if not run_command("python zap_scanner.py"):
            return

    print("Creating Jira issues from security report...")
    run_command("python jira_integration.py")

    print("Automation completed.")

if __name__ == "__main__":
    main()
