# PRODUCT-DOC: Skill Trust Card

## Document status

- Status: Approved
- Session ID: trust-card-session
- Approved by user: true
- Evidence as of: supplied fixture

## 1. Problem and desired outcome

Readers see a curated skill entry but cannot tell whether the exact version was
reviewed. In the synthetic discovery fixture, 8 of 12 participants assumed every
listing had passed a security review. The desired outcome is accurate
comprehension of what was tested and what remains unknown, not more installs.

## 2. Primary users and JTBD

Primary user: a non-developer WorkBuddy user comparing community skills.

JTBD: when comparing a skill, the user wants to see the evidence boundary at a
glance so they can decide whether to inspect further without mistaking curation
for a safety guarantee.

## 3. Evidence and assumptions

Evidence:

- `repo/README.md`: the product is a curated index, not an installer.
- `repo/resource-contract.md`: cards currently expose only title, URL, and
  description.
- `repo/discovery-notes.md`: synthetic moderated tasks show the trust-signaling
  misunderstanding.

Assumption: users can understand a short neutral status if the tested version
and limitations are adjacent. This must be checked in usability testing.

## 4. Scope and non-goals

In scope:

- evaluation status;
- tested commit or version;
- test date;
- concise limitations with a link to evidence.

Non-goals:

- skill installation or execution;
- a global safety score;
- vendor ranking;
- claims that an unevaluated skill is unsafe;
- code or workflow for the evaluated skill.

## 5. User flow and failure recovery

The user opens a skill entry, sees a neutral evidence state, expands details,
and reads the tested version, date, limitations, and report link.

If evidence is missing, the entry shows “Not independently evaluated” in neutral
gray. If an evidence link is unavailable, the card retains the tested version
and date, labels the report unavailable, and makes no safety claim.

## 6. Requirements

- R1: Every trust card displays one status: independently evaluated,
  coordinator evidence only, or not independently evaluated.
- R2: An independently evaluated state requires tested commit/version, test
  date, limitations, and evidence link.
- R3: Missing evidence uses neutral styling and the exact wording “Not
  independently evaluated”.
- R4: The UI never displays “safe”, “production ready”, or equivalent wording.
- R5: Unknown or malformed evidence data falls back to the neutral state.
- NFR1: Evidence text remains readable at a 320 px viewport without horizontal
  scrolling.
- NFR2: The static page performs no skill execution and requests no credentials.

## 7. Success metrics and guardrails

Primary metric: in a moderated comprehension test, at least 80% of participants
correctly identify the tested version and one stated limitation.

Guardrail: zero participants interpret the trust card as a safety guarantee.
Both conditions must pass.

## 8. Risks and dependencies

- Stale evaluation: show the tested version and date prominently.
- Badge over-trust: use neutral wording and always show limitations.
- Missing report: degrade to a neutral unavailable state.
- Editorial inconsistency: validate required fields before rendering.
- Dependency: the curated data source must support the four evidence fields.

## 9. Open questions

Non-blocking: whether the compact state appears directly on the list card or
only on the detail view. Test both placements without changing the evidence
contract.

There are no blocking open questions.

## 10. Acceptance criteria

- AC1: A complete evaluated fixture renders status, version, date, limitations,
  and report link.
- AC2: A fixture missing any required evidence field renders “Not independently
  evaluated” and no safety color.
- AC3: No rendered copy contains “safe” or “production ready”.
- AC4: At 320 px viewport width, the component has no horizontal overflow.
- AC5: The moderated test meets both the 80% comprehension target and the
  zero-guarantee guardrail.

## Decision log

- D1: Optimize for evidence comprehension, accepted from user.
- D2: Prioritize non-developer WorkBuddy users, accepted from user.
- D3: Limit MVP to four evidence fields, accepted from user.
- D4: Use a neutral unevaluated state, accepted from user.
- D5: Use the dual metric and guardrail, accepted from user.

## Implementation boundary

This approved document does not authorize implementation. The product-manager
skill stops here; a separate explicit task is required before code or delivery
work begins.
