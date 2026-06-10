# Email Not Routing to Agent — Instant Fix & Root Cause

> **Issue ID:** ROUTING-EMAIL-NOT_READY-ZOMBIE  
> **System:** Expertflow CX Media Routing Engine  
> **Last Updated:** 2026-06-10

---

## ⚡ INSTANT FIX (30 Seconds)

If emails are not routing to a specific agent (or all agents) and other channels (Facebook, Chat, etc.) work fine:

### Option 1: Restart Routing Engine Pod (Fastest — No Agent Action Needed)

```bash
# Kubernetes
kubectl rollout restart deployment <routing-engine-deployment> -n <namespace>

# Or delete the pod (it will recreate automatically)
kubectl delete pod <routing-engine-pod-name> -n <namespace>
```

**Why this works:** The Routing Engine holds agent MRD states in-memory. A restart wipes stale cache and rebuilds it correctly from the database/Redis.

### Option 2: Ask Agent to Toggle Email MRD State (If Restart Not Possible)

1. Agent opens **Agent Desk / Dashboard**
2. Finds the **EMAIL** channel/MRD control
3. Clicks **NOT_READY** → selects any reason → immediately clicks **READY**
4. This forces a state-change event that re-evaluates the in-memory cache

**Note:** Option 1 is more reliable if the state is deeply stuck.

---

## 🔍 How to Confirm This Is the Issue

Check Routing Engine logs for the affected agent:

```bash
kubectl logs <routing-engine-pod> -n <namespace> --tail=500 | grep -i "EMAIL\|agent 2690\|08fe55fb-5bdd-46ef-ab2c-a0940476ace3"
```

**Look for this pattern:**

```json
AgentMrdState(
  mrd=MediaRoutingDomain(id=6305de07166ba1099d11a889, name=EMAIL),
  state=NOT_READY,
  previousState=READY,
  stateChangeTime=2026-06-10 03:00:20.130...   <-- STUCK FOR HOURS
)
```

If `state=NOT_READY` and `stateChangeTime` is hours old while other MRDs (Facebook, Chat) are changing normally → **this is the issue.**

---

## 🧠 Root Cause Analysis

### What Happened

1. **Trigger:** A race condition or missed AMQ event during agent login/session init flipped the EMAIL MRD to `NOT_READY` in the Routing Engine's **in-memory cache**.
2. **Deadlock:** Because EMAIL was `NOT_READY` in memory, the engine never offered email tasks to that agent.
3. **No Recovery:** Because no email tasks were offered, there were zero email task events (no assign, wrap-up, close). The `AgentMrdStateListener` only re-evaluates reactively on task events.
4. **Result:** The EMAIL MRD stayed `NOT_READY` forever — a **zombie state** — while other MRDs (Facebook, Chat, etc.) kept getting "poked" by task events and stayed healthy.

```
NOT_READY (bad in-memory state)
    ↓
No email tasks routed
    ↓
No email task events
    ↓
No state re-evaluation triggered
    ↓
NOT_READY forever (zombie)
```

### Why Only Email Was Affected

| MRD | Task Traffic | State Evaluated? | Status |
|-----|------------|------------------|--------|
| Facebook | High | Every few minutes | Healthy |
| Chat | High | Every few minutes | Healthy |
| **Email** | **Zero** (blocked by NOT_READY) | **Never** | **Zombie** |

Other MRDs had constant task churn which repeatedly triggered `changeStateOnMediaClose`, `reserve`, and `updateState`. Email had no such triggers once stuck.

### Key Log Evidence

```
# Facebook MRD keeps transitioning
08:36:07.461  MRD state changed from: BUSY to: ACTIVE | MRD: Facebook
08:36:07.580  MRD state changed from: ACTIVE to: RESERVED | MRD: Facebook

# Email MRD unchanged for 5+ hours
08:36:07.462  state=NOT_READY, previousState=READY, stateChangeTime=03:00:20
```

---

## 🛡️ Prevention & Monitoring

### Monitoring Query

Set up an alert if any agent's MRD state is `NOT_READY` without a `reasonCode` for > 15 minutes:

```bash
# Log-based alert (example)
grep "AgentMrdState" routing-engine.log \
  | grep "name=EMAIL" \
  | grep "state=NOT_READY" \
  | grep -v "reasonCode"
```

### Long-Term Fixes (Engineering)

1. **Periodic State Reconciliation** — Routing Engine should sweep agent MRD states against DB every N minutes to catch orphaned `NOT_READY` states.
2. **Force Re-eval on Main Agent READY** — When `agentStateChanged=true` and main state is `READY`, validate ALL `isAutoSync=true` MRDs, not just recently active ones.
3. **Audit AMQ Consumer Lag** — Check for missed/dropped `AGENT_STATE_CHANGED` events on `VirtualTopic.STATE_CHANNEL` during high load.

---

## 📋 Quick Diagnostic Checklist

| Check | Command / Location | Expected |
|-------|-------------------|----------|
| Agent has Email routing attribute | Unified Admin > Agent Profile | Value = 1 / Enabled |
| Agent associated with Email MRD | Unified Admin > Agent Profile | MRD listed |
| Email Queue exists and has tasks | Routing Engine logs / Admin UI | Queue size > 0 |
| **Agent EMAIL MRD state in Engine** | **Routing Engine logs** | **Should be READY, not NOT_READY** |
| Agent's view in Agent Desk | Ask agent | Should match Engine state |

**If first 3 are ✅ but Engine shows `NOT_READY` → Restart Routing Engine pod.**

---

## Related Issues

- [Agent Desk Error Messages Guide](agent-desk-error-messages-guide.html)
- [Troubleshooting General Guide](troubleshooting-general-guide.html)

---

*Document created by Kimi Code CLI based on live log analysis. Issue confirmed resolved by Routing Engine pod restart on 2026-06-10.*
