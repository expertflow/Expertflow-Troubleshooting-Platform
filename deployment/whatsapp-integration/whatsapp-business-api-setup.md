# WhatsApp Business API Setup Guide

> **Goal:** Configure Meta Cloud WhatsApp Business API to send notifications and alerts.
> **Scope:** End-to-end setup from Meta Developer account to first message.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Create a Meta App](#2-create-a-meta-app)
3. [Set Up WhatsApp Product](#3-set-up-whatsapp-product)
4. [Get API Credentials](#4-get-api-credentials)
5. [Add a Phone Number](#5-add-a-phone-number)
6. [Create Message Templates](#6-create-message-templates)
7. [Send Your First Message](#7-send-your-first-message)
8. [Spring Boot Integration](#8-spring-boot-integration)
9. [Webhook Configuration](#9-webhook-configuration)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

Before you start, ensure you have:

| Requirement | Why You Need It |
|-------------|-----------------|
| **Meta Business Account** | Required to own and manage the WhatsApp Business Account. [Create here](https://business.facebook.com/) |
| **Facebook Developer Account** | Required to create apps and access the Graph API. [Sign up](https://developers.facebook.com/) |
| **A phone number** | Must not be already registered on WhatsApp (use a new number or unregister an existing one). |
| **Verified Meta Business** | For production use, Meta requires business verification. Testing works without it. |

---

## 2. Create a Meta App

1. Go to [Meta Developers](https://developers.facebook.com/apps/)
2. Click **"Create App"**
3. Select app type: **"Business"**
4. Fill in:
   - **App Name:** `Expertflow-WhatsApp-Connector` (or your preferred name)
   - **App Contact Email:** your business email
   - **Business Account:** select your Meta Business Account
5. Click **"Create App"**

---

## 3. Set Up WhatsApp Product

1. On your new app's dashboard, scroll to **"Add Products"**
2. Find **"WhatsApp"** and click **"Set Up"**
3. You will be taken to the **WhatsApp > Getting Started** page
4. A **test phone number** is auto-created for you (e.g., `+1 555 123 4567`)

> **Note:** The test number lets you send messages to **up to 5 phone numbers** without business verification. For production, you must add your own number.

---

## 4. Get API Credentials

On the **WhatsApp > Getting Started** page, locate:

### 4.1 Phone Number ID

```
Phone Number ID: 123456789012345
```

This identifies the sender.

### 4.2 WhatsApp Business Account ID (WABA ID)

```
WhatsApp Business Account ID: 987654321098765
```

This identifies your business account.

### 4.3 Generate a Permanent Access Token

**Do NOT use the temporary token from the Getting Started page in production.**

To create a permanent token:

1. Go to **Meta Business Suite** > **System Users**
2. Click **"Add"** to create a new System User
3. Assign the user to your WhatsApp app with **"WhatsApp Business Management"** and **"WhatsApp Business Messaging"** roles
4. Click **"Generate Token"**
5. Select your app, check **"whatsapp_business_messaging"** and **"whatsapp_business_management"**
6. Copy the token and store it securely (this token does not expire)

---

## 5. Add a Phone Number

### 5.1 Test Number (Immediate)

Use the auto-generated test number. You can send to **5 recipient numbers**.

### 5.2 Your Own Number (Production)

1. In the Meta App dashboard, go to **WhatsApp > Phone Numbers**
2. Click **"Add Phone Number"**
3. Select your **WhatsApp Business Account**
4. Enter your phone number
5. Verify via SMS or voice call
6. Complete **2FA setup**
7. Wait for Meta approval (usually instant for new numbers)

> ⚠️ **Important:** The phone number will be removed from any existing WhatsApp (personal or business) app.

---

## 6. Create Message Templates

**You cannot send free-form messages to customers who have not messaged you in the last 24 hours.** For notifications, you **must** use **pre-approved Message Templates**.

### 6.1 Create a Template via Meta Dashboard

1. Go to **WhatsApp > Message Templates**
2. Click **"Create Template"**
3. Fill in:
   - **Category:** `UTILITY` (for notifications, alerts, order updates)
   - **Name:** `order_status_update` (use `snake_case`)
   - **Language:** `en_US`
4. In the body, write:
   ```
   Hello {{1}}, your order #{{2}} is now {{3}}. Thank you for choosing us!
   ```
5. Submit for review. Approval usually takes minutes to a few hours.

### 6.2 Template Variables

| Variable | Description |
|----------|-------------|
| `{{1}}` | Customer name |
| `{{2}}` | Order number |
| `{{3}}` | Status (e.g., "shipped", "delivered") |

---

## 7. Send Your First Message

### 7.1 Using cURL (Test)

Replace placeholders with your actual values:

```bash
curl -X POST "https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages" \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "{RECIPIENT_PHONE_NUMBER}",
    "type": "template",
    "template": {
      "name": "order_status_update",
      "language": {
        "code": "en_US"
      },
      "components": [
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": "John Doe"
            },
            {
              "type": "text",
              "text": "ORD-12345"
            },
            {
              "type": "text",
              "text": "shipped"
            }
          ]
        }
      ]
    }
  }'
```

**Expected response:**
```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "{RECIPIENT_PHONE_NUMBER}", "wa_id": "..."}],
  "messages": [{"id": "wamid.XXX..."}]
}
```

### 7.2 Sending Free-Form Messages (Within 24h Window)

If the user has recently messaged you, you can send a text message directly:

```bash
curl -X POST "https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages" \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "{RECIPIENT_PHONE_NUMBER}",
    "type": "text",
    "text": {
      "body": "Hello! How can we help you today?"
    }
  }'
```

---

## 8. Spring Boot Integration

### 8.1 Add Dependencies

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

### 8.2 Configuration

```yaml
whatsapp:
  api-url: https://graph.facebook.com/v18.0
  phone-number-id: ${WHATSAPP_PHONE_NUMBER_ID}
  access-token: ${WHATSAPP_ACCESS_TOKEN}
```

### 8.3 Service Class

```java
@Service
public class WhatsAppService {

    @Value("${whatsapp.api-url}")
    private String apiUrl;

    @Value("${whatsapp.phone-number-id}")
    private String phoneNumberId;

    @Value("${whatsapp.access-token}")
    private String accessToken;

    private final WebClient webClient;

    public WhatsAppService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.baseUrl(apiUrl).build();
    }

    public Mono<String> sendTemplateMessage(String to, String templateName, List<String> params) {
        Map<String, Object> body = new HashMap<>();
        body.put("messaging_product", "whatsapp");
        body.put("recipient_type", "individual");
        body.put("to", to);
        body.put("type", "template");

        List<Map<String, Object>> parameters = params.stream()
            .map(p -> Map.of("type", "text", "text", p))
            .collect(Collectors.toList());

        body.put("template", Map.of(
            "name", templateName,
            "language", Map.of("code", "en_US"),
            "components", List.of(Map.of(
                "type", "body",
                "parameters", parameters
            ))
        ));

        return webClient.post()
            .uri("/{phoneNumberId}/messages", phoneNumberId)
            .header("Authorization", "Bearer " + accessToken)
            .bodyValue(body)
            .retrieve()
            .bodyToMono(String.class);
    }

    public Mono<String> sendTextMessage(String to, String message) {
        Map<String, Object> body = Map.of(
            "messaging_product", "whatsapp",
            "recipient_type", "individual",
            "to", to,
            "type", "text",
            "text", Map.of("body", message)
        );

        return webClient.post()
            .uri("/{phoneNumberId}/messages", phoneNumberId)
            .header("Authorization", "Bearer " + accessToken)
            .bodyValue(body)
            .retrieve()
            .bodyToMono(String.class);
    }
}
```

### 8.4 REST Controller

```java
@RestController
@RequestMapping("/api/whatsapp")
public class WhatsAppController {

    private final WhatsAppService whatsAppService;

    public WhatsAppController(WhatsAppService whatsAppService) {
        this.whatsAppService = whatsAppService;
    }

    @PostMapping("/send-notification")
    public Mono<ResponseEntity<String>> sendNotification(
            @RequestBody NotificationRequest request) {
        return whatsAppService.sendTemplateMessage(
                request.getPhoneNumber(),
                request.getTemplateName(),
                request.getParameters()
            )
            .map(ResponseEntity::ok)
            .onErrorResume(e -> Mono.just(
                ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error: " + e.getMessage())
            ));
    }
}
```

### 8.5 Request DTO

```java
public class NotificationRequest {
    private String phoneNumber;
    private String templateName;
    private List<String> parameters;

    // getters and setters
}
```

---

## 9. Webhook Configuration

To receive message status updates (delivered, read, failed) and incoming messages, configure a webhook.

### 9.1 In Your Meta App

1. Go to **WhatsApp > Configuration**
2. Under **Webhooks**, click **"Edit"**
3. Enter your callback URL:
   ```
   https://your-domain.com/api/whatsapp/webhook
   ```
4. Enter a **Verify Token** (a secret string you choose)
5. Click **"Verify and Save"**

### 9.2 Spring Boot Webhook Verification

```java
@GetMapping("/webhook")
public ResponseEntity<String> verifyWebhook(
        @RequestParam("hub.mode") String mode,
        @RequestParam("hub.verify_token") String token,
        @RequestParam("hub.challenge") String challenge) {

    if ("subscribe".equals(mode) && "YOUR_VERIFY_TOKEN".equals(token)) {
        return ResponseEntity.ok(challenge);
    }
    return ResponseEntity.status(HttpStatus.FORBIDDEN).body("Verification failed");
}
```

### 9.3 Handle Incoming Events

```java
@PostMapping("/webhook")
public ResponseEntity<Void> receiveWebhook(@RequestBody Map<String, Object> payload) {
    // Parse payload for message status, incoming messages, etc.
    // Log or process as needed
    return ResponseEntity.ok().build();
}
```

### 9.4 Subscribe to Webhook Fields

After verifying, subscribe to these fields:
- `messages` — incoming messages
- `message_statuses` — delivery/read/failed status

---

## 10. Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `AuthenticationError` | Invalid or expired access token | Regenerate a permanent token |
| `InvalidRecipient` | Phone number not in allowed list (test mode) | Add recipient in Getting Started, or switch to production |
| `TemplateNotFound` | Template name incorrect or not approved | Verify template name and approval status |
| `Undeliverable` | Recipient has blocked the number or is unreachable | Retry later or contact user |
| `RateLimit` | Too many messages sent too fast | Implement rate limiting; check Meta's rate limits |
| `NoResourceFoundException` | Wrong API version or URL | Verify `v18.0` and `PHONE_NUMBER_ID` |

---

## Next Steps

1. ✅ Complete the Meta App and WhatsApp setup above.
2. ✅ Add your phone number (test with auto-generated number first).
3. ✅ Create your first message template and get it approved.
4. ✅ Send a test message via cURL to confirm everything works.
5. ✅ Implement the Spring Boot service (use the code above).
6. ✅ Configure the webhook to receive delivery receipts.

**Need help with a specific step or want me to generate the full Spring Boot project?** Let me know.
