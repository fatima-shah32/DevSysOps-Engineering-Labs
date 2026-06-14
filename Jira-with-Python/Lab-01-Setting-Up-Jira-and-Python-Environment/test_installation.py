#!/usr/bin/env python3

try:
    from jira import JIRA
    import requests
    import pandas as pd

    print("All required libraries installed successfully.")
    print("JIRA library available.")
    print("Requests library available.")
    print("Pandas library available.")

except ImportError as e:
    print("Import error:", e)
