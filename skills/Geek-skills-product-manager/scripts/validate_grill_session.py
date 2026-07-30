#!/usr/bin/env python3
"""Validate a grill-me-to-doc state, transcript, and PRODUCT-DOC.

The validator uses only the Python standard library and fails closed: any
contract error exits 1.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

GATE_KEYS = {
    "problem",
    "users_jtbd",
    "evidence_assumptions",
    "scope_non_goals",
    "flows",
    "requirements",
    "success_metrics",
    "risks",
    "open_questions",
    "acceptance_criteria",
}
DOC_HEADINGS = [
    "## 1. Problem and desired outcome",
    "## 2. Primary users and JTBD",
    "## 3. Evidence and assumptions",
    "## 4. Scope and non-goals",
    "## 5. User flow and failure recovery",
    "## 6. Requirements",
    "## 7. Success metrics and guardrails",
    "## 8. Risks and dependencies",
    "## 9. Open questions",
    "## 10. Acceptance criteria",
    "## Decision log",
    "## Implementation boundary",
]
FORBIDDEN_ACTIONS = {
    "write_code",
    "create_scaffold",
    "create_branch",
    "commit",
    "push",
    "implement",
    "create_ticket",
}


def canonical_utf8_lf(data: bytes) -> bytes:
    """Return UTF-8 text with CRLF/CR normalized to LF and no other changes."""
    text = data.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def canonical_text_sha256(data: bytes) -> str:
    return hashlib.sha256(canonical_utf8_lf(data)).hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: cannot parse JSON: {exc}") from exc


def question_count(text: str) -> int:
    return len(re.findall(r"[?？]", text))


def validate_state(state: dict[str, Any], errors: list[str]) -> None:
    required = {
        "schema_version",
        "session_id",
        "skill_version",
        "mode",
        "status",
        "evidence",
        "decision_log",
        "unresolved_questions",
        "completion_gate",
        "product_doc",
        "hard_stop",
    }
    missing = required - state.keys()
    if missing:
        errors.append(f"state missing keys: {sorted(missing)}")
        return
    if state["schema_version"] != "1.0.0":
        errors.append("state schema_version must be 1.0.0")
    if state["skill_version"] != "1.2.0":
        errors.append("state skill_version must be 1.2.0")
    if state["mode"] != "grill-me-to-doc":
        errors.append("state mode must be grill-me-to-doc")
    evidence = state["evidence"]
    if not isinstance(evidence, list) or not evidence:
        errors.append("state must contain at least one evidence entry")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            if not re.fullmatch(r"[a-f0-9]{64}", str(item.get("sha256", ""))):
                errors.append(f"evidence[{index}] has invalid sha256")
            if not item.get("path") or not item.get("summary"):
                errors.append(f"evidence[{index}] needs path and summary")

    decisions = state["decision_log"]
    decision_ids = [item.get("id") for item in decisions if isinstance(item, dict)]
    if len(decision_ids) != len(set(decision_ids)):
        errors.append("decision_log ids must be unique")
    unresolved = state["unresolved_questions"]
    unresolved_ids = [item.get("id") for item in unresolved if isinstance(item, dict)]
    if len(unresolved_ids) != len(set(unresolved_ids)):
        errors.append("unresolved question ids must be unique")

    gate = state["completion_gate"]
    if not isinstance(gate, dict) or set(gate) != GATE_KEYS:
        errors.append(f"completion_gate keys must equal {sorted(GATE_KEYS)}")
    elif state["status"] in {"ready-for-draft", "awaiting-approval", "approved", "stopped"}:
        if not all(value is True for value in gate.values()):
            errors.append(f"status {state['status']} requires every completion gate to be true")

    hard_stop = state["hard_stop"]
    if not isinstance(hard_stop, dict) or hard_stop.get("implementation_allowed") is not False:
        errors.append("hard_stop.implementation_allowed must be false")
    product_doc = state["product_doc"]
    if state["status"] in {"approved", "stopped"}:
        if product_doc.get("approved_by_user") is not True:
            errors.append("approved/stopped state requires explicit user approval")
        if not product_doc.get("final_path"):
            errors.append("approved/stopped state requires final_path")


def validate_transcript(
    state: dict[str, Any],
    transcript: dict[str, Any],
    transcript_dir: Path,
    errors: list[str],
) -> None:
    events = transcript.get("events")
    if transcript.get("schema_version") != "1.0.0":
        errors.append("transcript schema_version must be 1.0.0")
    if transcript.get("session_id") != state.get("session_id"):
        errors.append("transcript session_id does not match state")
    if not isinstance(events, list) or not events:
        errors.append("transcript events must be a non-empty array")
        return
    expected_seq = list(range(1, len(events) + 1))
    actual_seq = [event.get("seq") for event in events if isinstance(event, dict)]
    if actual_seq != expected_seq:
        errors.append("transcript seq values must be contiguous from 1")

    seen_questions: dict[str, int] = {}
    answered: set[str] = set()
    first_question_seq: int | None = None
    draft_seq: int | None = None
    approval_seq: int | None = None
    resume_expected: str | None = None

    for event in events:
        if not isinstance(event, dict):
            errors.append("every transcript event must be an object")
            continue
        actor = event.get("actor")
        kind = event.get("kind")
        seq = event.get("seq")
        if kind == "question":
            first_question_seq = first_question_seq or seq
            qid = event.get("question_id")
            question = str(event.get("question", ""))
            recommendation = event.get("recommendation", {})
            if not qid or qid in seen_questions:
                errors.append(f"event {seq}: question_id missing or reused")
            else:
                seen_questions[qid] = seq
            if question_count(question) != 1:
                errors.append(f"event {seq}: question turn must contain exactly one question mark")
            if not recommendation.get("answer") or not recommendation.get("reason"):
                errors.append(f"event {seq}: recommendation needs answer and reason")
            if not event.get("evidence"):
                errors.append(f"event {seq}: question needs evidence context")
            if resume_expected and qid != resume_expected:
                errors.append(
                    f"event {seq}: resume expected {resume_expected}, got {qid}"
                )
            resume_expected = None
        elif kind == "answer":
            qid = event.get("question_id")
            if actor != "user" or qid not in seen_questions:
                errors.append(f"event {seq}: answer must match an earlier question")
            else:
                answered.add(qid)
        elif kind == "resume":
            if actor != "assistant":
                errors.append(f"event {seq}: resume must be an assistant event")
            resume_expected = event.get("from_next_question_id")
            state_path = event.get("state_path")
            state_sha = event.get("state_sha256")
            if not resume_expected or not state_sha or not state_path:
                errors.append(f"event {seq}: resume needs state path, hash, and next question id")
            else:
                try:
                    resume_bytes = (transcript_dir / state_path).read_bytes()
                    canonical_state = canonical_utf8_lf(resume_bytes)
                    actual_sha = hashlib.sha256(canonical_state).hexdigest()
                    if actual_sha != state_sha:
                        errors.append(f"event {seq}: resume state hash mismatch")
                    resume_state = json.loads(canonical_state.decode("utf-8"))
                    if resume_state.get("session_id") != state.get("session_id"):
                        errors.append(f"event {seq}: resume state session_id mismatch")
                    if resume_state.get("next_question_id") != resume_expected:
                        errors.append(f"event {seq}: resume next question mismatch")
                except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                    errors.append(f"event {seq}: cannot load resume state: {exc}")
        elif kind == "document_draft":
            draft_seq = seq
            if event.get("gate_passed") is not True:
                errors.append(f"event {seq}: draft emitted before completion gate")
            if question_count(str(event.get("question", ""))) != 1:
                errors.append(f"event {seq}: approval turn must ask exactly one question")
            recommendation = event.get("recommendation", {})
            if not recommendation.get("answer") or not recommendation.get("reason"):
                errors.append(f"event {seq}: approval turn needs recommendation and reason")
        elif kind == "approval":
            if actor != "user" or event.get("approved") is not True:
                errors.append(f"event {seq}: approval must be explicit and from user")
            approval_seq = seq
        elif kind == "final":
            if not approval_seq or approval_seq >= seq:
                errors.append(f"event {seq}: final document requires earlier approval")
            actions = set(event.get("actions", []))
            forbidden = sorted(actions & FORBIDDEN_ACTIONS)
            if forbidden:
                errors.append(f"event {seq}: forbidden implementation actions {forbidden}")
            if event.get("implementation_started") is not False:
                errors.append(f"event {seq}: implementation_started must be false")

    if first_question_seq:
        prior_evidence = [
            e for e in events
            if e.get("seq", 0) < first_question_seq and e.get("kind") == "evidence_read"
        ]
        if not prior_evidence:
            errors.append("repository evidence must be read before the first question")
    if draft_seq and (not approval_seq or approval_seq <= draft_seq):
        errors.append("explicit approval must follow the document draft")
    if resume_expected:
        errors.append("resume event was not followed by its stored next question")
    logged_question_ids = {
        item.get("question_id")
        for item in state.get("decision_log", [])
        if item.get("question_id")
    }
    missing_logs = answered - logged_question_ids
    if missing_logs:
        errors.append(f"answered questions missing from decision log: {sorted(missing_logs)}")


def validate_doc(state: dict[str, Any], text: str, errors: list[str]) -> None:
    if state.get("status") not in {"approved", "stopped"}:
        return
    for heading in DOC_HEADINGS:
        if heading not in text:
            errors.append(f"PRODUCT-DOC missing heading: {heading}")
    if re.search(r"\bTBD\b|待补充|此处略|placeholder", text, flags=re.IGNORECASE):
        errors.append("PRODUCT-DOC contains placeholder text")
    if "Approved by user: true" not in text:
        errors.append("PRODUCT-DOC must record explicit approval")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--transcript", required=True, type=Path)
    parser.add_argument("--product-doc", required=True, type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    try:
        state = load_json(args.state)
        transcript = load_json(args.transcript)
        doc = args.product_doc.read_text(encoding="utf-8")
        validate_state(state, errors)
        validate_transcript(state, transcript, args.transcript.parent, errors)
        validate_doc(state, doc, errors)
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"FAIL {len(errors)} error(s)")
        return 1
    print("PASS grill-me-to-doc contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
