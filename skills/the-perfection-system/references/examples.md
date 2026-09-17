# Worked examples

These examples illustrate the protocol. Their review records are hypothetical, not claims that tools or independent reviewers were actually run.

## 1. A small prose revision in plain chat

**Request:** simplify this instruction without changing its meaning. Return only the revised instruction.

**Original:**

> Applications must arrive before noon on Monday. Each application must have the applicant's signature. The review of applications happens on Tuesday.

**Compact contract K1:** preserve the strict before-noon Monday deadline (C1), applicant signature (C2), and Tuesday review day (C3). Remove unnecessary wording without adding claims (C4). One cycle; single-assistant mode. Critiquer covers C1, C2, C4; Continuity covers C1, C3.

**Candidate A1:**

> Submit your application with your signature before noon on Monday. Applications are reviewed on Tuesday.

**Cycle 1 review:** both required lenses pass. C1 is supported by the unchanged phrase "before noon on Monday"; C2 by "with your signature"; C3 by the final sentence; C4 by comparing the full original and revised instructions. No external verification is needed for a meaning-preservation task limited to the supplied text.

**Outcome:** `accepted` under K1. The user sees only A1, not the process record. This is a sequential self-review, not independent validation.

## 2. A code change with an unavailable runtime

**Request:** change a supplied integer helper from `return n + 2` to behavior that adds exactly one. Tests must pass.

**Contract K1:** C1 requires the visible implementation to add one; C2 requires the relevant runtime tests to pass. Critiquer covers C1 and C2; Continuity checks that the function's interface and surrounding explanation stay consistent. The environment can inspect and write text but cannot execute code.

**Candidate A1:** change the return expression to `return n + 1`, leaving the signature unchanged.

**Review:** C1 passes by direct inspection for the specified integer operation. C2 is `unverified` because no test execution is available. The interface consistency check passes on the supplied material. The Critiquer verdict is `unverified`, not `pass`.

**Outcome:** `blocked`. Deliver the proposed change, explain that tests were not run, and identify runtime execution as the missing acceptance check. Do not print invented test output or claim that a source-level check satisfies the runtime requirement.

## 3. Same-version review with multiple participants

**Task:** refine a setup guide while preserving its documented prerequisites and safety warnings. Required lenses are Critiquer, Continuity, and Safety. The contract is K1 and the budget is three cycles.

**Cycle 1, candidate A1:** Critiquer and Safety pass. Continuity finds two contradictory prerequisite orders and returns `revise` with finding F1.

**Revision:** the editor consults the supplied governing specification, resolves F1, and creates A2. A1's passes do not apply to A2.

**Cycle 2, candidate A2:** all three required lenses inspect A2 against K1. F1's fix is verified, every required criterion has evidence, and all three lenses pass. One reviewer suggests an optional diagram; this is advisory and does not reopen the required gate.

**Outcome:** `accepted` for A2, K1, cycle 2. If Safety had timed out instead, A2 would not be accepted. A1's Safety pass could not fill the gap.

## 4. A research artifact with missing evidence

**Task:** update a comparison with current prices and preserve the supplied product descriptions. The only supplied pricing evidence is dated two years earlier, and no retrieval capability is available.

**Contract:** distinguish preservation of supplied descriptions from verification of current prices. Current-price verification is required; older prices cannot silently be relabeled current.

**Work:** improve the comparison's structure and preserve the descriptions. Identify the old pricing date and leave the current-price check `unverified`. Provide useful partial work without inventing a current value.

**Outcome:** `blocked`, with an explicit request for current authoritative price evidence or an authorized retrieval capability. A structurally improved table is not evidence that prices are current.

## 5. Conflicting preferences and a stall

**Task:** improve a manual while preserving every mandatory warning. K1 requires the warnings; brevity is advisory. Budget: five cycles.

**Cycle 1:** a reviewer suggests removing a required warning for brevity. Reconciliation rejects the suggestion against K1; optional polish cannot override a required constraint.

**Cycles 2 and 3:** a different required ambiguity remains unresolved because two supplied governing passages disagree. If that conflict needs a decision the environment cannot make, stop as `blocked` rather than spend the remaining cycles guessing. If the ambiguity is actionable but repeated revisions make no substantive progress, use `stalled` after two consecutive no-progress revision cycles. Preserve the safest useful candidate and describe the unresolved issue.

**Outcome:** never `accepted` by quietly deleting a warning or dropping the dissenting lens. A finite budget is not permission to weaken the requirements.

## 6. A cross-harness handoff

**Checkpoint:** candidate A2, best candidate A2, contract K1, two of three review cycles used, F4 unresolved, no current acceptance. A new host has only file reading and editing, not the previous execution tools.

**On resumption:** read A2 and K1, verify their identities, confirm F4 still applies, and carry forward one remaining cycle. Map capabilities again. Historical test output may be kept as evidence of its actual run, but do not represent it as a new execution or as covering changed code.

If the file now contains unrelated user edits, do not replace it with checkpoint A2. Preserve the edits, establish the new candidate version, and invalidate stale approvals. If authority or permissions cannot be reconciled, stop as `blocked` with a useful handoff.
