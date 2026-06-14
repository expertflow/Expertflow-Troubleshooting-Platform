# Jira & Confluence Integration

This skill enables real-time interaction with Atlassian Cloud Jira and Confluence for the Expertflow Troubleshooting Platform.

## Setup

1. Copy `config/atlassian.yaml.template` to `config/atlassian.yaml`
2. Fill in your credentials:
   - `email`: Your Atlassian Cloud account email
   - `token`: An [API token](https://id.atlassian.com/manage-profile/security/api-tokens) (NOT your password)
   - `jira.url`: `https://YOUR-DOMAIN.atlassian.net`
   - `jira.project_key`: e.g., `EF`, `CX`, `SUP`
   - `confluence.url`: `https://YOUR-DOMAIN.atlassian.net/wiki`
   - `confluence.space_key`: e.g., `EF`, `KB`, `DOCS`

## Capabilities

### Search

- **Jira** — Search issues by text or JQL.
  ```python
  from jira_client import JiraClient
  client = JiraClient()
  issues = client.search_text("routing engine")
  issues = client.search_jql('project = EF AND status = "In Progress"')
  ```

- **Confluence** — Search pages by text or CQL.
  ```python
  from confluence_client import ConfluenceClient
  client = ConfluenceClient()
  pages = client.search_text("WhatsApp deployment")
  ```

- **Unified** — Search local repo, Jira, and Confluence in one call.
  ```python
  from search import unified_search
  results = unified_search("email not routing")
  # results["local"] → files in Troubleshooting/
  # results["jira"]   → matching Jira issues
  # results["confluence"] → matching Confluence pages
  ```

### Create / Update

- **Create Bug**
  ```python
  from jira_client import JiraClient
  client = JiraClient()
  bug = client.create_bug(
      summary="Routing Engine zombie state",
      description="Emails not routing due to stale NOT_READY cache...",
      priority="High",
      labels=["troubleshooting", "routing"],
      components=["Routing Engine"],
  )
  print(bug["key"])  # e.g., EF-1234
  ```

- **Add Comment**
  ```python
  client.add_comment("EF-1234", "Fix verified in staging.")
  ```

- **Transition Issue**
  ```python
  client.transition_issue_by_name("EF-1234", "In Progress")
  ```

- **Create Confluence Page**
  ```python
  from confluence_client import ConfluenceClient
  client = ConfluenceClient()
  page = client.create_page(
      title="Runbook: Restart Routing Engine",
      body_storage="<p>Step 1: kubectl delete pod ...</p>",
      parent_id=None,
  )
  ```

### Bug from Case File

If a troubleshooting investigation produces a case file, convert it to a Jira bug:

```python
from create_bug import create_bug_from_case
bug = create_bug_from_case("_bmad-output/implementation-artifacts/investigations/my-case.md")
```

## Workflow

When a user reports an issue:
1. Run `unified_search(query)` to pull context from local repo + Jira + Confluence.
2. Synthesize the answer using all sources.
3. If it is a new bug → ask user → create Jira bug → optionally mirror to Confluence.
4. Commit and push updates to this repo.
