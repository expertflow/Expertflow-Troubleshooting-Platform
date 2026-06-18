# Troubleshooting Log

> Central archive for all troubleshooting outputs, errors, debug logs, and diagnostic sessions.

---

## Session: 2026-06-08

### Summary
Initial session focused on downloading Expertflow documentation, identifying deployment guides, and documenting WhatsApp integration steps for EFCX 5.1.0.

### Issues Encountered
| # | Issue | Resolution |
|---|-------|-----------|
| 1 | `wget` not available on Windows Git Bash | Switched to `curl` with parallel download (`curl -Z`) |
| 2 | Parallel download via `xargs -P` was slow | Replaced with native `curl --parallel-max 50` for 6,982 URLs |
| 3 | Some files had naming conflicts (directory vs file without extension) | Fixed by appending `.html` extension to all paths |
| 4 | Permission errors moving large directories | Used `git mv` for tracked files, `cp -r` + `rm` for untracked |
| 5 | `Docs/Expertflow-Site/cx/4.5.1` could not be removed | Device busy — skipped and cleaned remaining files |

### Key Findings
- **Total docs downloaded:** ~9,100 files (~531 MB)
- **Key doc for WhatsApp:** `Deployment/Expertflow-Site/cx/4.5.1/meta-whatsapp-cloud-api-configuration-deployment-g.html`
- **Key doc for deployment:** `Deployment/Expertflow-Site/cx/5.1.0/deployment-guide.html`
- **Connector service name:** `cx-channels-whatsapp-connector-svc` (Helm-based)

### Commands Used
```bash
# Download all docs
curl -Z --parallel-max 50 --config /tmp/curl_config.txt

# Verify connector service
kubectl -n expertflow get svc | grep whatsapp-connector

# Search for specific terms
grep -ri "whatsapp-connector" Deployment/Expertflow-Site/cx/
```

---

---

## Session: 2026-06-13 — AMQ Artemis Deployment Crashing (JC-23)

### Summary
AMQ Artemis broker (v2.42.0) in CX 5.2.0 crashed with `java.lang.OutOfMemoryError: Java heap space`. The crash caused cascading failures: duplicate messages (20+ duplicates), pod disconnections that never reconnected, and broker-wide instability.

### Root Cause
**JVM heap exhaustion** caused by a combination of insufficient heap sizing and high memory pressure from VirtualTopic consumer churn (temporary queues being created/destroyed repeatedly).

### Affected Components
| Component | Evidence | Suspected Issue |
|---|---|---|
| **Real-time Reporting Manager** | `Consumer.realtime-reporting-manager.VirtualTopic.*` queues auto-removed repeatedly | Crash-looping / disconnecting; recreating temp queues each time |
| **Conversation Manager** | `queue conversation-manager`, `INBOUND_MESSAGE_QUEUE` | Potential message backlog if consumer is slow/dead |
| **CCM Timer Service** | `queue ccm-timers`, `VirtualTopic.cx_sla_timer` | Timer events accumulating rapidly |
| **Agent Desktop / Team Service** | `address team-announcements` | Broadcasting to disconnected sessions |
| **License Manager** | `address LMTopic` | License heartbeat events |

### Problematic Client IPs from Logs
| IP | Symptom |
|---|---|
| `10.109.1.20` | Multiple protocol handshake timeouts, AMQP connection failures |
| `10.109.1.25` | Multiple protocol handshake timeouts |
| `10.109.1.56` | Failed reattach requests (`confirmationWindowSize` not configured) |

> **Action:** Map these IPs to pods with `kubectl get pods -o wide --all-namespaces | grep <IP>`

### Log Indicators
```
AMQ224088: Timeout (10 seconds) on acceptor "artemis" during protocol handshake
AMQ212037: AMQP connection failure ... Java heap space [code=GENERIC_EXCEPTION]
AMQ222066: Reattach request failed as there is no confirmationWindowSize configured
Exception in thread "Thread-27" java.lang.OutOfMemoryError: Java heap space
```

### Resolution Steps
1. **Increase JVM Heap** (Critical)
   ```bash
   -Xms2g -Xmx2g
   ```
   Ensure K8s container limit is higher than `-Xmx` (e.g., `3Gi` limit for `2g` heap).

2. **Tune Broker Memory** in `broker.xml`:
   ```xml
   <global-max-size>1.5GB</global-max-size>
   ```

3. **Enable `confirmationWindowSize`** on acceptors/cluster connections to allow clean reattach:
   ```xml
   <acceptor ...>tcp://...?confirmationWindowSize=1048576;...</acceptor>
   ```

4. **Increase Handshake Timeout** if under connection pressure:
   ```xml
   <acceptor ...>tcp://...?handshakeTimeout=30000;...</acceptor>
   ```

5. **Kubernetes Resources**:
   ```yaml
   resources:
     limits:
       memory: "3Gi"
     requests:
       memory: "2Gi"
   env:
     - name: JAVA_OPTS
       value: "-Xms2g -Xmx2g -XX:+UseG1GC"
   ```

6. **Investigate Client-Side** — Check `realtime-reporting-manager` and `conversation-manager` for connection leaks or crash loops.

### Diagnostic Commands
```bash
# Map IPs to pods
kubectl get pods -o wide --all-namespaces | grep -E "10.109.1.20|10.109.1.25|10.109.1.56"

# Check queue depths
kubectl exec -it <artemis-pod> -- /opt/amq/bin/artemis queue stat --user admin --password admin

# Check for crash loops
kubectl get pods | grep realtime-reporting-manager

# Thread dump
kubectl exec <artemis-pod> -- jstack 1 > /tmp/artemis_threads.txt

# Heap dump (if reproducible)
kubectl exec <artemis-pod> -- jmap -dump:live,format=b,file=/tmp/heap.hprof 1
```

---

*Add new troubleshooting sessions below.*
