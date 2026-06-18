# 🔐 Configuration

[![Type](https://img.shields.io/badge/Type-Config-6c757d?style=for-the-badge)](.)
[![Tool](https://img.shields.io/badge/Tool-Atlassian-0052cc?style=for-the-badge&logo=jira&logoColor=white)](.)

> ⚙️ **Atlassian integration configs, templates & environment setup files.**

---

## 📂 Directory Structure

```
Config/
│
├── 📄 README.md                    ← You are here
├── 🔧 atlassian.json               ← Active Atlassian integration configuration
├── 🔧 atlassian.json.template      ← JSON configuration template
└── ⚙️ atlassian.yaml.template      ← YAML configuration template
```

---

## 📁 Files

| File | Format | Description |
|:---|:---|:---|
| [`atlassian.json`](atlassian.json) | 🔧 JSON | Active Atlassian integration configuration. **Do not commit credentials** unless `.gitignore` is configured to exclude this file. |
| [`atlassian.json.template`](atlassian.json.template) | 🔧 JSON | JSON configuration template — copy this to `atlassian.json` and fill in your values. |
| [`atlassian.yaml.template`](atlassian.yaml.template) | ⚙️ YAML | YAML configuration template — alternative format for Atlassian integrations. |

---

## 🚀 Quick Start

1. Copy the appropriate template:
   ```bash
   cp atlassian.json.template atlassian.json
   # or
   cp atlassian.yaml.template atlassian.yaml
   ```
2. Fill in your Atlassian credentials, base URL, and project keys.
3. Validate syntax before committing:
   ```bash
   python -m json.tool atlassian.json
   # or
   python -c "import yaml; yaml.safe_load(open('atlassian.yaml'))"
   ```

---

## 🔒 Security Note

If you want to hide live credentials from git, uncomment this line in `.gitignore`:

```gitignore
# Config/atlassian.json
```

> ⚠️ **Never commit production credentials to version control.**

---

## 🏷️ Legend

| Icon | Format |
|:---|:---|
| 🔧 | JSON |
| ⚙️ | YAML |

---

*← Back to [root README](../README.md)*
