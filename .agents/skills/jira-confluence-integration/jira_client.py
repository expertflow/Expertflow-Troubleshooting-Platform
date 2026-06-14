"""Jira REST API v3 client for Atlassian Cloud."""
import requests
from requests.auth import HTTPBasicAuth
from .config_loader import get_auth, get_jira_config


class JiraClient:
    def __init__(self):
        self.url, self.project_key = get_jira_config()
        self.email, self.token = get_auth()
        self.auth = HTTPBasicAuth(self.email, self.token)
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def _request(self, method, endpoint, **kwargs):
        resp = requests.request(
            method,
            f"{self.url}/rest/api/3{endpoint}",
            auth=self.auth,
            headers=self.headers,
            **kwargs,
        )
        resp.raise_for_status()
        return resp

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------
    def search_jql(self, jql, max_results=20):
        """Execute a JQL query and return a list of issues."""
        payload = {"jql": jql, "maxResults": max_results, "fields": ["summary", "status", "priority", "assignee", "created", "updated", "description", "labels", "components"],}
        resp = self._request("POST", "/search", json=payload)
        return resp.json().get("issues", [])

    def search_text(self, text, max_results=20):
        """Quick text search across the configured project."""
        jql = f'text ~ "{text}" AND project = {self.project_key} ORDER BY updated DESC'
        return self.search_jql(jql, max_results)

    def get_issue(self, issue_key):
        """Fetch a single issue by key (e.g. EF-123)."""
        resp = self._request("GET", f"/issue/{issue_key}")
        return resp.json()

    # ------------------------------------------------------------------
    # Create / Update
    # ------------------------------------------------------------------
    def create_bug(self, summary, description, priority=None, labels=None, components=None):
        """Create a Bug issue in the configured project."""
        fields = {
            "project": {"key": self.project_key},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}],
                    }
                ],
            },
            "issuetype": {"name": "Bug"},
            "labels": labels or ["troubleshooting", "auto-generated"],
        }
        if priority:
            fields["priority"] = {"name": priority}
        if components:
            fields["components"] = [{"name": c} for c in components]

        resp = self._request("POST", "/issue", json={"fields": fields})
        return resp.json()

    def add_comment(self, issue_key, body):
        """Add a comment to an existing issue."""
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": body}],
                    }
                ],
            }
        }
        resp = self._request("POST", f"/issue/{issue_key}/comment", json=payload)
        return resp.json()

    # ------------------------------------------------------------------
    # Transitions
    # ------------------------------------------------------------------
    def get_transitions(self, issue_key):
        """List available transitions for an issue."""
        resp = self._request("GET", f"/issue/{issue_key}/transitions")
        return resp.json().get("transitions", [])

    def transition_issue(self, issue_key, transition_id):
        """Move an issue to a new status via transition ID."""
        payload = {"transition": {"id": transition_id}}
        self._request("POST", f"/issue/{issue_key}/transitions", json=payload)

    def transition_issue_by_name(self, issue_key, transition_name):
        """Find transition by name and execute it."""
        transitions = self.get_transitions(issue_key)
        for t in transitions:
            if t["name"].lower() == transition_name.lower():
                self.transition_issue(issue_key, t["id"])
                return t
        raise ValueError(f"Transition '{transition_name}' not found for {issue_key}")
