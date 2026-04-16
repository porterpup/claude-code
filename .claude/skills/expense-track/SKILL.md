---
name: expense-track
description: Track, categorize, and report on expenses. Generate expense reports, budget summaries, and spending analysis.
allowed-tools: Read Grep Glob Bash
argument-hint: [expense data, receipt details, budget, or report request]
---

# Expense Tracking & Reporting

You help track expenses, generate reports, and analyze spending patterns.

## Mode 1: Log Expenses

When given expense data (receipts, descriptions, amounts), organize into a structured log:

### Expense Log — [Period]

| Date | Description | Category | Amount | Currency | Payment Method | Receipt | Reimbursable | Notes |
|------|-------------|----------|--------|----------|---------------|---------|-------------|-------|
| ... | ... | ... | $... | USD | Corp Card / Personal | Y/N | Y/N | ... |

**Categories:** Travel, Meals, Lodging, Transport, Software/Tools, Office Supplies, Client Entertainment, Professional Development, Other

**Running Totals:**
| Category | Total | Budget | Remaining | % Used |
|----------|-------|--------|-----------|--------|
| ... | $... | $... | $... | ...% |
| **Grand Total** | **$...** | **$...** | **$...** | **...%** |

## Mode 2: Expense Report Generation

Generate a submission-ready expense report:

### Expense Report
**Employee:** [Name]
**Department:** [Dept]
**Period:** [Date range]
**Purpose:** [Trip / Project / General]
**Submitted:** [Date]

[Expense table from Mode 1]

**Total Reimbursable:** $...
**Total Non-Reimbursable:** $...
**Grand Total:** $...

**Approver:** _______________
**Date Approved:** _______________

## Mode 3: Spending Analysis

When given historical expense data, analyze:

- **Trends:** Month-over-month spending by category
- **Anomalies:** Unusual spikes or outliers
- **Budget adherence:** Categories over/under budget
- **Optimization opportunities:** Subscriptions to cancel, cheaper alternatives, bulk purchasing
- **Forecast:** Projected spend for remainder of period based on current run rate

## Mode 4: Budget Planning

Help create or review budgets:

| Category | Last Period Actual | Proposed Budget | Change | Justification |
|----------|-------------------|-----------------|--------|---------------|
| ... | $... | $... | +/-% | ... |

## Input

$ARGUMENTS
