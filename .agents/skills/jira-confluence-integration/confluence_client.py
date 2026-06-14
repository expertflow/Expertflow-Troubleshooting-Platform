"""Confluence REST API v2 client for Atlassian Cloud."""
import requests
from requests.auth import HTTPBasicAuth
from .config_loader import get_auth, get_confluence_config


class ConfluenceClient:
    def __init__(self):
        self.url, self.space_key = get_confluence_config()
        self.email, self.token = get_auth()
        self.auth = HTTPBasicAuth(self.email, self.token)
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def _request(self, method, endpoint, **kwargs):
        resp = requests.request(
            method,
            f"{self.url}/wiki/api/v2{endpoint}",
            auth=self.auth,
            headers=self.headers,
            **kwargs,
        )
        resp.raise_for_status()
        return resp

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------
    def search_cql(self, cql, limit=20):
        """Execute a CQL query and return pages."""
        resp = self._request("GET", "/pages", params={"limit": limit})
        # CQL search is done via /wiki/rest/api/content/search in v1, but v2 uses /wiki/api/v2/pages with filters.
        # For full CQL we fall back to v1 search endpoint which is more flexible.
        resp = requests.request(
            method="GET",
            url=f"{self.url}/wiki/rest/api/content/search",
            auth=self.auth,
            headers=self.headers,
            params={"cql": cql, "limit": limit, "expand": "body.storage,space,version"},
        )
        resp.raise_for_status()
        return resp.json().get("results", [])

    def search_text(self, text, limit=20):
        """Quick text search inside the configured space."""
        cql = f'text ~ "{text}" AND space = {self.space_key} ORDER BY lastModified DESC'
        return self.search_cql(cql, limit)

    def get_page(self, page_id):
        """Fetch a single page by ID with storage format body."""
        resp = requests.request(
            method="GET",
            url=f"{self.url}/wiki/rest/api/content/{page_id}",
            auth=self.auth,
            headers=self.headers,
            params={"expand": "body.storage,space,version,ancestors"},
        )
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Create / Update
    # ------------------------------------------------------------------
    def create_page(self, title, body_storage, parent_id=None):
        """Create a new page in the configured space."""
        payload = {
            "type": "page",
            "title": title,
            "space": {"key": self.space_key},
            "body": {"storage": {"value": body_storage, "representation": "storage"}},
        }
        if parent_id:
            payload["ancestors"] = [{"id": parent_id}]

        resp = requests.request(
            method="POST",
            url=f"{self.url}/wiki/rest/api/content",
            auth=self.auth,
            headers=self.headers,
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()

    def update_page(self, page_id, title, body_storage, version_number):
        """Update an existing page (must supply next version number)."""
        payload = {
            "type": "page",
            "title": title,
            "body": {"storage": {"value": body_storage, "representation": "storage"}},
            "version": {"number": version_number + 1},
        }
        resp = requests.request(
            method="PUT",
            url=f"{self.url}/wiki/rest/api/content/{page_id}",
            auth=self.auth,
            headers=self.headers,
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()
