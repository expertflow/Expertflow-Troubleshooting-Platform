# Deployment & Configuration Query History

> This file tracks all deployment and configuration-related questions asked and answered during troubleshooting sessions.

---

## Session: 2026-06-08

### 1. Download Expertflow Documentation
**Question:** Fetch every detail from https://docs.expertflow.com/
**Answer:** Downloaded the entire docs site (~7,400 files, ~531 MB) into `Deployment/Expertflow-Site/`

### 2. Pods in Expertflow Namespace
**Question:** Tell me about the pods in expertflow namespace
**Answer:** I don't have live cluster access, but found documentation for Kubernetes/Helm deployment guides in the downloaded docs showing the `expertflow` namespace is used for EFCX deployments via Helm charts.

### 3. WhatsApp Integration for EFCX 5.1.0
**Question:** How to integrate WhatsApp for EFCX version 5.1.0 using the native `whatsapp-connector`
**Answer:** Documented step-by-step integration using Meta WhatsApp Cloud API:
- Step 1: Deploy CX Channels Helm chart
- Step 2: Set up Meta App, WhatsApp product, webhook, and generate long-lived token
- Step 3: Configure Channel Type, Channel Provider, Channel Connector, and Channel in EFCX Unified Admin
- Step 4: Test by sending a WhatsApp message to the business number

**Output file:** `Deployment/Whatsapp-Integration/efcx-5.1.0-whatsapp-connector-integration.md`

---

*Add new entries below as more deployment questions are asked.*
