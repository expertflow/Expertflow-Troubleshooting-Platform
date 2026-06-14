"""Load Atlassian configuration from config/atlassian.yaml"""
import os
import yaml

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "config", "atlassian.yaml"
)


def load_config():
    """Load and return the atlassian configuration dict."""
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"Config not found at {CONFIG_PATH}. "
            "Please copy config/atlassian.yaml.template to config/atlassian.yaml and fill in your credentials."
        )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_auth():
    """Return (email, token) tuple for Basic Auth."""
    cfg = load_config()
    auth = cfg.get("atlassian", {})
    return auth.get("email"), auth.get("token")


def get_jira_config():
    """Return Jira URL and project key."""
    cfg = load_config()
    jira = cfg.get("jira", {})
    return jira.get("url"), jira.get("project_key")


def get_confluence_config():
    """Return Confluence URL and space key."""
    cfg = load_config()
    conf = cfg.get("confluence", {})
    return conf.get("url"), conf.get("space_key")
