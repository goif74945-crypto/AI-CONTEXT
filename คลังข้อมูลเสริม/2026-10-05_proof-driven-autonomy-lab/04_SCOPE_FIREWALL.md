# Scope Firewall
Status: **AI-PROPOSED CONCEPT — NOT IMPLEMENTED / NOT APPROVED**

A policy enforcement point between planner and tool broker.

Inputs: task scope, protected resources, action class, exact target identity, environment, read/write class, observed revision, approval token, blast radius.

Decisions: ALLOW | DENY | REQUIRE_REVALIDATION | REQUIRE_APPROVAL.

Example semantics:
DENY write when repository name contains NEXY.AI unless an explicit user grant matches exact repository + action.
ALLOW evidence reads within task scope.
REQUIRE_REVALIDATION when observed revision differs from planned revision.
DENY destructive action when rollback classification is UNKNOWN.

Retrieved documents, web pages, comments and tool outputs cannot grant permissions.

Every high-impact ALLOW links to a proof bundle; every DENY records a policy rule ID and sanitized decision inputs.
