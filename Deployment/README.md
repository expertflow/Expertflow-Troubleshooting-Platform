# 🚀 Deployment Hub

[![Type](https://img.shields.io/badge/Type-Deployment-ff8c00?style=for-the-badge)](.)
[![Platform](https://img.shields.io/badge/Platform-Kubernetes_/_Helm-326ce5?style=for-the-badge&logo=kubernetes&logoColor=white)](.)

> ⚙️ **Deployment guides, integration configurations, connector setup & platform installation references.**

---

## 📂 Directory Structure

```
Deployment/
│
├── 📄 DEPLOYMENT_HISTORY.md            ← Query log of all deployment questions answered
│
├── 📁 Whatsapp-Integration/            ← 💬 Meta Cloud API & native connector guides
│   ├── index.md
│   ├── whatsapp-business-api-setup.md
│   ├── efcx-5.1.0-whatsapp-connector-integration.md
│   └── send-test-message.sh
│
└── 📁 Expertflow-Site/                 ← 🌐 Exported docs.expertflow.com (40+ connectors)
    ├── android-ios/
    ├── campaigns/
    ├── chat/
    ├── cpfg/
    ├── ctrfg/
    ├── cucm/
    ├── cwrfg/
    ├── cx/
    ├── cx-knowledgebase/
    ├── dwb/
    ├── dynamics-web/
    ├── gc/
    ├── hs-efcx-c/
    ├── hubspot-webex/
    ├── inter-chat/
    ├── javascript-cti/
    ├── ms-d-cti-c-efcx/
    ├── msd-cucm/
    ├── msd-genesys/
    ├── msd-usd-cc/
    ├── odoo-efcx/
    ├── odoo-webex/
    ├── pcs/
    ├── salesforce-cti/
    ├── sap-cic/
    ├── sap-efcx/
    ├── sap-genesys-cc/
    ├── sap-webex-cc/
    ├── service-cloud/
    ├── sf-cucm/
    ├── sfcxc/
    ├── sh/
    ├── siebel/
    ├── sn-efcx-c/
    ├── ssasc/
    ├── st/
    ├── suite-cisco/
    ├── suite-webex/
    ├── suitecrm-efcx/
    ├── super-whisper-gadget/
    ├── vr/
    ├── wfms/
    ├── z-c-w/
    ├── zendesk-efcx/
    ├── zoho-c-efcx/
    └── zoho-genesys/
```

---

## 📜 Deployment History

| File | Description |
|:---|:---|
| 📝 [`DEPLOYMENT_HISTORY.md`](DEPLOYMENT_HISTORY.md) | Chronological log of all deployment & configuration questions asked and answered during troubleshooting sessions. |

---

## 💬 Channel Integrations

### WhatsApp

| File | Description |
|:---|:---|
| 📝 [`Whatsapp-Integration/index.md`](Whatsapp-Integration/index.md) | WhatsApp Integration index & quick-start |
| 📝 [`Whatsapp-Integration/whatsapp-business-api-setup.md`](Whatsapp-Integration/whatsapp-business-api-setup.md) | Meta Cloud WhatsApp Business API setup |
| 📝 [`Whatsapp-Integration/efcx-5.1.0-whatsapp-connector-integration.md`](Whatsapp-Integration/efcx-5.1.0-whatsapp-connector-integration.md) | EFCX 5.1.0 native connector integration |
| 🐚 [`Whatsapp-Integration/send-test-message.sh`](Whatsapp-Integration/send-test-message.sh) | Test template-message script |

---

## 🌐 CRM & CTI Connectors

> Exported documentation for 40+ Expertflow connectors. Each folder contains versioned guides in plain-text + HTML.

### Salesforce Ecosystem

| Connector | Versions | Path |
|:---|:---|:---|
| **Salesforce CTI** | `3.1` | [`Expertflow-Site/salesforce-cti/`](Expertflow-Site/salesforce-cti/) |
| **Service Cloud** | `1.0` | [`Expertflow-Site/service-cloud/`](Expertflow-Site/service-cloud/) |
| **SF + CUCM** | `1.0.0` · `1.1.0` | [`Expertflow-Site/sf-cucm/`](Expertflow-Site/sf-cucm/) |
| **SFCXC** | `1.0` · `1.1` · `1.2.0` | [`Expertflow-Site/sfcxc/`](Expertflow-Site/sfcxc/) |
| **SSASC** | `1.0.0` | [`Expertflow-Site/ssasc/`](Expertflow-Site/ssasc/) |

### SAP Ecosystem

| Connector | Versions | Path |
|:---|:---|:---|
| **SAP + EFCX** | `1.0.0` | [`Expertflow-Site/sap-efcx/`](Expertflow-Site/sap-efcx/) |
| **SAP CIC** | `2.2.1` · `2.2.2` | [`Expertflow-Site/sap-cic/`](Expertflow-Site/sap-cic/) |
| **SAP + Genesys CC** | `1.0.0` | [`Expertflow-Site/sap-genesys-cc/`](Expertflow-Site/sap-genesys-cc/) |
| **SAP + Webex CC** | `1.0.0` | [`Expertflow-Site/sap-webex-cc/`](Expertflow-Site/sap-webex-cc/) |

### Microsoft Ecosystem

| Connector | Versions | Path |
|:---|:---|:---|
| **MS Dynamics + CTI + EFCX** | `1.0` | [`Expertflow-Site/ms-d-cti-c-efcx/`](Expertflow-Site/ms-d-cti-c-efcx/) |
| **MSD + CUCM** | `1.0.0` | [`Expertflow-Site/msd-cucm/`](Expertflow-Site/msd-cucm/) |
| **MSD + Genesys** | `1.0.0` | [`Expertflow-Site/msd-genesys/`](Expertflow-Site/msd-genesys/) |
| **MSD + USD CC** | `3.9.2` · `4.3` | [`Expertflow-Site/msd-usd-cc/`](Expertflow-Site/msd-usd-cc/) |

### ServiceNow & Zendesk

| Connector | Versions | Path |
|:---|:---|:---|
| **ServiceNow + EFCX** | `1.0` | [`Expertflow-Site/sn-efcx-c/`](Expertflow-Site/sn-efcx-c/) |
| **ServiceNow (C-SN-C)** | `3.1` | [`Expertflow-Site/c-sn-c/`](Expertflow-Site/c-sn-c/) |
| **Zendesk + EFCX** | `1.0.0` | [`Expertflow-Site/zendesk-efcx/`](Expertflow-Site/zendesk-efcx/) |

### Zoho & Odoo

| Connector | Versions | Path |
|:---|:---|:---|
| **Zoho + EFCX** | `1.0.0` · `2.0.0` | [`Expertflow-Site/zoho-c-efcx/`](Expertflow-Site/zoho-c-efcx/) |
| **Zoho + Genesys** | `1.0.0` | [`Expertflow-Site/zoho-genesys/`](Expertflow-Site/zoho-genesys/) |
| **Odoo + EFCX** | `1.0.0` | [`Expertflow-Site/odoo-efcx/`](Expertflow-Site/odoo-efcx/) |
| **Odoo + Webex** | `1.0.0` | [`Expertflow-Site/odoo-webex/`](Expertflow-Site/odoo-webex/) |

### HubSpot

| Connector | Versions | Path |
|:---|:---|:---|
| **HubSpot + EFCX** | `1.0.0` | [`Expertflow-Site/hs-efcx-c/`](Expertflow-Site/hs-efcx-c/) |
| **HubSpot + Webex** | `1.0.0` | [`Expertflow-Site/hubspot-webex/`](Expertflow-Site/hubspot-webex/) |

### SuiteCRM

| Connector | Versions | Path |
|:---|:---|:---|
| **SuiteCRM + EFCX** | `1.0.0` | [`Expertflow-Site/suitecrm-efcx/`](Expertflow-Site/suitecrm-efcx/) |
| **Suite + Cisco** | `1.0.0` | [`Expertflow-Site/suite-cisco/`](Expertflow-Site/suite-cisco/) |
| **Suite + Webex** | `1.0.0` | [`Expertflow-Site/suite-webex/`](Expertflow-Site/suite-webex/) |

---

## ☎️ Cisco & Genesys Infrastructure

| Connector | Versions | Path |
|:---|:---|:---|
| **CUCM** | `1.0` | [`Expertflow-Site/cucm/`](Expertflow-Site/cucm/) |
| **Siebel** | `3.4.2.5` | [`Expertflow-Site/siebel/`](Expertflow-Site/siebel/) |
| **GC (Genesys Cloud)** | `3.4.1` · `3.4.2` | [`Expertflow-Site/gc/`](Expertflow-Site/gc/) |
| **VR (Verint)** | `14.3` · `14.4` · `14.5` | [`Expertflow-Site/vr/`](Expertflow-Site/vr/) |
| **PCS** | `12.3.2` · `13.0` | [`Expertflow-Site/pcs/`](Expertflow-Site/pcs/) |

---

## 🔧 Gadgets & Utilities

| Connector | Versions | Path |
|:---|:---|:---|
| **Super Whisper Gadget** | `2.1.0` · `2.3.0` | [`Expertflow-Site/super-whisper-gadget/`](Expertflow-Site/super-whisper-gadget/) |
| **CPFG** | `2.1` | [`Expertflow-Site/cpfg/`](Expertflow-Site/cpfg/) |
| **CTRFG** | `1.0` | [`Expertflow-Site/ctrfg/`](Expertflow-Site/ctrfg/) |
| **CWRFG** | `4.0` | [`Expertflow-Site/cwrfg/`](Expertflow-Site/cwrfg/) |
| **ST** | `13.2` · `13.3` · `13.4` | [`Expertflow-Site/st/`](Expertflow-Site/st/) |
| **DWB** | `13.7` · `13.9` | [`Expertflow-Site/dwb/`](Expertflow-Site/dwb/) |
| **WFMS** | `1.0` | [`Expertflow-Site/wfms/`](Expertflow-Site/wfms/) |
| **SH** | `1.0.0` | [`Expertflow-Site/sh/`](Expertflow-Site/sh/) |
| **Z-C-W** | `1.0.0` · `2.0.0` | [`Expertflow-Site/z-c-w/`](Expertflow-Site/z-c-w/) |

---

## 📱 Mobile & Chat

| Connector | Versions | Path |
|:---|:---|:---|
| **Android / iOS** | `3.0` | [`Expertflow-Site/android-ios/`](Expertflow-Site/android-ios/) |
| **Chat** | `3.15` | [`Expertflow-Site/chat/`](Expertflow-Site/chat/) |
| **Inter-Chat** | `1.0` | [`Expertflow-Site/inter-chat/`](Expertflow-Site/inter-chat/) |
| **JavaScript CTI** | `3.0.3` · `3.0.4` · `3.0.5` | [`Expertflow-Site/javascript-cti/`](Expertflow-Site/javascript-cti/) |

---

## 🎯 Campaigns & CX Core

| Connector | Versions | Path |
|:---|:---|:---|
| **Campaigns** | `13.3` | [`Expertflow-Site/campaigns/`](Expertflow-Site/campaigns/) |
| **CX Core** | `4.3` · `4.4` · `4.10` | [`Expertflow-Site/cx/`](Expertflow-Site/cx/) |
| **CX Knowledgebase** | `latest` | [`Expertflow-Site/cx-knowledgebase/`](Expertflow-Site/cx-knowledgebase/) |

---

## 🏷️ Legend

| Icon | Meaning |
|:---|:---|
| 📝 | Markdown guide |
| 🐚 | Shell script |
| 📁 | Directory (contains multiple versioned guides) |

---

*← Back to [root README](../README.md)*
