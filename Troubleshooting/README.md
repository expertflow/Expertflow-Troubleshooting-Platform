# 🐛 Troubleshooting Hub

[![Type](https://img.shields.io/badge/Type-Troubleshooting-ff4444?style=for-the-badge)](.)
[![Status](https://img.shields.io/badge/Status-Living_Document-28a745?style=for-the-badge)](.)

> 🔥 **Central archive for known issues, error references, diagnostic guides & version-specific planned issues.**

---

## 📂 Directory Structure

```
Troubleshooting/
│
├── 📄 TROUBLESHOOTING_LOG.md               ← Master session log (root causes, resolutions, commands)
├── 📄 email-not-routing-to-agent.md        ← 🔥 Critical: Email routing fix & root cause
│
├── 📋 Planned Issues (per CX version)
│   ├── cx4-3-planned-issues[.html]
│   ├── cx4-4-6-planned-issues[.html]
│   ├── cx4-4-7-planned-issues[.html]
│   ├── ... (CX 4.3 → 6.2)
│   └── _cx4-5-6-planned-issues[.html]
│
├── 📖 General Troubleshooting Guides
│   ├── troubleshooting-guides.html
│   ├── troubleshooting-guide[.html]
│   ├── troubleshooting-and-maintenance[.html]
│   ├── troubleshooting-general-guide.html
│   ├── troubleshooting-for-cx-voice.html
│   ├── troubleshooting-data-platform.html
│   ├── troubleshooting-expertflow-etl-data-platform[.html]
│   ├── troubleshooting-login-errors.html
│   ├── troubleshooting-articles[.html]
│   ├── faqs-and-troubleshooting.html
│   └── all-known-issues.html
│
├── 🔗 Integration-Specific Guides
│   ├── linkedin-integration.html
│   ├── linkedin-social-media.html
│   ├── linkedin-account-onboarding.html
│   ├── linkedin-configuration-guide.html
│   ├── linkedin-connector-configuration-guide.html
│   ├── linkedin-connector-deployment-using-helm.html
│   ├── limitation-issues-in-cisco-integration-for-cx4-0-c[.html]
│   ├── limitation-issues-in-cisco-integration-in-cx4-2[.html]
│   ├── voice-channel-configuration-limitations-issues[.html]
│   ├── whisper-gadget-troubleshooting.html
│   └── supervisor-tools-installation-troubleshooting-guide-windows.html
│
├── ⚠️ Error Reference Guides
│   ├── errors[.html]
│   ├── connect_error[.html]
│   ├── keycloak-error-responses-guide[.html]
│   └── agent-desk-error-messages-guide.html
│
└── 🐳 Infrastructure & Security
    ├── docker-issues-with-firewalld[.html]
    └── ef-cx-component-vulnerability-report-2-0-after-fix.html
```

---

## 📋 Session Log

| File | Description |
|:---|:---|
| 📝 [`TROUBLESHOOTING_LOG.md`](TROUBLESHOOTING_LOG.md) | Master chronological log of every troubleshooting session, including root-cause analyses, resolutions, and diagnostic commands used. |

---

## 🚨 Critical Guides

| File | Symptom | Priority |
|:---|:---|:---|
| 📝 [`email-not-routing-to-agent.md`](email-not-routing-to-agent.md) | Emails not routing while other channels work | ![Critical](https://img.shields.io/badge/-Critical-red) |

---

## 📦 Planned Issues by Version

> Version-specific known-issue lists exported from the Expertflow knowledge base. Each version has both a **plain-text** and an **HTML** export.

### CX 4.x Series

| Version | Plain | HTML |
|:---|:---|:---|
| **4.3** | [`cx4-3-planned-issues`](cx4-3-planned-issues) | [`cx4-3-planned-issues.html`](cx4-3-planned-issues.html) |
| **4.4.5** | [`cx-4-4-5-planned-issues`](cx-4-4-5-planned-issues) | [`cx-4-4-5-planned-issues.html`](cx-4-4-5-planned-issues.html) |
| **4.4.6** | [`cx4-4-6-planned-issues`](cx4-4-6-planned-issues) | [`cx4-4-6-planned-issues.html`](cx4-4-6-planned-issues.html) |
| **4.4.7** | [`cx4-4-7-planned-issues`](cx4-4-7-planned-issues) | [`cx4-4-7-planned-issues.html`](cx4-4-7-planned-issues.html) |
| **4.4.8** | [`cx4-4-8-planned-issues`](cx4-4-8-planned-issues) | [`cx4-4-8-planned-issues.html`](cx4-4-8-planned-issues.html) |
| **4.4.8-1** | [`cx4-4-8-1-planned-issues`](cx4-4-8-1-planned-issues) | [`cx4-4-8-1-planned-issues.html`](cx4-4-8-1-planned-issues.html) |
| **4.4.9** | [`cx4-4-9-planned-issues`](cx4-4-9-planned-issues) | [`cx4-4-9-planned-issues.html`](cx4-4-9-planned-issues.html) |
| **4.4.10** | [`_cx4-4-10-planned-issues`](_cx4-4-10-planned-issues) · [`cx4-4-10-planned-issues`](cx4-4-10-planned-issues) | [`_cx4-4-10-planned-issues.html`](_cx4-4-10-planned-issues.html) · [`cx4-4-10-planned-issues.html`](cx4-4-10-planned-issues.html) |
| **4.4.11** | [`cx4-4-11-planned-issues`](cx4-4-11-planned-issues) | [`cx4-4-11-planned-issues.html`](cx4-4-11-planned-issues.html) |
| **4.4.12** | [`cx4-4-12-planned-issues`](cx4-4-12-planned-issues) | [`cx4-4-12-planned-issues.html`](cx4-4-12-planned-issues.html) |
| **4.4.13** | [`cx4-4-13-planned-issues`](cx4-4-13-planned-issues) | [`cx4-4-13-planned-issues.html`](cx4-4-13-planned-issues.html) |
| **4.4.14** | [`cx4-4-14-planned-issues`](cx4-4-14-planned-issues) | [`cx4-4-14-planned-issues.html`](cx4-4-14-planned-issues.html) |

### CX 5.x Series

| Version | Plain | HTML |
|:---|:---|:---|
| **5.0** | [`_cx4-5-planned-issues`](_cx4-5-planned-issues) | [`_cx4-5-planned-issues.html`](_cx4-5-planned-issues.html) |
| **5.1** | [`cx4-5-1-planned-issues`](cx4-5-1-planned-issues.html) | [`cx4-5-1-planned-issues.html`](cx4-5-1-planned-issues.html) |
| **5.2** | [`_cx4-5-2-planned-issues`](_cx4-5-2-planned-issues) | [`_cx4-5-2-planned-issues.html`](_cx4-5-2-planned-issues.html) |
| **5.3** | [`_cx4-5-3-planned-issues`](_cx4-5-3-planned-issues) | [`_cx4-5-3-planned-issues.html`](_cx4-5-3-planned-issues.html) |
| **5.4** | [`_cx4-5-4-planned-issues`](_cx4-5-4-planned-issues) · [`cx4-5-4-planned-issues`](cx4-5-4-planned-issues) | [`_cx4-5-4-planned-issues.html`](_cx4-5-4-planned-issues.html) · [`cx4-5-4-planned-issues.html`](cx4-5-4-planned-issues.html) |
| **5.5** | [`_cx4-5-5-planned-issues`](_cx4-5-5-planned-issues) | [`_cx4-5-5-planned-issues.html`](_cx4-5-5-planned-issues.html) |
| **5.6** | [`_cx4-5-6-planned-issues`](_cx4-5-6-planned-issues) | [`_cx4-5-6-planned-issues.html`](_cx4-5-6-planned-issues.html) |
| **6.0** | [`_cx4-6-planned-issues`](_cx4-6-planned-issues) | [`_cx4-6-planned-issues.html`](_cx4-6-planned-issues.html) |
| **6.1** | — | [`cx4-6-1-planned-issues.html`](cx4-6-1-planned-issues.html) |
| **6.2** | — | [`cx4-6-2-planned-issues.html`](cx4-6-2-planned-issues.html) |

---

## 🏷️ Legend

| Icon | Meaning |
|:---|:---|
| 📝 | Plain-text / Markdown source |
| 🌐 | Rendered HTML export |

---

*← Back to [root README](../README.md)*
