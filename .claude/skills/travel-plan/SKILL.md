---
name: travel-plan
description: Build detailed travel itineraries with logistics, packing lists, meeting schedules, and contingency plans for business trips.
allowed-tools: Read Grep Glob Bash WebFetch WebSearch TodoWrite
argument-hint: [destination, dates, purpose, or constraints]
---

# Travel Planning & Coordination

You create comprehensive travel plans that cover every logistical detail so the user can focus on the purpose of their trip, not the logistics.

## Travel Itinerary Template

### Trip: [Destination] — [Purpose]
**Dates:** [Departure] → [Return]
**Traveler:** [Name]

---

#### Pre-Trip Checklist
- [ ] Flights booked (confirmation: ___)
- [ ] Hotel booked (confirmation: ___)
- [ ] Ground transport arranged (rental car / rideshare / driver)
- [ ] Travel docs valid (passport expiry, visa requirements)
- [ ] Travel insurance confirmed
- [ ] Out-of-office set on email/calendar
- [ ] Key contacts notified of travel dates
- [ ] Expense pre-approval obtained (est. budget: $____)
- [ ] Meeting materials prepared and loaded offline
- [ ] Chargers, adapters, essential tech packed

#### Day-by-Day Itinerary

**Day 1 — [Date] (Travel Day)**
| Time | Activity | Location | Notes |
|------|----------|----------|-------|
| HH:MM | Depart [origin] | [Airport/Terminal] | Flight: ___, Seat: ___ |
| HH:MM | Arrive [destination] | [Airport] | Ground transport: ___ |
| HH:MM | Check in | [Hotel, address] | Confirmation: ___ |
| HH:MM | [Dinner / prep / rest] | [Location] | |

**Day 2 — [Date] (Meeting Day)**
| Time | Activity | Location | Notes |
|------|----------|----------|-------|
| ... | ... | ... | ... |

[Continue for each day]

#### Key Contacts
| Role | Name | Phone | Email |
|------|------|-------|-------|
| Hotel | [name] | ... | ... |
| Local host/contact | [name] | ... | ... |
| Travel support | [name] | ... | ... |
| Emergency | [name] | ... | ... |

#### Logistics Notes
- **Timezone:** [Local TZ, offset from home]
- **Currency:** [Local currency, exchange rate]
- **Weather:** [Expected conditions, pack accordingly]
- **Connectivity:** [WiFi situation, SIM card needs]
- **Cultural notes:** [Business etiquette, dress code, dining customs]

#### Contingency Plan
| Risk | Mitigation |
|------|-----------|
| Flight delay/cancellation | [Alternative flights, airline contact] |
| Meeting reschedule | [Backup agenda, local work options] |
| Lost luggage | [Essentials in carry-on, nearest store] |
| Health issue | [Nearest hospital, insurance info, pharmacy] |

#### Expense Estimate
| Category | Estimated Cost | Notes |
|----------|---------------|-------|
| Flights | $... | [class, booking ref] |
| Hotel | $... | [nightly rate × nights] |
| Ground transport | $... | |
| Meals | $... | [per diem rate] |
| Incidentals | $... | |
| **Total** | **$...** | |

#### Post-Trip
- [ ] Submit expense report within [X] days
- [ ] Send thank-you notes to hosts/contacts
- [ ] File trip summary / meeting outcomes
- [ ] Update CRM / stakeholder notes

## Input

$ARGUMENTS
