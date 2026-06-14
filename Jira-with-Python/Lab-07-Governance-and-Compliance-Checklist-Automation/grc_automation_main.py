#!/usr/bin/env python3

import sys
import json

sys.path.append('checks')
sys.path.append('reports')

from grc_checker import GRCChecker
from issue_tracker import IssueTracker


class GRCAutomation:

    def __init__(self):
        self.checker = GRCChecker()
        self.tracker = IssueTracker()

    def run_compliance_scan(self):

        print("Starting GRC Compliance Automation...")
        print("=" * 50)

        self.checker.run_all_checks()

        report = self.checker.generate_report()

        print("\nCompliance Scan Results")
        print("=" * 50)

        print("Total Checks :", report["summary"]["total_checks"])
        print("Passed       :", report["summary"]["passed"])
        print("Failed       :", report["summary"]["failed"])
        print("Errors       :", report["summary"]["errors"])
        print("Compliance   :", report["summary"]["compliance_rate"])

        failed_checks = self.checker.get_failed_checks()

        if failed_checks:

            print("\nCreating Issues For Failed Checks...\n")

            created = self.tracker.create_issues_from_failed_checks(
                failed_checks
            )

            for issue in created:
                print(
                    f"{issue['id']} - "
                    f"{issue['title']} "
                    f"(Priority: {issue['priority']})"
                )

        else:
            print("\nNo Compliance Violations Found")

        with open("reports/grc_report.json", "w") as f:
            json.dump(report, f, indent=2)

        print("\nReport saved to reports/grc_report.json")

    def show_open_issues(self):

        issues = self.tracker.list_open_issues()

        print("\nOpen Issues")
        print("=" * 50)

        if not issues:
            print("No open issues found")
            return

        for issue in issues:
            print(
                f"{issue['id']} | "
                f"{issue['priority']} | "
                f"{issue['title']}"
            )


if __name__ == "__main__":

    app = GRCAutomation()

    app.run_compliance_scan()

    app.show_open_issues()
