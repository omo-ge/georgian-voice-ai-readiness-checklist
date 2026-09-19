# Georgian Voice AI Readiness Workbook / მზადყოფნის სამუშაო ცხრილი

A fillable companion to the [readiness checklist](../README.md), with **38 bilingual
checks across seven sections**. It starts entirely **not assessed**. It is not a
completed assessment of OMO, a customer deployment, a certification or a benchmark.

## Download and use

- [Spreadsheet-friendly CSV](readiness-workbook.csv) — UTF-8 with BOM; import into
  Excel or Google Sheets. There are no macros or spreadsheet formulas.
- [Equivalent structured JSON](readiness-workbook.json) — the same rows and fields.
- [Original checklist](../README.md) — explanations and the minimum pilot gate.
- [12 synthetic booking examples](../examples/booking-safety/) — optional learning
  material, not evidence that a real deployment passed a test.

1. Make a private copy. Record the workflow and version being assessed separately.
2. Assign an owner and an ISO date (`YYYY-MM-DD`) where follow-up is needed.
3. Choose `not_assessed`, `ready`, `needs_work` or `not_applicable`.
4. For `ready`, record a reviewable evidence reference and reviewer notes.
5. For `not_applicable`, explain why; for `needs_work`, assign remediation.
6. Review critical blockers individually. Do not treat a percentage of checked rows
   as authorization to launch. Agree the actual pilot and rollback gates with owners.

`source_url` points to the exact source commit and section. It is a provenance link,
**not** evidence that the requirement is satisfied. `evidence_reference` is where
your team points to its own restricted test or decision record.

## ქართული ინსტრუქცია

ცხრილი შეიცავს **38 ორენოვან შემოწმებას შვიდ განყოფილებაში**. ყველა პუნქტის საწყისი
სტატუსია `not_assessed` — შეფასება ჯერ არ ჩატარებულა.

შექმენით პირადი ასლი. თითოეული პუნქტისთვის მიუთითეთ პასუხისმგებელი, საჭიროებისას
ვადა, სტატუსი და გადამოწმებადი მტკიცებულების მითითება. `ready` ნიშნავს, რომ მოთხოვნა
განსაზღვრულია, შემოწმებულია და ჰყავს პასუხისმგებელი; `needs_work` — სამუშაო დარჩენილია;
`not_applicable` — საჭიროა წერილობითი დასაბუთება.

`source_url` ასახელებს საწყის სახელმძღვანელოს და არა შესრულების მტკიცებულებას.
რეალური შემოწმების ჩანაწერზე მითითებისთვის გამოიყენეთ `evidence_reference`.
შევსებული ასლი შეინახეთ პირადად. არ ატვირთოთ მომხმარებელთა ნომრები, საუბრები,
პაციენტების მონაცემები, გასაღებები ან შიდა წვდომის ბმულები საჯარო რეპოზიტორიაში.
მხოლოდ მონიშნული პუნქტების პროცენტი არ ამტკიცებს რეალურ გარემოში გაშვების მზადყოფნას.

## Provenance and reuse

The English requirements are extracted, in order, from the repository's existing
checklist. Georgian translations match each of the 38 English requirements; the
shorter Georgian narrative in older versions was not a one-to-one row mapping.
This workbook and its translations were prepared with AI assistance and checked
for row parity, completeness and file consistency. Those checks do not replace
business, linguistic, legal, privacy or security review.

Maintainer: [OMO AI](https://omo.ge/en). Reuse under the checklist's existing
[CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/), with attribution.
For a version-specific citation, use [CITATION.cff](../CITATION.cff) and name the
release or commit you actually used.
