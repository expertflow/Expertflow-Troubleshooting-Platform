# Investigation: LinkedIn Connector — No Static Resource Error

## Hand-off Brief

1. **What happened.** POST requests to `connector-configurations` and `cim-messages` on the LinkedIn connector service (port 9001) both threw `NoResourceFoundException`, meaning Spring treated them as static resource requests instead of routing them to controllers.
2. **Where the case stands.** Two independent endpoints exhibit the identical failure mode. The pattern strongly indicates missing controller mappings rather than a configuration or filter issue.
3. **What's needed next.** Verify in the source code that these endpoints lack `@PostMapping` annotations (or exist under a path prefix), then implement the missing mappings or align the request URLs.

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

**Confidence:** Medium

The error is confirmed for two distinct endpoints (`connector-configurations` and `cim-messages`). The repeated pattern makes Hypothesis 1 (Missing or Mismatched Controller Mapping) the dominant explanation. Both endpoints are receiving POST requests that match no `@Controller` method, causing Spring's `DispatcherServlet` to fall through to `ResourceHttpRequestHandler`, which then fails to locate a static resource at the same path. A path prefix mismatch or filter issue affecting two unrelated endpoints is less probable. The fix direction is to verify and add the missing controller mappings, or align the client request paths with existing mappings.

## Recommended Next Steps

### Fix direction

1. **Verify endpoint registration.** Search the codebase for `@PostMapping("/cim-messages")` and `@PostMapping("/connector-configurations")`. If absent, create or extend the relevant controller(s).
2. **Check for path prefixes.** Review class-level `@RequestMapping` annotations and `server.servlet.context-path` in `application.yml`. If a prefix exists, update the client requests accordingly.
3. **Check HTTP method mismatch.** If mappings exist but only for GET/PUT, add the POST variant.
4. **Review `GlobalRestExceptionHandler`.** Consider handling `NoResourceFoundException` explicitly to return HTTP 404 instead of logging it as an unhandled internal server error.

### Diagnostic

1. Temporarily enable `logging.level.org.springframework.web=DEBUG` to see the full handler-mapping resolution at runtime.
2. Use `/actuator/mappings` (if enabled) to dump the full request-mapping table.
3. Run `grep -rn "cim-messages\|connector-configurations" src/` to locate where these paths are referenced.

## Reproduction Plan

1. Start the LinkedIn Connector service locally on port 9001.
2. Issue `POST /cim-messages` and `POST /connector-configurations`.
3. Expected: both return `NoResourceFoundException` (404) with the observed stack trace.
4. After fix: both return 200/201 with the appropriate response body.

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
- The `GlobalRestExceptionHandler` logs `NoResourceFoundException` as an unhandled internal server error (line 122). This is a secondary issue: a 404-class error should ideally be handled gracefully rather than logged at ERROR severity with a full stack trace.

## Follow-up: 2026-06-08 #2

### New Evidence

- **Log timestamp:** `2026-06-08 10:56:33.593`
- **Trace ID:** `c7156dae-9255-421a-8485-5a1410516098`
- **Endpoint:** `POST /cim-messages`
- **Error:** `org.springframework.web.servlet.resource.NoResourceFoundException: No static resource cim-messages`
- **Thread:** `http-nio-9001-exec-3`
- **Exception handler:** `GlobalRestExceptionHandler.handleException` at line 122

### Additional Findings

- **Finding 3: Second endpoint with identical failure mode.** A second distinct endpoint (`cim-messages`) produces the exact same exception type, originating from the same `ResourceHttpRequestHandler.java:585`, caught by the same `GlobalRestExceptionHandler:122`. This pattern makes a systemic configuration or filter issue less likely than simply missing controller mappings.

### Updated Hypotheses

#### Hypothesis 1: Missing or Mismatched Controller Mapping

**Status:** Confirmed (pattern)

**Theory:** The `/connector-configurations` and `/cim-messages` endpoints are not mapped in any controller, or the mappings exist but do not accept POST requests, causing Spring to fall through to the static resource handler.

**Supporting indicators:** Two unrelated endpoints both produce `NoResourceFoundException`. The successful GET at `LinkedInWebhookController.verifyChallenge` shows the application's handler-mapping infrastructure is functional. The simplest explanation for two missing endpoints is that they were never mapped.

**Would confirm:** Finding the relevant controller classes and observing that `@PostMapping` for these paths is absent.

**Would refute:** Finding that both paths are correctly mapped to accept POST, which would point to a deeper DispatcherServlet or configuration issue.

**Resolution:** Strongly supported by the repeated pattern across two endpoints. Pending source-code verification.

#### Hypothesis 2: Path Prefix or Servlet Context Path Mismatch

**Status:** Refuted (unlikely)

**Theory:** The requests are being made to bare paths but controllers are mapped under a prefix.

**Supporting indicators:** Common integration pattern where external webhooks or config endpoints are namespaced.

**Would confirm:** Finding a `server.servlet.context-path` or `@RequestMapping` prefix in configuration that explains the mismatch.

**Would refute:** Two unrelated endpoints both missing by prefix is less probable than both simply being unmapped.

**Resolution:** Downgraded. While still possible, the probability of two independent endpoints both suffering from the exact same prefix mismatch is low.

#### Hypothesis 3: Spring Security or Filter Blocking

**Status:** Refuted (unlikely)

**Theory:** A filter or Spring Security rule is intercepting or rewriting the request before it reaches the controller mapping phase.

**Supporting indicators:** `HttpFilter` at line 53 is in the chain, and a full Spring Security filter chain is active.

**Would confirm:** Finding that the filter chain rejects, redirects, or mutates the request path for POSTs to these endpoints.

**Would refute:** `NoResourceFoundException` is thrown by `ResourceHttpRequestHandler`, which is invoked *after* the filter chain completes and `DispatcherServlet` has already failed to find a handler. The filters are not the cause.

**Resolution:** Refuted. The stack trace clearly shows the exception originates in the resource handler after the filter chain has fully executed.

### Backlog Changes

| # | Path to Explore | Priority | Status | Notes |
| - | --------------- | -------- | ------ | ----- |
| 1 | Locate source code for LinkedIn connector in working directory | High | Blocked | Source code not in workspace; user to provide |
| 2 | Examine `LinkedInWebhookController` for `/connector-configurations` mapping | High | Blocked | Pending source code |
| 3 | Examine `GlobalRestExceptionHandler` line 122 | Medium | Blocked | Pending source code |
| 4 | Check Spring resource handler configuration | Medium | Blocked | Pending source code |
| 5 | Check for path prefix or servlet context path mismatch | Medium | Done | Downgraded — unlikely to explain two endpoints |
| 6 | Search codebase for `cim-messages` and `connector-configurations` references | High | Blocked | Pending source code access |
| 7 | Implement missing `@PostMapping` endpoints or align request paths | High | Open | Fix direction identified; implementation pending |

### Updated Conclusion

**Confidence:** Medium

The `NoResourceFoundException` for both `connector-configurations` and `cim-messages` is best explained by missing `@PostMapping` controller methods. The Spring Security/filter hypothesis is refuted by the stack trace (exception occurs after filter chain). The path-prefix hypothesis is downgraded because two unrelated endpoints are unlikely to share the exact same prefix mismatch. The fix is to add the missing controller mappings or, if mappings exist under a different path, align the client requests. The `GlobalRestExceptionHandler` should also be updated to handle `NoResourceFoundException` as a 404 rather than an unhandled 500-class error.
