# CRM cross-check runbook (registration or attendee list)

Read-only against CRM. Report findings, wait for a yes, then act. Never delete or edit CRM rows from this skill.

1. Inputs: Zoom registration export (tabs "Registration List" and "Recording Request") or attendee CSV (`pandas.read_csv(..., skiprows=4)`; columns `Display Name`, `Attendee Email`). Lowercase and dedupe emails first.
2. Salesforce, batches of 35 to 40 emails per IN clause:
   `SELECT Email, FirstName, LastName, Account.Name, Account.Type, Account.Sales_Stage__c, Account.ICP__c, Account.Organization_Type__c, Owner.Name FROM Contact WHERE Email IN (...)` via soqlQuery. Duplicate contacts on one email: take the first. Nulls show as "(blank)". CSM fields come from Account (`Onboarding_CSM__c, Post_Onboarding_CSM__c, Backup_CSM__c`). Account name misses: SOSL via find, `FIND {NASP*} IN NAME FIELDS RETURNING Account(Id, Name)`.
3. HubSpot pass for the unmatched: search_crm_objects CONTACT, one filter group, operator IN, values = emails. Return hs_object_id, email, name, company, jobtitle, lifecyclestage, hs_analytics_source. Expect Salesforce to match 92 to 96%.
4. Deliverable: two-tab workbook written with openpyxl. Tab 1 "Summary" (counts by sales stage, ICP, account type, as formulas). Tab 2 "Attendee Detail" color-coded: active pipeline, demo-unperformed re-engage, former-client win-back, ICP with no stage, unmatched highlighted.
5. Cleanup notes (reported, never auto-applied): duplicate registrants, internal or vendor registrants to exclude, contacts whose account is not linked.
6. Session metrics: registrations, registrations plus deduped recording requests, attendees, attendee rate = attendees / registrations.
