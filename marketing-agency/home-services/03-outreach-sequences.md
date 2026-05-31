# Home Services Agency — Cold Outreach Sequences & Scripts
### Vertical: HVAC · Plumbing · Electrical

The outreach playbook for **Engine A (Client Acquisition)**. Everything here is built around one
principle: **lead with a personalized audit ("show, don't tell"), not a pitch.** You are showing a
contractor money they're already leaving on the table.

> ⚖️ **Compliance first:** Email follows CAN-SPAM (physical address + honored one-click opt-out,
> warmed separate domains). Calls follow TCPA/DNC (scrub published business lines, AI voice must
> disclose it's an AI and the company it represents). **No cold SMS to prospects** — SMS is for the
> client's *opted-in* past customers only (Engine B).

---

## The personalization variables (computed per prospect in Clay)

Every message is assembled from data you already scraped/enriched:

| Variable | Source | Example |
|---|---|---|
| `{{first_name}}` | Clay enrichment | "Mike" |
| `{{company}}` | Google Maps | "Allstar Heating & Air" |
| `{{city}}` | Google Maps | "Tucson" |
| `{{trade}}` | classification | "HVAC" |
| `{{star_rating}}` | GBP scrape | "4.1" |
| `{{review_count}}` | GBP scrape | "38" |
| `{{competitor_name}}` | top-ranked nearby | "Desert Comfort" |
| `{{competitor_rating}}` / `{{competitor_reviews}}` | GBP scrape | "4.8 / 220" |
| `{{est_missed_calls}}` | calc (see below) | "~18/month" |
| `{{audit_link}}` | generated asset | loom/landing URL |

**Missed-call estimate (defensible, conservative):** assume a busy trades shop takes 150–400
calls/mo and misses 20–30%. Anchor low and frame as a range so it's credible, not hypey.

---

## Sequence 1 — Cold Email (primary channel)

5 touches over ~12 business days, one thread. Plain-text style, no images, no links in email #1
(protects deliverability). The audit link appears from email #2 onward.

### Email 1 — Day 1 — the observation (no ask, no link)
> **Subject:** `{{competitor_name}} vs {{company}}`
>
> Hi {{first_name}},
>
> Quick one — I was looking at {{trade}} companies in {{city}} and noticed {{company}} is at
> {{star_rating}}★ with {{review_count}} reviews, while {{competitor_name}} is sitting at
> {{competitor_rating}}★ with {{competitor_reviews}}.
>
> On Google, that review gap is quietly sending a chunk of "{{trade}} near me" calls their way
> instead of yours.
>
> Worth me sending over a 2-minute breakdown of where those calls are going?
>
> — {{your_name}}, {{your_company}}
> {{physical_address}} · unsubscribe: {{unsub_link}}

### Email 2 — Day 3 — deliver the audit
> **Subject:** `re: {{competitor_name}} vs {{company}}`
>
> {{first_name}} — made you that breakdown: {{audit_link}}
>
> Short version: you're likely missing **{{est_missed_calls}}** calls a month (after-hours, on
> other lines, on jobs). For {{trade}}, even one recovered install can be $8–12k.
>
> We fix that with two things most shops aren't doing: instant text-back on missed calls, and a
> reactivation campaign to your past customers. Open to a 15-min call this week?

### Email 3 — Day 6 — proof / specificity
> **Subject:** `the past-customer goldmine`
>
> The fastest money isn't new leads — it's the customers already in your system. A {{trade}} shop
> we worked with texted their list a tune-up offer and booked 20+ jobs in the first week.
>
> You've got years of customers who haven't heard from you. Want me to show you what that list is
> worth?

### Email 4 — Day 9 — objection pre-empt
> **Subject:** `not asking you to switch anything`
>
> {{first_name}} — to be clear, this doesn't touch how you run jobs or your dispatch software. It
> sits on top of your existing phone and customer list and just stops leads from leaking out.
>
> 15 minutes and I'll show you the missed-call number live. {{audit_link}}

### Email 5 — Day 12 — breakup
> **Subject:** `should I close this out?`
>
> Haven't heard back, so I'll assume the timing's off and stop here. If recovering missed {{trade}}
> calls in {{city}} ever moves up the list, just reply "reviews" and I'll reopen it.
>
> Either way — good luck this season.

**Targets:** ~8% reply, ~25% of replies book. Tune subject lines first (biggest lever), then email 1.

---

## Sequence 2 — AI Voice / Cold Call (high-converting for trades)

Owners live on the phone. Use an AI voice agent (Vapi/Bland) for first touch + booking, or a human
SDR with this script. **Mandatory disclosure** at the top.

### Opening (disclosure + pattern interrupt)
> "Hi, is this {{first_name}}? — Quick heads up, this is an AI assistant calling on behalf of
> {{your_company}}, I'll be 30 seconds. I was comparing {{trade}} companies in {{city}} and noticed
> {{company}} has {{review_count}} reviews while {{competitor_name}} has {{competitor_reviews}} —
> can I send you a quick breakdown of how that's affecting your call volume?"

### If yes → capture + book
> "Perfect — what's the best email? ... Sent. It shows you're likely missing around
> {{est_missed_calls}} calls a month. Worth 15 minutes with our team to walk through fixing it?
> I've got Thursday at 9 or 2 open."

### Common objections (one-liners)
- *"We're too busy / booked out."* → "Totally — this is for the slower stretch and for the calls
  you can't get to right now. Takes nothing to set up. Worth a look for when it cools off?"
- *"We already do marketing."* → "Most shops we help do too — this isn't ads, it's plugging the
  leak on calls that come in and never get answered. Different problem. 15 minutes?"
- *"Send me info."* → "Will do — sending the breakdown now. I'll hold Thursday 2pm so you've got a
  slot if it's useful." (then nurture)

### Voicemail (if no answer)
> "Hi {{first_name}}, {{your_name}} with {{your_company}} — noticed {{company}}'s missing some
> {{trade}} calls to competitors in {{city}}, sent you a quick breakdown by email. No pressure,
> take a look. Thanks!"

---

## Sequence 3 — Follow-up after "send me info" / no-show

Light email drip, max 3 touches, then drop to long-term nurture (monthly value email).

1. **+1 day:** "Here's the breakdown again {{audit_link}} — the missed-call number is on page 1."
2. **+4 days:** Short case-study line + soft re-book link.
3. **+10 days:** Breakup ("closing this out — reply 'reviews' anytime").

---

## The audit asset (what `{{audit_link}}` points to)

Auto-generated per prospect (template + merge in Make). One screen / one Loom covering:
1. Their GBP rating + review count vs the top local competitor (side by side).
2. Estimated missed calls/month and rough dollar value (range, conservative).
3. Three fixes: missed-call text-back · review engine · database reactivation.
4. One CTA button → book a call.

This single asset is the highest-leverage thing in the whole acquisition engine. Make it good.

---

## Deliverability checklist (don't skip — this is the real bottleneck)

- [ ] Separate sending domains (e.g. `getallstar.co`, not your main domain), 2–3 inboxes each
- [ ] 3-week warmup before real sends; ramp slowly
- [ ] ≤ 30 sends/inbox/day, rotated
- [ ] Verify every address (NeverBounce/ZeroBounce) before sending
- [ ] Plain text, minimal/no links in email 1, no spammy words
- [ ] Physical address + working one-click unsubscribe in every email
- [ ] Honor opt-outs instantly; sync suppression list across all inboxes
- [ ] Monitor reply + bounce rates; pause any domain that dips
