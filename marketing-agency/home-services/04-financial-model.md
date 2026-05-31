# Home Services Agency — Financial Model
### Vertical: HVAC · Plumbing · Electrical

A simple, conservative model you can plug your own numbers into. Three parts: **acquisition funnel
math**, **unit economics per client**, and a **12-month MRR ramp**. All figures are illustrative
starting assumptions — replace with your real conversion rates as you get data.

---

## 1. Acquisition funnel (how many prospects → one client)

Driven by the audit-first cold email + AI-voice engine in `03-outreach-sequences.md`.

| Stage | Rate | From 1,000 contacted |
|---|---|---|
| Prospects contacted | — | 1,000 |
| Positive reply | 8% | 80 |
| Booked discovery call | 30% of replies | 24 |
| Showed up | 70% | 17 |
| Closed to client | 30% of shows | **~5** |

**≈ 5 clients per 1,000 quality prospects contacted.** (Early on assume worse — 2–3 — until your
audit, list quality, and sales calls are dialed.)

### What that costs (CAC)

| Cost item | Monthly | Notes |
|---|---|---|
| Sending infra (Smartlead/Instantly + domains + inboxes) | ~$150 | scales slowly |
| Lead data + enrichment (Outscraper + Clay) | ~$350 | per ~2–4k leads |
| AI voice (Vapi/Bland) usage | ~$200 | per-minute |
| Your/SDR time | variable | mostly the sales calls |
| **Total to contact ~2,000/mo** | **~$700** | yields ~10 clients/mo at mature rates |

**Blended CAC ≈ $70–150 per client** at mature conversion — well under the "1× first-month
revenue" ($2,800) ceiling. Even at 3× worse conversion you're under $500. This is the whole reason
automated outreach makes the model work.

---

## 2. Unit economics (per client)

Blended across tiers (assume mix skews to Tier 2 "Growth" at $3,000).

| Metric | Value |
|---|---|
| Avg. monthly retainer (blended) | **$2,800** |
| One-time setup fee | $1,000 (recognized month 1) |
| Tooling cost per client (GHL sub-acct share, Twilio, CallRail, AI mins) | ~$250/mo |
| Fulfillment labor per client (at scale, automated) | ~$300/mo |
| **Gross margin per client** | **~$2,250/mo (~80%)** |
| Avg. client lifespan | 12 months (conservative; good agencies hit 18–24) |
| **LTV (gross margin × lifespan)** | **~$27,000** |
| CAC | ~$150 |
| **LTV:CAC** | **~180:1** (the constraint is fulfillment capacity, not CAC) |

> The bottleneck in this business is **never** lead cost — it's how many clients one operator +
> automations can fulfill well. Protect retention and fulfillment quality above all.

---

## 3. Twelve-month MRR ramp (conservative)

Assumes you add **3 net new clients/month** months 1–4 (while building), then **5–6/month** once
the outreach engine is mature, minus **~5% monthly churn**.

| Month | New | Churn | Active clients | MRR (@$2,800) | Notes |
|---|---|---|---|---|---|
| 1 | 2 | 0 | 2 | $5,600 | Manual closes, building snapshot |
| 2 | 3 | 0 | 5 | $14,000 | First reactivation wins |
| 3 | 4 | 0 | 9 | $25,200 | Outreach engine live |
| 4 | 5 | 1 | 13 | $36,400 | |
| 5 | 6 | 1 | 18 | $50,400 | **~$50k MRR milestone** |
| 6 | 6 | 1 | 23 | $64,400 | Consider first hire (fulfillment) |
| 7 | 6 | 1 | 28 | $78,400 | |
| 8 | 6 | 2 | 32 | $89,600 | |
| 9 | 7 | 2 | 37 | $103,600 | **$100k MRR** |
| 10 | 7 | 2 | 42 | $117,600 | |
| 11 | 7 | 2 | 47 | $131,600 | |
| 12 | 7 | 3 | 51 | $142,800 | ~$1.7M run-rate |

### Rough P&L at month 12 (~51 clients)

| Line | Monthly |
|---|---|
| Revenue (MRR) | ~$142,800 |
| Tooling (~$250/client + platform fees) | ~$15,000 |
| Outreach/acquisition | ~$1,500 |
| Fulfillment team (2–3 people) | ~$25,000 |
| Software/overhead | ~$5,000 |
| **Approx. operating profit** | **~$95k/mo (~65% margin)** |

---

## 4. The numbers that actually move this model

1. **Churn.** Going from 5% → 3% monthly churn roughly doubles steady-state client count. Retention
   = the reactivation/missed-call ROI being *visible* in the monthly report. Obsess over this.
2. **Close rate on calls.** 30% → 40% is a 33% increase in clients for the *same* ad/outreach spend.
   The audit-first approach is what lifts this.
3. **Fulfillment capacity per operator.** Every automation that lets one person handle 15 clients
   instead of 8 directly drops your cost line and raises margin.
4. **Tier mix.** Nudging clients from Tier 1 ($1,500) to Tier 2 ($3,000) via LSA management is the
   easiest revenue expansion — same client, ~2× revenue.

> Plug your real reply/close/churn rates in here monthly. The model is only as good as the inputs,
> and your first 10 clients will tell you the true numbers.
