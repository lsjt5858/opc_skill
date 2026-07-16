---
name: ai-loop-orchestrator
description: Design bounded AI agent loops and skill workflows for complex goals. Use when the user mentions AI loops, goal loops, autonomous/automatic agent work, repeated iteration, verification criteria, stop conditions, token/cost control, scheduled monitoring, multi-agent workflows, or wants to turn a broad objective into a reusable skill-driven workflow.
---

# AI Loop Orchestrator

Turn a broad request into a bounded loop specification before executing it. Prefer the simplest loop that can meet the objective with clear validation.

## Core Workflow

1. Classify the loop.
   - **Turn loop**: one normal agent turn with local verification; use for short, non-recurring tasks.
   - **Goal loop**: repeat until a measurable condition is satisfied; use for tasks with explicit acceptance criteria.
   - **Timed loop**: repeat on a schedule or interval; use for polling, reminders, PR/CI monitoring, or recurring reports.
   - **Event loop**: react to external events; use when connectors, webhooks, CI, mail, or chat events are the true trigger.
   - **Workflow loop**: coordinate subagents or scripted orchestration; use for large migrations, codebase audits, research, or parallel solution exploration.

2. Write a loop spec in working notes before acting:
   - **Objective**: one sentence describing the destination.
   - **Trigger**: user prompt, explicit goal, time interval, event, or manual resume.
   - **Stop condition**: measurable success, max turns/time, empty queue, merged PR, clean test result, or user decision required.
   - **Verification**: commands, screenshots, rendered artifacts, logs, review pass, source citations, or external system checks.
   - **Budget**: max attempts/turns, model/tool intensity, subagent count, and any expensive steps to avoid.
   - **State**: what to remember between iterations: task list, files touched, failures, IDs, links, commands run.

3. Execute in small iterations:
   - Gather only the context needed for the next decision.
   - Make scoped changes or produce the requested artifact.
   - Run the strongest practical verification available.
   - If verification fails, update the working hypothesis and repeat.
   - Stop only when a named terminal state applies.

4. Report the terminal state:
   - **Achieved**: include the evidence.
   - **Needs user decision**: state the exact unresolved choice.
   - **Blocked**: state the blocking condition and what would unblock it.
   - **Budget reached**: summarize progress and remaining risk.
   - **Unsafe/unapproved**: explain the specific operation requiring consent.

## Primitive Selection

- Use the ordinary Codex turn loop by default.
- If the user explicitly asks to start or run a goal and the goal tool is available, create a goal with a concrete objective and complete it only after evidence supports success.
- If the user asks for reminders, monitoring, recurring checks, or schedules, search for the automation tool first and use it instead of hand-writing schedule instructions.
- If the task is parallelizable and high-value, use subagents or workflow tools only after defining independent worker prompts and a review/merge step.
- If a domain skill exists, invoke it for the verification loop: Playwright for UI/browser behavior, PDF/DOCX skills for rendered documents, GitHub skills for PR comments/CI, Lark skills for Feishu workflows, and so on.

## Verification Ladder

Pick the highest rung that is feasible and proportional to risk:

1. **Reasoned check**: explain why the output satisfies the request.
2. **Static check**: inspect files, schemas, types, diffs, or citations.
3. **Command check**: run tests, linters, builds, scripts, or validators.
4. **Runtime check**: exercise the app/API/document/browser and inspect real output.
5. **Independent review**: use a fresh reviewer/subagent or adversarial pass for high-risk changes.

Do not claim completion from edits alone when a runnable or inspectable verification path exists.

## Token And Cost Control

- Avoid multi-agent workflows for small tasks.
- Prefer deterministic commands and scripts over model reasoning for repeatable checks.
- Cap attempts explicitly when success is uncertain.
- Reuse existing repo commands, skills, and artifacts before inventing new machinery.
- Keep loop memory compact: current hypothesis, next action, evidence, and remaining failures.
- For recurring work, align frequency to how often the external state can realistically change.

## Reusable Loop Design

When the user wants a loop they can reuse later, create or update a skill only if the workflow will recur. Keep the skill concise, put detailed decision tables in `references/`, and include concrete trigger language in the skill description.

Read `references/loop-selection.md` when designing a reusable loop, comparing loop types, or drafting a prompt/spec for another agent.
