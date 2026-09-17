# Perfection System run record

Optional template. Fill only fields useful to the task. Keep records concise and do not store secrets. Fields and verdicts are conventions, not a required API or runtime dependency.

## Contract

```text
Run ID:
Contract version:
Objective and audience:
Requested output format:
Authorized editable surface:
Out of scope:
Immutable constraints:
Authority references and versions:
Disclosed assumptions:
Execution mode:
Available and authorized capabilities:
Unavailable capabilities:
Required review lenses and participants:
Maximum cycles: 3, unless the user or host sets a different finite limit
Other hard budgets:
Approval gates:
```

## Acceptance criteria

| ID | Required or advisory | Observable condition | Verification method | Assigned lens |
| --- | --- | --- | --- | --- |
| C1 | required | Replace with a task-specific condition. | Name the actual check. | critiquer |
| C2 | required | Replace with a task-specific continuity check. | Name the actual check. | continuity |

Cover every explicit user requirement. Assign every required criterion to at least one required lens and give every required lens a non-empty remit. Advisory preferences must not override required criteria.

## Candidate and cycle

```text
Cycle:
Candidate version:
Contract version:
Artifact location or inline content:
Material changes:
Source changes since the prior cycle:
```

## Review record, repeated for each required lens

```text
Review ID:
Candidate / contract / cycle:
Lens:
Participant and actual isolation, if any:
Assigned required criteria:
Criterion results: <ID, pass|fail|unverified, evidence or missing check>
Finding IDs:
Checks actually performed and results:
Coverage limitations:
Verdict: pass | revise | unverified
```

## Finding ledger

| ID | Criterion | Required/advisory | Location and evidence | Resolution condition | State | Origin |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | C1 | required | Describe the observed failure. | Describe what would resolve it. | open | Lens and cycle |

Use `open`, `resolved`, or `disputed` for finding state. Link resolved findings to verification on the revised candidate. Preserve disputed findings and their evidence until genuinely resolved.

## Result or checkpoint

```text
Status: accepted | blocked | budget_exhausted | stalled | stopped
Delivered candidate:
Latest working candidate, if different:
Best candidate and selection rationale, if different:
Contract and source versions:
Last completed cycle and any incomplete review:
Required lenses and criterion coverage:
Material changes:
Verification actually performed:
Open required failures and unverified checks:
Advisory notes:
Remaining budget:
Next action, missing evidence, or required decision:
```

Before accepting, confirm same-candidate, same-contract, same-cycle passes from all required lenses and evidenced coverage of every required criterion. No required finding or approval gate may remain unresolved. On resumption, verify the actual artifact and authority rather than trust this record's status labels.
