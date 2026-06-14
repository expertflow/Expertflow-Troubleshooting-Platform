"""Unified search across local repo, Jira, and Confluence."""
import os
import subprocess
from .jira_client import JiraClient
from .confluence_client import ConfluenceClient

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")


def search_local(query, max_results=10):
    """Grep the local Troubleshooting/ and deployment/ directories."""
    dirs = ["Troubleshooting", "deployment", "docs"]
    hits = []
    for d in dirs:
        path = os.path.join(REPO_ROOT, d)
        if not os.path.isdir(path):
            continue
        try:
            result = subprocess.run(
                ["grep", "-ri", "-l", query, path],
                capture_output=True,
                text=True,
                timeout=10,
            )
            files = result.stdout.strip().split("\n")[:max_results]
            for f in files:
                if f:
                    hits.append({"source": "local", "type": "file", "path": f})
        except Exception:
            continue
    return hits


def search_jira(query, max_results=10):
    """Search Jira via text/JQL."""
    try:
        client = JiraClient()
        issues = client.search_text(query, max_results)
        return [
            {
                "source": "jira",
                "type": "issue",
                "key": i["key"],
                "summary": i["fields"].get("summary", ""),
                "status": i["fields"].get("status", {}).get("name", ""),
                "priority": i["fields"].get("priority", {}).get("name", ""),
                "url": f"{client.url}/browse/{i['key']}",
            }
            for i in issues
        ]
    except Exception as e:
        return [{"source": "jira", "type": "error", "message": str(e)}]


def search_confluence(query, max_results=10):
    """Search Confluence via CQL."""
    try:
        client = ConfluenceClient()
        pages = client.search_text(query, max_results)
        return [
            {
                "source": "confluence",
                "type": "page",
                "id": p.get("id"),
                "title": p.get("title", ""),
                "url": f"{client.url}/wiki/spaces/{client.space_key}/pages/{p.get('id')}",
            }
            for p in pages
        ]
    except Exception as e:
        return [{"source": "confluence", "type": "error", "message": str(e)}]


def unified_search(query, max_per_source=10):
    """Search local repo, Jira, and Confluence simultaneously."""
    return {
        "local": search_local(query, max_per_source),
        "jira": search_jira(query, max_per_source),
        "confluence": search_confluence(query, max_per_source),
    }
