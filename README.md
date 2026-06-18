# 🔧 Expertflow Troubleshooting Platform

[![Repo](https://img.shields.io/badge/EFCX-Troubleshooting_Platform-0055ff?style=for-the-badge&logo=github&logoColor=white)](https://github.com/expertflow/expertflow-cx-documentation)
[![Docs](https://img.shields.io/badge/📖_EFCX_Documentation-0a96ba?style=for-the-badge&logo=bookstack&logoColor=white)](https://github.com/expertflow/expertflow-cx-documentation)
[![Status](https://img.shields.io/badge/Status-Active-28a745?style=for-the-badge)](.)
[![Last Updated](https://img.shields.io/badge/Last_Updated-2026--06--18-ff69b4?style=for-the-badge)](.)

> 📚 **Central knowledge base, troubleshooting guides & deployment references for the Expertflow CX platform.**

---

## 🗺️ Repository Structure

This repository is organized into **7 top-level modules**. Each module is self-contained and serves a distinct purpose in the Expertflow CX ecosystem.

```
Expertflow-Troubleshooting-Platform/
│
├── 📁 Troubleshooting/      ← 🐛 Known issues, diagnostic guides & error references
├── 📁 Deployment/           ← 🚀 Deployment guides, connector configs & integration docs
├── 📁 Design-Artifacts/     ← 🎨 Product briefs, UX scenarios & design-system specs
├── 📁 Docs/                 ← 📖 General documentation workspace
├── 📁 Scripts/              ← 🤖 Automation scripts & integration test suites
├── 📁 Config/               ← 🔐 Atlassian templates & environment configuration files
│
├── 📁 _Bmad/                ← 🧠 BMAD agent workspace (internal)
├── 📁 _Bmad-Output/         ← 📦 BMAD output artifacts (internal)
│
└── 📄 README.md             ← You are here
```

---

## 📁 Module Directory

| 📂 Directory | 🏷️ Tags | 📝 Purpose |
|:---|:---|:---|
| **[`Troubleshooting/`](Troubleshooting/)** | `🐛` `🔥` `📋` | Houses **all** known issues, planned-issue lists per CX version, error-message references, and step-by-step diagnostic guides. This is your first stop when something breaks. |
| **[`Deployment/`](Deployment/)** | `🚀` `⚙️` `☸️` | Contains deployment playbooks, connector integration guides (WhatsApp, CRM, CTI), Helm configurations, and the full exported Expertflow documentation site. |
| **[`Design-Artifacts/`](Design-Artifacts/)** | `🎨` `📐` `🧩` | Structured design-to-development pipeline: Product Briefs → Trigger Maps → UX Scenarios → Design System → Development Specs. |
| **[`Docs/`](Docs/)** | `📖` `📝` | Flexible workspace for general documentation, runbooks, and reference material that doesn't fit into the other modules. |
| **[`Scripts/`](Scripts/)** | `🤖` `🐍` | Python and shell scripts for automation, integration testing, and operational tooling. |
| **[`Config/`](Config/)** | `🔐` `⚙️` | Atlassian integration templates (JSON/YAML) and environment-specific configuration files. Copy a template, fill in credentials, and go. |
| **`_Bmad/`** | `🧠` `🤖` | Internal BMAD agent workspace. Contains agent definitions, workflows, skills, and tools for the BMAD framework. |
| **`_Bmad-Output/`** | `📦` `🧪` | Internal BMAD output artifacts: implementation investigations, planning artifacts, and test results. |

---

## 🚀 Quick Access

### 🐛 Troubleshooting

| Category | Files | Badge |
|:---|:---|:---|
| **🔥 Critical Guides** | [`email-not-routing-to-agent.md`](Troubleshooting/email-not-routing-to-agent.md) | ![Critical](https://img.shields.io/badge/Priority-Critical-red?style=flat-square) |
| **📋 Planned Issues** | Version-specific known issues for CX `4.3` → `6.2` | ![Planned](https://img.shields.io/badge/Type-Planned_Issues-blue?style=flat-square) |
| **📖 Error References** | Keycloak, Agent Desk, Connect Errors | ![Reference](https://img.shields.io/badge/Type-Reference-9cf?style=flat-square) |
| **🔗 Integration** | LinkedIn, Cisco, Voice, Whisper Gadget | ![Integration](https://img.shields.io/badge/Type-Integration-green?style=flat-square) |

> 📂 **Explore all:** [`Troubleshooting/`](Troubleshooting/)

### 🚀 Deployment

| Category | Files | Badge |
|:---|:---|:---|
| **📜 History** | [`DEPLOYMENT_HISTORY.md`](Deployment/DEPLOYMENT_HISTORY.md) | ![Log](https://img.shields.io/badge/Type-Log-6f42c1?style=flat-square) |
| **💬 WhatsApp** | Meta Cloud API setup, connector integration | ![WhatsApp](https://img.shields.io/badge/Channel-WhatsApp-25D366?style=flat-square&logo=whatsapp&logoColor=white) |
| **🌐 Integrations** | 40+ CRM/CTI connectors *(see [`Deployment/Expertflow-Site/`](Deployment/Expertflow-Site/))* | ![CRM](https://img.shields.io/badge/Type-CRM_/_CTI-ff8c00?style=flat-square) |

> 📂 **Explore all:** [`Deployment/`](Deployment/)

---

## 🎨 Design Artifacts Pipeline

```
A-Product-Brief  →  B-Trigger-Map  →  C-UX-Scenarios  →  D-Design-System  →  E-Development
   (Why)              (What)              (How)               (Look)              (Build)
```

> 📂 **Explore:** [`Design-Artifacts/`](Design-Artifacts/)

---

## 🔗 Related Resources

[![EFCX Docs](https://img.shields.io/badge/📖_EFCX_Official_Documentation-Expertflow-0a96ba?style=for-the-badge&logo=github)](https://github.com/expertflow/expertflow-cx-documentation)

---

## 🏷️ File Type Legend

| Icon | Extension | Meaning |
|:---|:---|:---|
| 📝 | `.md` | Markdown guide / documentation |
| 🌐 | `.html` | Exported HTML page / web archive |
| 🔧 | `.json` | JSON configuration |
| ⚙️ | `.yaml` / `.yml` | YAML configuration |
| 🐚 | `.sh` | Shell script |
| 🐍 | `.py` | Python script |

---

*Maintained by the Expertflow CX team. Last updated: 2026-06-18.*
