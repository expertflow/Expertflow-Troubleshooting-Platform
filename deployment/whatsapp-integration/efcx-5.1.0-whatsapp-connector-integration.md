# EFCX 5.1.0 WhatsApp Connector Integration Guide

> Native `whatsapp-connector` via Meta WhatsApp Cloud API

---

## Step 1: Ensure CX Channels is Deployed

The `whatsapp-connector` is part of the **CX Channels** Helm chart. If channels are not yet deployed:

```bash
helm upgrade --install --namespace expertflow \
  --set global.efCxReleaseName="ef-cx" \
  --debug cx-channels \
  --values helm-values/cx-channels-custom-values.yaml \
  expertflow/channels --version 5.1.0
```

Verify the connector service exists:

```bash
kubectl -n expertflow get svc | grep whatsapp-connector
# Expected output: cx-channels-whatsapp-connector-svc
```

---

## Step 2: Meta Developer Portal Setup

### 2.1 Create Meta App & Add WhatsApp Product

1. Go to [developers.facebook.com](https://developers.facebook.com).
2. Create a new app (Business type).
3. Add the **WhatsApp** product to the app.

### 2.2 Add Business Phone Number

1. In the App Dashboard, navigate to **WhatsApp → API Setup**.
2. Under *Send and receive messages*, add your business phone number in the **From** field.
3. Verify the number — Meta will send a confirmation code via WhatsApp.

### 2.3 Configure Webhook

1. In your App, go to **Add Product → Webhooks**.
2. From the left menu, select **Webhooks**.
3. Choose **WhatsApp Business Account** as the object to subscribe to.
4. Enter the webhook URL:
   ```
   https://{YOUR-CIM-FQDN}/whatsapp-connector/webhook/{Phone-number-ID}
   ```
5. Enter a **Verify Token** of your choice.
6. Click **Verify & Save**.

### 2.4 Generate Long-Lived Page Access Token

1. In the Meta App dashboard, generate a **Long-Lived Page Access Token**.
2. Save this token securely — it is required in Unified Admin.

> **Note:** The token never expires, so store it in a safe place.

---

## Step 3: Configure in EFCX Unified Admin

Log in to **EFCX Unified Admin** and configure the following:

### 3.1 Channel Type

| Field | Value |
|-------|-------|
| Name | `WhatsApp` |
| MRD | Select a suitable MRD |

### 3.2 Channel Provider

| Field | Value |
|-------|-------|
| Name | `WhatsApp Provider` |
| Provider Webhook | `https://{YOUR-CIM-FQDN}/whatsapp-connector` |

### 3.3 Channel Connector

| Field | Value |
|-------|-------|
| Name | `WhatsApp Connector` |
| WHATSAPP-PAGE-ACCESS-TOKEN | Paste the **Long-Lived Page Access Token** from Step 2.4 |
| Verify Token | Enter the same verify token used in Step 2.3 |

### 3.4 Channel

| Field | Value |
|-------|-------|
| Channel Type | `WhatsApp` |
| Channel Connector | `WhatsApp Connector` |

---

## Step 4: Test

1. Send a WhatsApp message to your registered business number.
2. The message should arrive in EFCX as a new conversation.
3. Verify it is routed to the appropriate queue.

---

## Reference

- Source documentation: `docs/expertflow-site/cx/4.5.1/meta-whatsapp-cloud-api-configuration-deployment-g.html`
- Unified Admin guide: `docs/expertflow-site/cx/4.10/unified-admin-guide.html`
