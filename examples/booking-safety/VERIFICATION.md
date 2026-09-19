# Local verification

Scope: synthetic fixture consistency and regression tests only.
Python 3.11.9 was used locally on 2026-09-19 (Asia/Tbilisi).

The release checks are run from this directory:

```sh
python -B verify_cases.py
python -B -m unittest -v test_verify_cases
```

The expected corpus has 12 cases: nine `no_write`, one `create_once`, one
`reconcile` and one `handoff`. These are authored example counts, not measured
outcomes. The test suite has 70 local unit/mutation tests.

Release preparation changes only the file layout, editorial status/attribution
wording and schema/publication metadata. The original 12 safety scenarios,
utterances, synthetic states, annotations and expected actions are unchanged.
Two additional tests keep educational-release metadata separate from runtime
validation claims.

The tests exercise missing/stale/future evidence, the freshness boundary, offer
scope, corrections, quotes, background speech, withdrawal, duplicate prevention,
uncertain writes, known no-write failures, malformed JSON and bounded file reads.

No OMO server, model, audio, calendar, CRM, real caller, concurrency mechanism,
destination-side idempotency, reconciliation service or human handoff was tested.
No independent human linguistic review or third-party certification is claimed.
This report is not a live CI status badge.

## Observed release-preparation results

Verified locally at `2026-09-19T04:47:11.330135+04:00`.

| Command | Exit | Observed result |
|---|---:|---|
| `python -B verify_cases.py` | 0 | 12 fixtures passed; `runtime_validated: false` |
| `python -B -m unittest -v test_verify_cases` | 0 | All 70 local unit/mutation tests passed |
