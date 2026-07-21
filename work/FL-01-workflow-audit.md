# FL-01 — AI Workflow Audit and Tool Setup

**Track:** General AI Fluency · **Week 1 · Onboarding**
**By:** Rohit Madhavan (GitHub: ROHITCRAFTSYT)

---

## 1. Workflow audit

Ten-plus recurring tasks from a real week (ML internship + solo dev + open-source
+ a paying client), each classified and given a one-line rationale.

**Classification key**

| Category | Meaning |
|---|---|
| Just me | AI stays out — judgment, accountability, or a failure mode AI itself causes |
| Delegate w/ review | AI drafts the whole thing; I check and ship |
| Collaborate | Back-and-forth; I lead the thinking, AI accelerates |
| Fully automate | Runs without me in the loop (script/CI); I only see failures |

| # | Recurring task | Classification | Rationale |
|---|---|---|---|
| 1 | Write commit messages | Delegate w/ review | AI drafts from the diff; I check it's honest about *why*. |
| 2 | Write OSS PR descriptions (zizmor campaign) | Delegate w/ review | Mechanical summary of work I did; I verify the claims. |
| 3 | Scrub AI-generated inline comments before opening a PR | **Just me** | Maintainers reject AI-slop comments repeatedly — the AI *is* the failure mode, so I'm the gate. |
| 4 | Reply to the paying voice-pipeline customer | Delegate w/ review | AI drafts tone; I check facts and never auto-send. Real money on the line. |
| 5 | Weekly internship progress write-up | Collaborate | I supply what happened; AI shapes it into something readable. |
| 6 | Frame the ML research question / pick the lane | **Just me** | Direction-setting — the core thinking the work is meant to test. |
| 7 | Run + verify notebooks top to bottom | **Just me** | Validation is my accountability; AI can't sign off on its own output. |
| 8 | Understand an unfamiliar codebase | Collaborate | AI maps it fast; I still have to build the real mental model. |
| 9 | Debug failing tests / stack traces | Collaborate | AI proposes hypotheses; I confirm them against the system. |
| 10 | Judge "does this choice bias the benchmark/result?" | **Just me** | High-stakes judgment; a wrong call quietly corrupts every downstream number. |
| 11 | Write tests (hard checks, state machines) | Delegate w/ review | AI covers the obvious cases; I add the ones it won't think of. |
| 12 | Scaffold boilerplate for a new project | Delegate w/ review | Tedious, low-risk setup. |
| 13 | Pin GitHub Actions to SHAs / add zizmor hooks | Fully automate | Deterministic, script/CI-enforced. |
| 14 | Fix lint/formatting + dependency bumps | Fully automate | Already runs on a Dependabot cooldown; humans only on breakage. |

**Honest "just me" tasks (rubric asks for ≥2):** #3, #6, #7, #10 — four of them,
each for a different reason (AI-caused failure mode, direction-setting, personal
accountability, high-stakes judgment).

---

## 2. Tool setup

- [ ] Claude account
- [ ] ChatGPT account
- [ ] Anthropic Academy account
- [ ] Enrolled in *AI Fluency: Framework & Foundations*, module 1 complete
- [ ] Claude Project created with the custom instructions below (screenshot attached)

*(Evidence: screenshots of the configured Claude Project and Academy enrollment.)*

### Claude Project custom instructions

```
Who I am: Rohit Madhavan — B.Tech CSBS student, ML engineering intern, security
  analyst & AI engineer. Solo/lead dev on vaanibench; built SOC-Triage-Gym (RL env,
  national finalist) and a production vernacular voice pipeline for a paying customer.
  GitHub: ROHITCRAFTSYT.

What I'm working toward: the ML internship (CTR/engagement ranking); shipping
  vaanibench; keeping my open-source zizmor campaign clean and merged.

How to work with me:
  - Don't over-explain basics. I can read and modify anything you write.
  - Flag design tradeoffs explicitly — especially every "this choice biases the
    benchmark / result" moment.
  - Plan before code: list files to create/change, get my confirmation, then implement.
  - Tests are mandatory for hard checks and state machines.
  - NO superfluous inline comments in code or PRs — keep a comment only where it
    states a real constraint. (Maintainers reject AI-slop comments.)
  - Timebox is real (solo, part-time) — cut scope, not the deadline.
```

---

## 3. Three target tasks for FL-02 – FL-04

Chosen to span the range (one delegate, one collaborate, one high-trust) and to
each have a concrete, checkable definition of success.

| Task | "Done well" means (measurable) |
|---|---|
| **OSS PR authoring** (delegate + human gate) | Next zizmor PR merges with **zero "superfluous comments" feedback** from the maintainer; all Action/workflow refs pinned to full SHAs. |
| **Debug from a stack trace** (collaborate) | AI's top hypothesis is the real cause **≥6 / 10** on real test failures; fix reached faster than solo (stopwatch). |
| **Client reply drafting** (delegate, high-trust) | Draft needs **zero** factual correction, matches my voice, and **0 auto-sends** — I read every one before it goes. |
