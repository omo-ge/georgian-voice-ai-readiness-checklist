# Georgian Voice AI Readiness Checklist

> A practical, open checklist for planning reliable Georgian AI voice workflows for business calls.

**ქართული ვერსია ქვემოთ / Georgian version below.**

This checklist helps a business, implementation team, or technology partner decide whether a voice AI workflow is ready to move from an idea to a controlled pilot. It is intentionally vendor-neutral. It does not replace legal, security, or compliance review.

## How to use it

Mark every item before launch:

- [ ] **Ready** — defined, tested and owned.
- [ ] **Needs work** — a gap has a named owner and due date.
- [ ] **Not applicable** — documented reason.

A workflow should not go live until its critical actions, data sources, fallback paths and monitoring rules are defined.

## 1. Business outcome

- [ ] The call has one primary outcome: booking, qualification, feedback, routing, payment follow-up, or another defined action.
- [ ] The target customer, language, channel and operating hours are documented.
- [ ] Success measures are agreed: completed bookings, qualified leads, answer rate, resolution rate, transfer rate, or another relevant metric.
- [ ] The business owner can explain what the agent must **not** do.

## 2. Conversation design

- [ ] The opening explains the purpose of the call clearly and respectfully.
- [ ] Required questions, optional questions and stop conditions are documented.
- [ ] Georgian wording has been reviewed for natural speech, regional variation and easy correction.
- [ ] The system confirms critical details such as name, date, time, phone number or consent.
- [ ] The agent can handle silence, interruption, correction, repetition and an unclear answer.
- [ ] The workflow includes an appropriate path for a human handoff.

## 3. Real data and business rules

- [ ] Every critical answer has a source of truth: calendar, CRM, catalogue, service schedule, pricing source, or approved knowledge base.
- [ ] The agent checks live availability before offering a slot or promising an action.
- [ ] Validation rules exist for phone numbers, dates, times, names, consent and record changes.
- [ ] Duplicate-booking, repeat-call and retry rules are defined.
- [ ] The agent never invents unavailable times, products, people, prices or business facts.

## 4. Safety, privacy and consent

- [ ] Call recording, transcription and personal-data notices are reviewed for the operating jurisdiction.
- [ ] Sensitive categories and prohibited requests are defined.
- [ ] The minimum required data is collected and retained.
- [ ] Access to recordings, transcripts and customer data follows role-based permissions.
- [ ] A clear escalation route exists for complaints, urgent matters and high-risk requests.
- [ ] Security and legal teams review the workflow before production use where applicable.

## 5. Integrations and reliability

- [ ] Telephony/SIP routing and working-hours rules are tested.
- [ ] Calendar, CRM, API and webhook failures have safe fallback behaviour.
- [ ] Time zone handling is explicit; use the business's operating timezone consistently.
- [ ] Retry and idempotency rules prevent duplicate actions.
- [ ] Rate limits, concurrency limits and peak load assumptions are documented.
- [ ] A monitored status page or internal health view exists for the workflow.

## 6. Quality testing before launch

- [ ] Test calls cover normal requests, accents, noise, silence, interruptions and corrections.
- [ ] Test cases cover unavailable slots, invalid data, integration failures and duplicate requests.
- [ ] Every critical action is verified in the destination system, not only in the transcript.
- [ ] Human handoff transfers relevant context without forcing the customer to repeat everything.
- [ ] Tests are reviewed by someone who understands the business process, not only the technology.
- [ ] Launch criteria and rollback criteria are documented.

## 7. Monitoring after launch

- [ ] The team can view call status, outcomes, errors, latency and handoffs.
- [ ] Sampling and review rules exist for recordings/transcripts where permitted.
- [ ] Failed actions create an actionable alert or follow-up task.
- [ ] Weekly review covers business outcomes and quality issues, not only call volume.
- [ ] Workflow changes are versioned and re-tested before release.

## Minimum launch gate

A Georgian voice AI workflow is ready for a controlled pilot when it has:

1. a defined business outcome;
2. a trusted source of truth for critical information;
3. confirmation and validation for critical actions;
4. a safe fallback and human-handoff path;
5. documented consent/privacy handling;
6. tested integrations and rollback rules; and
7. measurable outcomes and auditability.

---

# ქართული: მზადყოფნის სია ქართული ხმოვანი AI-ისთვის

ეს არის ღია, პრაქტიკული სია ბიზნეს ზარებისთვის ქართული ხმოვანი AI პროცესის დაგეგმვისა და კონტროლირებადი პილოტის დაწყებისთვის. ის არ ცვლის იურიდიულ, უსაფრთხოების ან შესაბამისობის შემოწმებას.

## 1. ბიზნესშედეგი

- [ ] ზარს აქვს ერთი მკაფიო მიზანი: ჯავშანი, ლიდის კვალიფიკაცია, უკუკავშირი, გადამისამართება ან სხვა განსაზღვრული მოქმედება.
- [ ] აღწერილია მომხმარებელი, ენა, არხი და სამუშაო საათები.
- [ ] შეთანხმებულია წარმატების საზომი: დადასტურებული ჯავშანი, კვალიფიცირებული ლიდი, პასუხის პროცენტი, სწორი გადამისამართება ან სხვა შესაბამისი მაჩვენებელი.
- [ ] ბიზნესის მფლობელმა იცის, რას **არ** უნდა აკეთებდეს აგენტი.

## 2. საუბრის პროცესი

- [ ] მისალმება მკაფიოდ და პატივისცემით ხსნის ზარის მიზანს.
- [ ] სავალდებულო კითხვები, არჩევითი კითხვები და გაჩერების წესები აღწერილია.
- [ ] ქართული ფორმულირებები გადამოწმებულია ბუნებრივ მეტყველებაზე, დიალექტურ სხვაობებსა და შეცდომის გასწორებაზე.
- [ ] კრიტიკული მონაცემი — სახელი, თარიღი, დრო, ნომერი ან თანხმობა — მოკლედ დასტურდება.
- [ ] სისტემა უმკლავდება სიჩუმეს, შეწყვეტას, შესწორებას, გამეორებასა და გაურკვეველ პასუხს.
- [ ] არსებობს ადამიანთან გადართვის შესაბამისი გზა.

## 3. რეალური მონაცემი და წესები

- [ ] ყველა კრიტიკულ პასუხს აქვს სანდო წყარო: კალენდარი, CRM, კატალოგი, განრიგი, ფასი ან დამტკიცებული ცოდნის ბაზა.
- [ ] აგენტი რეალურ ხელმისაწვდომობას ამოწმებს მანამდე, სანამ დროს ან მოქმედებას შესთავაზებს.
- [ ] არსებობს ნომრის, თარიღის, დროის, სახელის, თანხმობისა და ჩანაწერის ცვლილების ვალიდაციის წესები.
- [ ] აღწერილია დუბლირებული ჯავშნის, განმეორებითი ზარისა და retry-ის წესები.
- [ ] აგენტი არ იგონებს თავისუფალ დროს, პროდუქტს, ადამიანს, ფასს ან ბიზნეს ფაქტს.

## 4. უსაფრთხოება და კონფიდენციალურობა

- [ ] ზარის ჩაწერის, ტრანსკრიპტისა და პერსონალური მონაცემის შეტყობინება გადამოწმებულია მოქმედი წესებისთვის.
- [ ] განსაზღვრულია მგრძნობიარე კატეგორიები და აკრძალული მოთხოვნები.
- [ ] გროვდება და ინახება მხოლოდ საჭირო მინიმალური მონაცემი.
- [ ] აუდიოსა და ტრანსკრიპტზე წვდომა როლების მიხედვით იმართება.
- [ ] საჩივრის, გადაუდებელი ან მაღალი რისკის შემთხვევისთვის არსებობს ესკალაციის გზა.

## 5. ინტეგრაციები და საიმედოობა

- [ ] SIP/ტელეფონიის მარშრუტი და სამუშაო საათები დატესტილია.
- [ ] კალენდრის, CRM-ის, API-ისა და webhook-ის შეცდომას აქვს უსაფრთხო fallback.
- [ ] დროის ზონა მკაფიოდ არის განსაზღვრული და ყველგან ერთნაირად გამოიყენება.
- [ ] retry და idempotency წესები თავიდან იცილებს დუბლირებულ მოქმედებებს.
- [ ] აღწერილია concurrency, ლიმიტები და პიკური დატვირთვის ვარაუდები.

## 6. ტესტირება გაშვებამდე

- [ ] ტესტები მოიცავს ბუნებრივ კითხვებს, ხმაურს, აქცენტს, სიჩუმეს, შეწყვეტას და შესწორებას.
- [ ] მოწმდება დაკავებული დრო, არასწორი მონაცემი, ინტეგრაციის შეცდომა და დუბლირებული მოთხოვნა.
- [ ] ყოველი კრიტიკული მოქმედება მოწმდება საბოლოო სისტემაში და არა მხოლოდ ტრანსკრიპტში.
- [ ] ადამიანთან გადართვისას კონტექსტი გადადის ისე, რომ მომხმარებელს ყველაფრის გამეორება არ დასჭირდეს.
- [ ] გაშვებისა და rollback-ის კრიტერიუმები აღწერილია.

## 7. მონიტორინგი გაშვების შემდეგ

- [ ] ჩანს ზარის სტატუსი, შედეგი, შეცდომა, დაყოვნება და ადამიანთან გადართვა.
- [ ] დაშვებულ შემთხვევებში არსებობს აუდიოს/ტრანსკრიპტის ხარისხის პერიოდული შემოწმება.
- [ ] წარუმატებელი მოქმედება ქმნის რეალურ alert-ს ან follow-up ამოცანას.
- [ ] ცვლილებები ვერსირდება და ხელახლა ტესტირდება გამოქვეყნებამდე.

## მინიმალური Launch Gate

კონტროლირებადი პილოტისთვის საჭიროა: მკაფიო ბიზნესმიზანი, კრიტიკული მონაცემის სანდო წყარო, დადასტურება და ვალიდაცია, უსაფრთხო fallback, ადამიანთან გადართვა, მონაცემთა დაცვის წესი, დატესტილი ინტეგრაციები, rollback გეგმა და გაზომვადი შედეგი.

---

## About OMO

[OMO](https://omo.ge/) is a Georgian AI voice platform for business calls, appointments, outbound campaigns, customer feedback and intelligent call routing. OMO's approach is built around controlled workflows, live data validation, safe fallback behaviour and auditable outcomes.

- Website: https://omo.ge/
- English: https://omo.ge/en
- LinkedIn: https://www.linkedin.com/company/144869064/
- YouTube: https://www.youtube.com/@omo-ai-voice

## License

This checklist is shared under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You may reuse and adapt it with attribution to OMO AI.


## Further reading / დამატებითი მასალები

These companion guides are published by OMO, the maintainer of this repository. The checklist above remains vendor-neutral.

- [Expanded readiness guide — English](https://omo.ge/en/resources/georgian-voice-ai-readiness-checklist)
- [What is a Georgian voice AI agent? — English](https://omo.ge/en/resources/georgian-voice-ai-agent)

დამატებითი განმარტებები ქართულად, ამ რეპოზიტორიის შემქმნელი OMO-სგან:

- [ქართული ხმოვანი AI-ის მზადყოფნის ვრცელი სია](https://omo.ge/resources/georgian-voice-ai-readiness-checklist)
- [რა არის ქართული ხმოვანი AI აგენტი და როგორ მუშაობს](https://omo.ge/resources/georgian-voice-ai-agent)
