#!/usr/bin/env python3
"""Quick validation script for Jira + Confluence connectivity."""
import sys
import os

# Ensure the skill package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".agents", "skills", "jira-confluence-integration"))

from jira_client import JiraClient
from confluence_client import ConfluenceClient


def test_jira():
    print("\n=== Jira Test ===")
    client = JiraClient()
    print(f"URL: {client.url}")
    print(f"Project: {client.project_key}")
    if client.project_key == "YOUR-PROJECT-KEY":
        print("WARNING: project_key is still a placeholder. Update config/atlassian.json with your real project key.")

    # Try a lightweight search
    try:
        issues = client.search_jql(f"project = {client.project_key} ORDER BY created DESC", max_results=3)
        print(f"Connection OK. Found {len(issues)} recent issues.")
        for i in issues:
            print(f"  - {i['key']}: {i['fields'].get('summary')}")
    except Exception as e:
        print(f"ERROR: {e}")


def test_confluence():
    print("\n=== Confluence Test ===")
    client = ConfluenceClient()
    print(f"URL: {client.url}")
    print(f"Space: {client.space_key}")
    if client.space_key == "YOUR-SPACE-KEY":
        print("WARNING: space_key is still a placeholder. Update config/atlassian.json with your real space key.")

    try:
        pages = client.search_cql(f"space = {client.space_key} ORDER BY lastModified DESC", limit=3)
        print(f"Connection OK. Found {len(pages)} recent pages.")
        for p in pages:
            print(f"  - {p.get('id')}: {p.get('title')}")
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    test_jira()
    test_confluence()
