"""Bug creation workflow tied to case files."""
import os
import re
from datetime import datetime
from .jira_client import JiraClient
from .confluence_client import ConfluenceClient


def extract_case_metadata(case_file_path):
    """Parse a Markdown case file for summary, root cause, component, severity."""
    with open(case_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    def _extract(pattern, default=""):
        m = re.search(pattern, content, re.IGNORECASE)
        return m.group(1).strip() if m else default

    return {
        "summary": _extract(r"##?\s*Summary\s*\n+(.+?)(?:\n##|\n\n|$)"),
        "root_cause": _extract(r"##?\s*Root Cause\s*\n+(.+?)(?:\n##|\n\n|$)"),
        "component": _extract(r"##?\s*Affected Component\s*\n+(.+?)(?:\n##|\n\n|$)"),
        "severity": _extract(r"##?\s*Severity\s*\n+(.+?)(?:\n##|\n\n|$)"),
        "reproduction": _extract(r"##?\s*Reproduction Steps\s*\n+(.+?)(?:\n##|\n\n|$)"),
    }


def create_bug_from_case(case_file_path, labels=None, push_to_confluence=False):
    """Create a Jira Bug from a case file and optionally mirror it to Confluence."""
    meta = extract_case_metadata(case_file_path)
    jira = JiraClient()

    summary = meta["summary"] or os.path.basename(case_file_path)
    description = (
        f"*Root Cause:*\n{meta['root_cause']}\n\n"
        f"*Reproduction Steps:*\n{meta['reproduction']}\n\n"
        f"*Source case file:* {case_file_path}\n"
        f"*Auto-generated:* {datetime.utcnow().isoformat()}Z"
    )

    bug = jira.create_bug(
        summary=summary,
        description=description,
        priority=meta.get("severity") or "Medium",
        labels=labels or ["troubleshooting", "auto-generated"],
        components=[meta["component"]] if meta.get("component") else None,
    )

    if push_to_confluence and bug.get("key"):
        conf = ConfluenceClient()
        title = f"[{bug['key']}] {summary}"
        body = (
            f"<h1>{summary}</h1>"
            f"<p><strong>Jira:</strong> <a href=\"{jira.url}/browse/{bug['key']}\">{bug['key']}</a></p>"
            f"<p><strong>Root Cause:</strong> {meta['root_cause']}</p>"
            f"<p><strong>Reproduction:</strong></p><pre>{meta['reproduction']}</pre>"
        )
        conf.create_page(title, body)

    return bug


def quick_bug(summary, description, priority="Medium", labels=None):
    """Create a bug directly without a case file."""
    jira = JiraClient()
    return jira.create_bug(
        summary=summary,
        description=description,
        priority=priority,
        labels=labels or ["troubleshooting", "auto-generated"],
    )
