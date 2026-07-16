# Loop Selection Reference

## Decision Table

| Need | Loop type | Stop condition | Verification | Cost control |
| --- | --- | --- | --- | --- |
| Quick one-off code/content task | Turn loop | Agent proves task done or asks for context | Focused tests, file inspection, screenshots, citations | Specific prompt and smallest useful context |
| Complex task with measurable finish line | Goal loop | Acceptance criteria pass or max turns/time reached | Transcript-visible evidence: test output, build exit, metrics, checklist | Explicit max attempts and one measurable target |
| PR/CI/review monitoring | Timed loop | PR merged, CI green, no open actionable comments, or user cancels | `gh`, CI logs, review thread state | Longer intervals or event trigger when possible |
| Periodic digest/report | Timed loop or automation | Report delivered for each period | Source links, timestamps, deduped items | Match cadence to source update rate |
| External event response | Event loop | Each event classified, handled, and acknowledged | Connector/API state and response record | Filter events before invoking large model |
| Large migration/audit/research | Workflow loop | Queue empty plus review pass complete | Independent reviewer or sampled runtime checks | Batch work, cap agents, summarize intermediate state |

## Loop Spec Template

```text
Objective:
Trigger:
Inputs and context:
Stop condition:
Verification evidence:
Budget limits:
State to preserve:
Fallback if verification fails:
Terminal states:
```

## Good Stop Conditions

- `npm test` exits 0 and no source files outside `src/auth` changed.
- Lighthouse performance/accessibility/best-practices/SEO scores are all >= 90, or stop after 5 attempts.
- Every open PR review thread has a response or code change, CI is green, and the branch is pushed.
- The issue queue label `needs-triage` is empty, and each processed issue has exactly one owner/status label.

## Poor Stop Conditions

- "Make it better."
- "Until it feels done."
- "Fix everything."
- "Keep going as long as possible."

Rewrite poor conditions into measurable checks before starting the loop.

## Review Prompt Pattern

Use a fresh reviewer when risk is high:

```text
Review the current artifact/change against the stated stop condition.
Focus on bugs, missing verification, regressions, and places where the loop could stop too early.
Do not rewrite the solution unless a defect requires it.
Return findings ordered by severity with file/line or evidence references.
```
