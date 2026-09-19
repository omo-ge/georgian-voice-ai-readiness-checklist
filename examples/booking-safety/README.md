# Synthetic Georgian booking-safety examples

**12 bilingual cases for design review — not a product benchmark.**

Prepared for OMO / OMO AI as a companion to the
[Georgian Voice AI Readiness Checklist](../../README.md). Every utterance,
identifier, timestamp, speaker/intent annotation, availability observation and
destination result is synthetic. No real customer record is included.

## Start here

- [English explanation with a short Georgian summary](EXPLAINER.md)
- [ქართული გზამკვლევი: ჯავშნის თანხმობის გადამოწმება](GUIDE_KA.md)
- [Machine-readable bilingual cases](booking-safety-cases.json)
- [Local validator](verify_cases.py) and [unit/mutation tests](test_verify_cases.py)
- [Verification scope and results](VERIFICATION.md)

## Run locally

From this directory, using Python 3.10 or later:

```sh
python -B verify_cases.py
python -B -m unittest -v test_verify_cases
```

Only the Python standard library is needed. No installation, account, API key,
network request, model call, audio processing or booking integration is required.
The validator reads files within this directory and prints a report. Tests use
in-memory mutations and mocks; they do not perform real booking actions.

For a design review, read each case's state and evidence before inspecting
`expected`. Compare the permitted next action and rationale. Record disagreements
as design questions, not as recognition accuracy or product performance.

## Cases

| ID | Scenario | Expected mode |
|---|---|---|
| BS-01 | Direct confirmation of the current offer with matching evidence | create_once |
| BS-02 | An approximate Georgian time | no_write |
| BS-03 | A correction to the offered time | no_write |
| BS-04 | Missing availability evidence | no_write |
| BS-05 | Stale availability evidence | no_write |
| BS-06 | Consent refers to an older offer | no_write |
| BS-07 | Quoted or hypothetical agreement | no_write |
| BS-08 | A background speaker says yes | no_write |
| BS-09 | The caller withdraws before submission | no_write |
| BS-10 | Matching evidence of an existing booking | no_write |
| BS-11 | The outcome of a write is unknown | reconcile |
| BS-12 | Explicit destination rejection before any write effect | handoff |

`create_once` permits a hypothetical guarded attempt; it does not prove completion.
`no_write` prohibits creation but can still permit clarification, an authorized
read or returning an existing result. `reconcile` preserves the original operation
identifier before any retry. `handoff` is a required next step, not proof that an
operator actually received anything.

## Contract and limitations

Schema `1.1` fixes twelve ordered case IDs and scenario labels. It preserves the
original synthetic safety examples while using release-appropriate metadata and
a local file layout. The `educational_resource` label does not prove publication,
indexation, runtime testing or production readiness.

An offer ID binds an immutable service/resource/person/time tuple within a case.
Identifiers are fictional and case-local. “Tomorrow” is relative to each fixture's
explicit `2030-05-14` decision date, not the computer clock. The `+04:00` examples
do not validate future timezone law or an IANA timezone database.

The 120-second freshness window is illustrative, not an OMO setting or universal
safety threshold. Fresh availability is not a reservation: the positive example
also stipulates conditional slot writes and durable destination-side idempotency.
Those are hypothetical premises, not tested capabilities.

The validator checks structure and hand-authored evidence/expectation consistency.
It does not infer Georgian meaning, evaluate translations, transcribe audio,
identify speakers, authenticate callers, contact a destination or execute an action.
A test deliberately demonstrates that changed utterance text can still pass when
its manually supplied annotation is unchanged.

**Passing these checks says nothing about OMO's live booking accuracy, latency,
availability, concurrency, reconciliation or human-handoff delivery.**

## Provenance and attribution

Based on the Georgian Voice AI Readiness Checklist by OMO AI, which is shared
under the repository's existing [CC BY 4.0 notice](../../README.md#license).
Changes: original synthetic bilingual cases, explicit action boundaries,
English/Georgian explanations and local validation examples.

The existing checklist attribution and license notice are retained; no repository
license file or license terms were changed for this addition. Product descriptions
link to OMO's own first-party guides, not independent certification:

- [Appointment-booking guidance](https://omo.ge/resources/automated-appointment-booking)
- [Quality-testing guidance](https://omo.ge/resources/voice-ai-quality-testing)
- [Public media kit](https://omo.ge/media-kit)

## მოკლე ქართული განმარტება

ეს არის 12 სინთეზური ორენოვანი მაგალითი და მათი ლოკალური შემოწმება.
ყველა დრო, პირობითი იდენტიფიკატორი და შედეგი გამოგონილია სასწავლო მიზნისთვის.
ტესტი არ ამოწმებს OMO-ს რეალურ სისტემას ან ქართული მეტყველების ამოცნობას.
კითხვის არსია: რა მოქმედება შეიძლება სცადოს პროცესმა არსებული მტკიცებულებით
და რა არ უნდა გააკეთოს გაურკვევლობის შემთხვევაში?
