# Home Services Agency — Automation Build Specs (Make.com / n8n)
### Vertical: HVAC · Plumbing · Electrical

Implementation blueprints for the two engines. Each scenario is described as **trigger → steps →
output**, tool-agnostic enough to build in Make.com (start here — easier) or n8n (self-host later
to cut cost). GoHighLevel (GHL) is the CRM/messaging hub throughout.

---

## Engine A — Client Acquisition scenarios

### A1. Lead sourcing & enrichment
- **Trigger:** scheduled (weekly) or manual run per target metro.
- **Steps:**
  1. Outscraper (or Apify Google Maps scraper) → pull businesses for `{HVAC|plumber|electrician}`
     + `{metro}`. Fields: name, address, phone, website, GBP rating, review count, category.
  2. Push rows → Clay table.
  3. Clay enrichment: find owner first name, verify/append email (Clay waterfall), detect if running
     Google Ads/LSA, normalize city.
  4. Clay formula → `lead_score` (high if rating < 4.5 OR reviews < 75 OR no website).
  5. Clay formula → `est_missed_calls` (conservative range from category + review volume proxy).
  6. Email verification (NeverBounce) → drop invalid/risky.
- **Output:** clean, scored, enriched rows with all `{{merge}}` variables from doc 03.

### A2. Audit asset generation
- **Trigger:** Clay row reaches `status = ready` and `lead_score = high`.
- **Steps:**
  1. Make webhook receives the row.
  2. Merge variables into an audit template (landing page via GHL funnel, or a generated
     PDF/Loom-style page). One unique URL per prospect.
  3. Write `audit_link` back to the Clay row.
- **Output:** per-prospect `audit_link` ready for sequences.

### A3. Multichannel outreach dispatch
- **Trigger:** row `status = ready` + `audit_link` present.
- **Steps:**
  1. Push to Smartlead/Instantly campaign (maps merge fields → email sequence in doc 03).
  2. In parallel, queue AI-voice first-touch (Vapi/Bland) with the call script + `audit_link`
     send-by-email action on positive response.
  3. Respect per-domain daily caps; rotate inboxes.
- **Output:** prospect entered into live multichannel sequence; activity logged to Clay/GHL.

### A4. Reply → booking → CRM
- **Trigger:** positive reply (Smartlead reply webhook) or AI-voice "interested" outcome.
- **Steps:**
  1. Create/zupdate contact in GHL (agency sales pipeline, stage = "Replied").
  2. Send calendar link / AI voice books directly into GHL calendar.
  3. On booking → stage "Call Booked"; fire reminder sequence (email + SMS to *opted-in* booker is
     fine — they engaged); on no-show → reschedule sequence.
  4. Auto-suppress contact from cold sequences (no double-touching).
- **Output:** booked discovery calls landing in your calendar; clean pipeline stages.

### A5. Won → onboarding handoff
- **Trigger:** GHL opportunity moved to "Won".
- **Steps:**
  1. Stripe: create customer + subscription (retainer) + one-time setup charge.
  2. Fire Engine B onboarding (B0).
- **Output:** billing live, delivery setup kicked off.

---

## Engine B — Delivery / Fulfillment scenarios (per client sub-account)

### B0. Onboarding & snapshot deploy
- **Trigger:** "Won" (from A5) or manual.
- **Steps:**
  1. Create GHL **sub-account** from your **snapshot template** (pre-built with B1–B6 workflows,
     pipelines, templates).
  2. Send intake form (collect: GBP access, business phone, CRM type — ServiceTitan/Housecall
     Pro/Jobber, past-customer CSV/API, service offers, opt-out footer text).
  3. Connect GBP, provision Twilio number + CallRail tracking, set up email/SMS sending identity.
  4. Import + dedupe past-customer list; tag segments (e.g. `no_service_12mo`, `install_8yr_plus`).
- **Output:** fully configured client sub-account, identical to every other client.

### B1. Missed-Call Text-Back
- **Trigger:** inbound call to tracking number ends as missed/abandoned (Twilio/CallRail event).
- **Steps:** instant SMS from business number → "Sorry we missed you at {{company}} — what do you
  need help with?" → replies open a GHL conversation → route to booking / notify dispatch.
- **Output:** recovered call becomes a tracked conversation + potential booked job.
- **Compliance:** SMS to someone who just called you = clear consent; still include opt-out.

### B2. Speed-to-Lead
- **Trigger:** new lead (web form, LSA lead, ad lead) hits GHL.
- **Steps:** within 60s → auto-call bridges contractor ↔ lead (Twilio) **and** sends intro SMS +
  email; if no connect, start short call/text cadence until booked or dead.
- **Output:** sub-minute first response — the single biggest lever on booking rate.

### B3. Review Engine
- **Trigger:** job marked complete in client CRM (ServiceTitan/Housecall Pro/Jobber webhook → Make).
- **Steps:** wait 2–4h → SMS + email review request → if rating ≥ 4 route to Google review link;
  if ≤ 3 route to private feedback form (alerts owner, protects public rating).
- **Output:** steady Google review velocity; bad experiences intercepted privately.

### B4. Database Reactivation
- **Trigger:** scheduled seasonal campaigns + on-demand.
- **Steps:** select segment (e.g. `no_service_12mo`) → send SMS + email seasonal offer (spring AC
  tune-up, winter heating safety check) → responders routed to booking → measure booked jobs.
- **Output:** booked jobs from existing customers — the fastest week-one ROI.
- **Compliance:** existing-customer relationship; every message carries opt-out, honored instantly.

### B5. Lead Nurture
- **Trigger:** lead created but not booked within X hours.
- **Steps:** multi-day value + offer drip (email + opted-in SMS) until booked or marked dead; stop
  on booking.
- **Output:** recovered slow leads; nothing falls through cracks.

### B6. Reporting
- **Trigger:** monthly schedule.
- **Steps:** pull GBP (reviews delta), CallRail (calls recovered), ads (LSA/Google spend + leads),
  GHL (jobs booked) → populate Looker Studio template → auto-email + post to client GHL dashboard.
- **Output:** one-page ROI report headlining calls recovered, reviews gained, jobs booked, ad ROI.

---

## Architecture notes & gotchas

- **GHL snapshot = your product.** Build B1–B6 once inside a template sub-account; every new client
  is a clone. Changes to the playbook = update snapshot, roll forward.
- **Make first, n8n later.** Make is faster to build/visualize; once you have >15 clients and the
  scenarios are stable, self-hosting n8n cuts per-operation cost meaningfully.
- **CRM webhooks vary.** ServiceTitan has a real API (job-complete events); Housecall Pro/Jobber
  have APIs/Zapier hooks too. Abstract "job complete" into one internal Make webhook so B3 doesn't
  care which CRM the client uses.
- **One suppression source of truth.** Sync unsubscribes/opt-outs across Smartlead, GHL, and all
  inboxes so a opt-out never gets re-contacted on any channel.
- **Idempotency.** Guard scenarios against duplicate triggers (e.g. a call event firing twice) with
  a dedupe key so you don't double-text leads.
- **Secrets/keys.** Store API keys in the platform's vault/connections, never in plaintext modules.

---

## Build order (maps to doc 02)

1. **B0 + B1 + B3 + B4** inside one GHL snapshot → this is the minimum sellable product.
2. **B6** reporting (clients must *see* the ROI or they churn).
3. **A1–A5** acquisition engine once you've run delivery manually for 1–2 clients.
4. **B2 + B5 + AI receptionist** as you move clients to Tier 2.

## Day-one vs. add-later (orchestration layer)

You do **not** need a full Make.com/n8n build to start. Lean on GoHighLevel native workflows
first; add the orchestration layer only when a scenario actually requires cross-tool plumbing.

**Day one (no/minimal Make — runs inside GHL or its native integrations):**
- B1 Missed-Call Text-Back · B4 Database Reactivation · B5 Lead Nurture · A4 reply→booking — all
  native GHL workflows.
- B3 Review Engine *if* you trigger it manually or via GHL's own "job complete" tag at first.

**Add later (this is where Make/n8n earns its keep):**
- B3 Review Engine via **client CRM webhook** (ServiceTitan/Housecall Pro/Jobber → Make) — needed
  once clients want it fully hands-off.
- B6 cross-platform **reporting aggregation** (GBP + CallRail + ads + GHL → Looker).
- A1–A3 **scraping → Clay enrichment → audit generation → outreach dispatch** pipeline.
- B2 Speed-to-Lead auto-dial bridge and AI receptionist.

Self-host n8n only once you're past ~15 clients and scenarios are stable (cost optimization).
