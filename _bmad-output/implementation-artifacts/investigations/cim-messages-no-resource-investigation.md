# Investigation: cim-messages — No Static Resource Error

## Hand-off Brief

1. **What happened.** A POST request to `cim-messages` on the LinkedIn connector service (port 9001) threw `NoResourceFoundException`, meaning Spring treated it as a static resource request instead of routing it to a controller.
2. **Where the case stands.** Stronghold established: the exact error, timestamp, and request ID are confirmed. The endpoint is not registered in Spring's handler map. The service is `ClusterIP` with no ingress; the caller reaches the pod directly.
3. **What's needed next.** Inspect source code for the `cim-messages` controller mapping, verify active Spring profiles, and confirm the exact URL the caller should use.

## Case Info

| Field            | Value                                                                      |
| ---------------- | -------------------------------------------------------------------------- |
| Ticket           | N/A                                                                        |
| Date opened      | 2026-06-08                                                                 |
| Status           | Active                                                                     |
| System           | Spring Boot application (LinkedIn Connector), port 9001, Java 21, K8s ClusterIP |
| Evidence sources | Log snippet provided by user (stdout/stderr), K8s service/ingress inventory |

## Problem Statement

A POST request to `/cim-messages` on the LinkedIn connector service results in a `NoResourceFoundException: No static resource cim-messages`. The user expects this endpoint to be handled by application code, but Spring's `ResourceHttpRequestHandler` is attempting to serve it as a static resource instead.

## Evidence Inventory

| Source               | Status    | Notes                                                                                |
| -------------------- | --------- | ------------------------------------------------------------------------------------ |
| Application log      | Available | Single log snippet with error trace, timestamp 2026-06-08 10:56:33.593, req ID c7156dae-9255-421a-8485-5a1410516098 |
| Source code          | Missing   | Project source not yet located in working directory                                  |
| Issue tracker        | Missing   | No ticket ID provided                                                                |
| Version control      | Missing   | Commit range unknown                                                                 |
| Test results         | Missing   | No test output provided                                                              |
| Configuration files  | Missing   | No application.yml/properties or route config examined                               |
| K8s service          | Available | `cx-channels-linkedin-connector-svc` ClusterIP on port 9001, 213d old                |
| K8s ingress          | Available | No ingress routes to this service; caller must use internal service or port-forward  |

## Investigation Backlog

| # | Path to Explore | Priority | Status | Notes |
| - | --------------- | -------- | ------ | ----- |
| 1 | Locate source code for LinkedIn connector in working directory | High | Open | Need to find controller and config classes |
| 2 | Examine controller for `/cim-messages` mapping | High | Open | Verify if mapping exists and what HTTP methods it supports |
| 3 | Check Spring resource handler configuration | Medium | Open | Look for `WebMvcConfigurer` or `ResourceHttpRequestHandler` overrides |
| 4 | Check for path prefix or servlet context path mismatch | Medium | Open | Could explain why request misses controller mapping |
| 5 | Check active Spring profile / feature flags | Medium | Open | Endpoint may be conditional on a profile or property |
| 6 | Verify deployed image version vs. expected | Medium | Open | Wrong build could explain missing endpoint |

## Timeline of Events

| Time                        | Event                                                    | Source                | Confidence |
| --------------------------- | -------------------------------------------------------- | --------------------- | ---------- |
| 2026-06-08 10:56:33.593     | POST request to `cim-messages` throws `NoResourceFoundException` | Application log       | Confirmed  |

## Confirmed Findings

### Finding 1: Exact Error and Request Context

**Evidence:** Log timestamp `2026-06-08 10:56:33.593`, request ID `c7156dae-9255-421a-8485-5a1410516098`

**Detail:** The application threw `org.springframework.web.servlet.resource.NoResourceFoundException: No static resource cim-messages.` The stack trace originates from `ResourceHttpRequestHandler.handleRequest(ResourceHttpRequestHandler.java:585)` and was caught by `GlobalRestExceptionHandler.handleException` at line 122. The request method was POST (`FrameworkServlet.doPost` at line 914).

### Finding 2: Application Identity

**Evidence:** Stack trace shows package `com.linkedin.connector.config.HttpFilter` at `HttpFilter.java:53`; log entries reference `LinkedInWebhookController` and `LinkedInConfigService`.

**Detail:** This is a LinkedIn integration connector service running inside Kubernetes namespace `expertflow`.

### Finding 3: No Ingress for This Service

**Evidence:** `kubectl get svc,ingress -n expertflow` shows service `cx-channels-linkedin-connector-svc` (ClusterIP, port 9001) but no ingress routing to it.

**Detail:** The caller is reaching the pod either via internal cluster networking (`http://cx-channels-linkedin-connector-svc:9001/...`) or via `kubectl port-forward`. There is no path rewriting by ingress for this service.

## Deduced Conclusions

### Deduction 1: The Request Path Arrives Unchanged at Spring

**Based on:** Finding 3 (no ingress)

**Reasoning:** Without an ingress or proxy rewriting the path, the URL the caller sends is the exact URL Spring receives. A path prefix mismatch at the ingress/proxy layer is ruled out.

**Conclusion:** If the caller sends `POST /cim-messages`, Spring receives `POST /cim-messages`. The issue is either a missing controller mapping, wrong HTTP method on an existing mapping, or a missing Spring profile/feature flag.

## Hypothesized Paths

### Hypothesis 1: Missing or Mismatched Controller Mapping

**Status:** Open

**Theory:** The `/cim-messages` endpoint is not mapped in any controller, or the mapping exists but does not accept POST requests, causing Spring to fall through to the static resource handler.

**Supporting indicators:** `NoResourceFoundException` is Spring's standard response when no handler mapping matches a request and static resource lookup also fails.

**Would confirm:** Finding a controller that should handle `/cim-messages` but is missing, uses a different path, or only accepts GET/PUT instead of POST.

**Would refute:** Finding that `/cim-messages` is correctly mapped to accept POST, which would point to a configuration or profile issue instead.

**Resolution:** *(pending)*

### Hypothesis 2: Spring Profile or Feature Flag Not Active

**Status:** Open

**Theory:** The controller or endpoint is annotated with `@Profile` or `@ConditionalOnProperty` and is not loaded because the required profile/property is missing.

**Supporting indicators:** Common pattern for optional connector features.

**Would confirm:** Finding `@Profile("cim")` or similar on the controller, and observing that the profile is not in the active list.

**Would refute:** No conditional annotations on the controller; the bean is loaded but the mapping is still absent.

**Resolution:** *(pending)*

### Hypothesis 3: Wrong Build Deployed

**Status:** Open

**Theory:** The endpoint was implemented in a newer commit but the deployed container image is an older build.

**Supporting indicators:** Service is 213 days old (`213d`).

**Would confirm:** Image tag does not match latest; source control shows the endpoint exists in HEAD but not in the deployed tag.

**Would refute:** Image is current; endpoint is genuinely absent from all recent commits.

**Resolution:** *(pending)*

## Missing Evidence

| Gap                              | Impact                                             | How to Obtain                              |
| -------------------------------- | -------------------------------------------------- | ------------------------------------------ |
| Source code of LinkedIn connector | Required to verify controller mappings and config  | Search working directory or request from user |
| Full application configuration    | Required to check context paths and resource handlers | Find `application.yml` / `application.properties` |
| Active Spring profiles            | Would explain conditional beans not loading        | Check `actuator/env` or pod startup logs |
| Deployed image version            | Would reveal stale build                           | `kubectl get pod -o jsonpath='{.spec.containers[0].image}'` |

## Source Code Trace

| Element       | Detail                                      |
| ------------- | ------------------------------------------- |
| Error origin  | `ResourceHttpRequestHandler.java:585` (Spring framework) |
| Trigger       | POST request to `/cim-messages`             |
| Condition     | No handler mapping matched; static resource lookup failed |
| Related files | `GlobalRestExceptionHandler.java:122`, `HttpFilter.java:53` |

## Conclusion

**Confidence:** Low

The error is confirmed: a POST request to `cim-messages` is being handled by Spring's static resource handler instead of application code. The root cause is not yet determined. The most likely paths are (1) a missing or method-mismatched controller mapping, (2) an inactive Spring profile/feature flag, or (3) a stale deployed build. Source code access is needed to proceed.

## Recommended Next Steps

### Fix direction

*(Pending source code review.)*

### Diagnostic

1. Search working directory for Java source files related to `cim-messages`.
2. Check `application.yml` / `application.properties` for `server.servlet.context-path` and any custom resource handler configurations.
3. Check the pod's active profiles via actuator or startup logs.
4. Compare deployed image tag against latest build.

## Reproduction Plan

*(Pending — need to locate source code and build instructions.)*

## Side Findings

- The `GlobalRestExceptionHandler` logs `NoResourceFoundException` as an unhandled internal server error (line 122). This is a secondary issue: a 404-class error should ideally be handled gracefully rather than logged at ERROR severity with a full stack trace.
