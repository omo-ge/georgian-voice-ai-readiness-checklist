# A fluent answer is not a confirmed booking: 12 safety checks for Georgian voice AI

**Prepared for OMO / OMO AI. Educational companion to the open checklist. All examples, timestamps and destination results are synthetic. No OMO runtime, language model or live integration was tested.**

A caller can hear a clear, reassuring answer while the destination calendar contains no booking. The reverse is also possible: a booking exists, but the response never reaches the caller. Neither fluent speech nor silence settles the operational question. Engineers and business operators need to distinguish what the caller requested, what the system may attempt, and what the destination actually confirms.

## Start with the evidence boundary

An **offer** is a specific proposed service, resource, person, start time and end time, interpreted in an explicit timezone. In this corpus, an offer ID binds those details immutably. Changing the time means issuing a new offer, not quietly updating the meaning of an earlier confirmation.

The **source of truth** is the authorized destination system responsible for the booking. A transcript, a model's memory and a successful request submission are not equivalent to a matching, verified destination result.

The design principle is simple: **the LLM interprets and speaks; deterministic logic authorizes; a verified backend result supplies the evidence for completion.** This is a recommended process, not proof that a product implements it.

[OMO's booking guidance](https://omo.ge/resources/automated-appointment-booking) distinguishes conversation from completed action. Integration scope depends on deployment. The [media kit](https://omo.ge/media-kit) cautions against guaranteed-completion and certification claims.

## Four different next steps

The corpus separates four modes:

- **No-write:** clarify, refresh evidence, acknowledge withdrawal or return an existing result without creating anything.
- **Create-once:** permit at most one guarded attempt for the confirmed current offer. This is not a completion claim.
- **Reconcile:** determine the outcome of an earlier attempt using its original operation identifier, without another create.
- **Handoff:** route an unresolved or known failure to a human with an honest account of what is known.

An **idempotency key** identifies one logical booking operation. Durable destination-side enforcement prevents repeated submissions of that operation from creating additional bookings. Merely adding a key to a request does not establish that guarantee.

## Twelve checks at the action boundary

1. **A valid request and current confirmation.** BS-01 pairs an initial request with an exact offer and direct caller agreement. Fresh matching availability and declared write guards permit one hypothetical attempt. A verified result is still needed before saying the booking is confirmed.

2. **An approximate Georgian time.** In synthetic BS-02, “ხვალ სამისკენ ჩამწერეთ” means “Book me tomorrow around three.” Without further context, an exact hour and intended part of the day remain unresolved. Ask; do not silently choose 15:00.

3. **A correction to the proposed time.** BS-03 changes a preference from 15:00 to 16:00. Invalidate authority attached to the earlier offer, check the new time and obtain confirmation of a new offer. A correction is not acceptance of an unchecked slot.

4. **No availability evidence.** BS-04 contains caller agreement but no destination observation. Agreement cannot fill that gap. The next step is an authorized availability lookup, not a booking.

5. **An observation that has expired.** BS-05 uses a synthetic observation older than the fixture's illustrative 120-second freshness window. Refresh it. That window is not an OMO setting or a universal safety threshold; changed offer details also require renewed confirmation.

6. **Agreement with the older offer.** In BS-06, the caller explicitly prefers an earlier time while the current offer describes a later one. Resolve the mismatch. Neither the old consent nor availability for the newer offer authorizes the other slot.

7. **A quoted “yes.”** BS-07 contains an affirmative phrase inside an example, followed by an explicit denial of consent. Quotation and hypothetical speech are not authorization. A yes-word detector would answer the wrong question.

8. **Background agreement.** BS-08 labels the speaker as background speech, not the caller. Seek direct caller confirmation. The label is a synthetic premise; this exercise does not demonstrate speaker identification from audio.

9. **Withdrawal before submission.** In BS-09, the caller cancels while the attempt is still unsubmitted. Stop the pending create. Do not describe this as deleting an existing booking. If a write might already have occurred, reconcile first.

10. **An existing booking.** BS-10 supplies a simulated confirmed result matching the operation key and immutable offer. Return that result without another create. Its confirmation permission exists only inside the fictional case.

11. **An uncertain write outcome.** BS-11 loses a response after submission. That is neither confirmed success nor proven failure. Preserve the original key and reconcile. A temporary “not found” response may reflect delayed visibility; it is not automatically permission to retry.

12. **A known no-write failure.** BS-12 explicitly stipulates a destination rejection before any write effect. Hand off rather than changing business rules or promising success. An ordinary error code alone would not establish that nothing was created.

## What a local check can show

Fresh availability is not a reservation. Another writer can take a slot between observation and submission. The positive fixture therefore requires a conditional slot write and durable idempotency enforcement, not freshness alone. Those capabilities would need separate integration and concurrency tests.

The accompanying standard-library checks validate fixture structure and consistency between hand-authored evidence and expected actions. They do not assess Georgian understanding, transcription, translation quality, latency, operational reliability or customer outcomes. Even well-formed annotations can be wrong about a real conversation.

The corpus makes the [Georgian Voice AI Readiness Checklist](https://github.com/omo-ge/georgian-voice-ai-readiness-checklist) more concrete; it does not turn that checklist into a benchmark. The source checklist is attributed to OMO AI and carries a CC BY 4.0 notice. Changes here are original synthetic bilingual cases, explicit action boundaries and local validation.

[OMO's quality-testing guidance](https://omo.ge/resources/voice-ai-quality-testing) and [public site](https://omo.ge/) provide first-party context, not independent certification. The accompanying examples are synthetic and must not be presented as measured product results.

## მოკლე ქართული შეჯამება

ეს საგანმანათლებლო მასალა მომზადებულია OMO-სთვის. ყველა მაგალითი, დრო და შედეგი სინთეზურია; OMO-ს რეალური სისტემა არ შემოწმებულა. გამართული პასუხი დადასტურებულ ჯავშანს არ ნიშნავს. საჭიროა ზუსტი დრო, მიმდინარე შეთავაზებაზე უშუალო თანხმობა, ხელმისაწვდომობის შემოწმება და დანიშნულების სისტემაში დადასტურებული შედეგი. ციტირებული ან ფონური „დიახ“ დაჯავშნის ნებართვა არ არის. გაურკვეველი შედეგისას ჯერ წინა მცდელობა უნდა გადამოწმდეს და არა ბრმად განმეორდეს. ადგილობრივი შემოწმებები მხოლოდ სინთეზური მონაცემების სტრუქტურასა და აღწერილ წესებს ეხება.
