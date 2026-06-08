#!/bin/bash
# WhatsApp Test Message Script
# Usage: ./send-test-message.sh <recipient_phone_number>
# Example: ./send-test-message.sh 923001234567

set -e

# --- CONFIGURE THESE VALUES ---
PHONE_NUMBER_ID="YOUR_PHONE_NUMBER_ID"
ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
TEMPLATE_NAME="order_status_update"  # Must be pre-approved in Meta dashboard
# ------------------------------

RECIPIENT="$1"

if [ -z "$RECIPIENT" ]; then
    echo "Usage: $0 <recipient_phone_number_with_country_code>"
    echo "Example: $0 923001234567"
    exit 1
fi

if [ "$PHONE_NUMBER_ID" = "YOUR_PHONE_NUMBER_ID" ] || [ "$ACCESS_TOKEN" = "YOUR_ACCESS_TOKEN" ]; then
    echo "ERROR: Please edit this script and set PHONE_NUMBER_ID and ACCESS_TOKEN."
    exit 1
fi

echo "Sending test template message to +$RECIPIENT ..."

curl -X POST "https://graph.facebook.com/v18.0/${PHONE_NUMBER_ID}/messages" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"messaging_product\": \"whatsapp\",
    \"recipient_type\": \"individual\",
    \"to\": \"${RECIPIENT}\",
    \"type\": \"template\",
    \"template\": {
      \"name\": \"${TEMPLATE_NAME}\",
      \"language\": {
        \"code\": \"en_US\"
      },
      \"components\": [
        {
          \"type\": \"body\",
          \"parameters\": [
            { \"type\": \"text\", \"text\": \"John Doe\" },
            { \"type\": \"text\", \"text\": \"ORD-12345\" },
            { \"type\": \"text\", \"text\": \"shipped\" }
          ]
        }
      ]
    }
  }"

echo ""
echo "Done."
