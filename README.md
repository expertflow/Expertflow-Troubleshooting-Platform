# Expertflow-Troubleshooting-Platform

Knowledge base and troubleshooting guides for Expertflow CX platform issues.

## Troubleshooting Guides

- [Email Not Routing to Agent — Instant Fix & Root Cause](Troubleshooting/email-not-routing-to-agent.md)
  - **Symptom:** Emails not routing to agents while other channels (Facebook, Chat) work fine.
  - **Instant Fix:** Restart Routing Engine pod or ask agent to toggle Email MRD state.
  - **Root Cause:** Zombie `NOT_READY` state in Routing Engine in-memory cache.
