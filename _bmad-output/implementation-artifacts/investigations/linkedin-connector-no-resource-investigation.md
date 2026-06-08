# Investigation: LinkedIn Connector — No Static Resource Error

## Hand-off Brief

1. **What happened.** A POST request to `connector-configurations` on the LinkedIn connector service (port 9001) threw `NoResourceFoundException`, meaning Spring treated it as a static resource request instead of routing it to a controller.
2. **Where the case stands.** Stronghold established: the exact error, timestamp, and request ID are confirmed. The application's controller mappings and route configuration are not yet examined.
3. **What's needed next.** Map the evidence perimeter — inspect source code for `LinkedInWebhookController`, `GlobalRestExceptionHandler`, and any configuration classes that define or override request mappings for `/connector-configurations`.

## Case Info

| Field            | Value                                                                      |
| ---------------- | -------------------------------------------------------------------------- |
| Ticket           | N/A                                                                        |
| Date opened      | 2026-06-08                                                                 |
| Status           | Active                                                                     |
| System           | Spring Boot application (LinkedIn Connector), port 9001, Java 21           |
| Evidence sources | Log snippet provided by user (stdout/stderr)                               |

## Problem Statement

A POST request to `/connector-configurations` on the LinkedIn connector service results in a `NoResourceFoundException: No static resource connector-configurations`. The user expects this endpoint to be handled by application code, but Spring's `ResourceHttpRequestHandler` is attempting to serve it as a static resource instead.

## Evidence Inventory

| Source               | Status    | Notes                                                                                |
| -------------------- | --------- | ------------------------------------------------------------------------------------ |
| Application log      | Available | Single log snippet with error trace, timestamp 2026-06-08 06:59:42.852, req ID 6792346d-6180-48c6-88ba-76704e0ed20d |
| Source code          | Missing   | Project source not yet located in working directory                                  |
| Issue tracker        | Missing   | No ticket ID provided                                                                |
| Version control      | Missing   | Commit range unknown                                                                 |
| Test results         | Missing   | No test output provided                                                              |
| Configuration files  | Missing   | No application.yml/properties or route config examined                               |

## Investigation Backlog

| # | Path to Explore | Priority | Status | Notes |
| - | --------------- | -------- | ------ | ----- |
| 1 | Locate source code for LinkedIn connector in working directory | High | Open | Need to find controller and config classes |
| 2 | Examine `LinkedInWebhookController` for `/connector-configurations` mapping | High | Open | Verify if mapping exists and what HTTP methods it supports |
| 3 | Examine `GlobalRestExceptionHandler` line 122 | Medium | Open | Understand how exceptions are classified and logged |
| 4 | Check Spring resource handler configuration | Medium | Open | Look for `WebMvcConfigurer` or `ResourceHttpRequestHandler` overrides |
| 5 | Check for path prefix or servlet context path mismatch | Medium | Open | Could explain why request misses controller mapping |

## Timeline of Events

| Time                        | Event                                                    | Source                | Confidence |
| --------------------------- | -------------------------------------------------------- | --------------------- | ---------- |
| 2026-06-08 06:59:42.852     | POST request to `connector-configurations` throws `NoResourceFoundException` | Application log       | Confirmed  |
| 2026-06-08 06:59:42.908     | `CustomerResponseBodyAdviceAdaptor` returns `EF009` "Internal Server Error" | Application log       | Confirmed  |
| 2026-06-08 07:42:28.470     | Successful GET challenge verification request received   | Application log       | Confirmed  |

## Confirmed Findings

### Finding 1: Exact Error and Request Context

**Evidence:** Log timestamp `2026-06-08 06:59:42.852`, request ID `6792346d-6180-48c6-88ba-76704e0ed20d`

**Detail:** The application threw `org.springframework.web.servlet.resource.NoResourceFoundException: No static resource connector-configurations.` The stack trace originates from `ResourceHttpRequestHandler.handleRequest(ResourceHttpRequestHandler.java:585)` and was caught by `GlobalRestExceptionHandler.handleException` at line 122. The request method was POST (`FrameworkServlet.doPost` at line 914).

### Finding 2: Application Identity

**Evidence:** Stack trace shows package `com.linkedin.connector.config.HttpFilter` at `HttpFilter.java:53`; log entries reference `LinkedInWebhookController` and `LinkedInConfigService`.

**Detail:** This is a LinkedIn integration connector service. The same application later successfully handled a GET challenge verification request at 07:42:28, indicating the service was running and responsive.

## Deduced Conclusions

*(None yet — pending source code examination.)*

## Hypothesized Paths

### Hypothesis 1: Missing or Mismatched Controller Mapping

**Status:** Open

**Theory:** The `/connector-configurations` endpoint is not mapped in any controller, or the mapping exists but does not accept POST requests, causing Spring to fall through to the static resource handler.

**Supporting indicators:** `NoResourceFoundException` is Spring's standard response when no handler mapping matches a request and static resource lookup also fails. The successful GET at `LinkedInWebhookController.verifyChallenge` shows the application does have working mappings.

**Would confirm:** Finding a controller that should handle `/connector-configurations` but is missing, uses a different path, or only accepts GET/PUT instead of POST.

**Would refute:** Finding that `/connector-configurations` is correctly mapped to accept POST, which would point to a configuration or filter issue instead.

**Resolution:** *(pending)*

### Hypothesis 2: Path Prefix or Servlet Context Path Mismatch

**Status:** Open

**Theory:** The request is being made to `/connector-configurations` but the controller is mapped under a prefix (e.g., `/api/connector-configurations`) or a servlet context path (e.g., `/linkedin/connector-configurations`) that does not match.

**Supporting indicators:** Common integration pattern where external webhooks or config endpoints are namespaced.

**Would confirm:** Finding a `server.servlet.context-path` or `@RequestMapping` prefix in configuration that explains the mismatch.

**Would refute:** Controller is mapped exactly at `/connector-configurations` with no prefix.

**Resolution:** *(pending)*

### Hypothesis 3: Spring Security or Filter Blocking

**Status:** Open

**Theory:** A filter (e.g., `HttpFilter` at line 53) or Spring Security rule is intercepting or rewriting the request before it reaches the controller mapping phase, causing it to fall through to the resource handler.

**Supporting indicators:** The stack trace shows `com.linkedin.connector.config.HttpFilter.doFilterInternal(HttpFilter.java:53)` in the chain, and a full Spring Security filter chain is active.

**Would confirm:** Finding that the filter chain rejects, redirects, or mutates the request path for POSTs to this endpoint.

**Would refute:** Filter chain passes the request through unchanged and the issue is purely at the `DispatcherServlet` mapping level.

**Resolution:** *(pending)*

## Missing Evidence

| Gap                              | Impact                                             | How to Obtain                              |
| -------------------------------- | -------------------------------------------------- | ------------------------------------------ |
| Source code of LinkedIn connector | Required to verify controller mappings and config  | Search working directory or request from user |
| Full application configuration    | Required to check context paths and resource handlers | Find `application.yml` / `application.properties` |
| HTTP request details (headers, full path) | Would confirm exact URL being requested            | Enable access logging or inspect proxy/gateway logs |

## Source Code Trace

| Element       | Detail                                      |
| ------------- | ------------------------------------------- |
| Error origin  | `ResourceHttpRequestHandler.java:585` (Spring framework) |
| Trigger       | POST request to `/connector-configurations` |
| Condition     | No handler mapping matched; static resource lookup failed |
| Related files | `GlobalRestExceptionHandler.java:122`, `HttpFilter.java:53` |

## Conclusion

**Confidence:** Low

The error is confirmed: a POST request to `connector-configurations` is being handled by Spring's static resource handler instead of application code. The root cause is not yet determined. The most likely paths are (1) a missing or method-mismatched controller mapping, (2) a path prefix mismatch, or (3) filter/security chain interference. Source code access is needed to proceed.

## Recommended Next Steps

### Fix direction

*(Pending source code review.)*

### Diagnostic

1. Search working directory for Java source files related to `LinkedInWebhookController`, `LinkedInConfigService`, and any class referencing `connector-configurations`.
2. Check `application.yml` / `application.properties` for `server.servlet.context-path` and any custom resource handler configurations.
3. Review `GlobalRestExceptionHandler` to understand how `NoResourceFoundException` is being logged as an unhandled internal error.

## Reproduction Plan

*(Pending — need to locate source code and build instructions.)*

## Side Findings

- The same application instance successfully handled a LinkedIn webhook challenge verification (GET) at 07:42:28, ~43 minutes after the error. This suggests the service was not completely down; the failure is specific to the `connector-configurations` endpoint or the POST method.
