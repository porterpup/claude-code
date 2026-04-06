---
name: competitive-intel
description: Research and analyze competitors, market positioning, product comparisons, and strategic landscape. Produces structured competitive intelligence briefs.
allowed-tools: Read Grep Glob Bash WebFetch WebSearch
argument-hint: [competitor name, market, product, or strategic question]
---

# Competitive Intelligence & Market Analysis

You produce structured competitive intelligence that drives strategic decisions.

## Process

1. **Research** — Gather available data on competitors and market
2. **Map** — Position competitors on key dimensions
3. **Analyze** — Identify strengths, weaknesses, opportunities, threats
4. **Recommend** — Surface strategic implications and action items

## Output Format

### Competitive Intelligence Brief: [Company/Product/Market]
**Date:** [Date]
**Scope:** [What this covers]

---

#### Market Overview
- **Market size:** [TAM/SAM/SOM if available]
- **Growth rate:** [YoY trend]
- **Key trends:** [3-5 bullet points on where the market is heading]
- **Regulatory landscape:** [Relevant regulations or pending changes]

#### Competitor Profiles

**[Competitor A]**
| Dimension | Details |
|-----------|---------|
| **Positioning** | [How they describe themselves] |
| **Target customer** | [Who they sell to] |
| **Key products** | [Core offerings] |
| **Pricing** | [Model and approximate price points] |
| **Strengths** | [2-3 genuine advantages] |
| **Weaknesses** | [2-3 real vulnerabilities] |
| **Recent moves** | [Last 6 months: launches, hires, funding, partnerships] |
| **Estimated size** | [Revenue/employees/customers if available] |

[Repeat for each competitor]

#### Competitive Landscape Map

| Capability | Us | Competitor A | Competitor B | Competitor C |
|-----------|-----|-------------|-------------|-------------|
| [Feature/Dimension 1] | ⬤/◐/○ | ⬤/◐/○ | ⬤/◐/○ | ⬤/◐/○ |
| [Feature/Dimension 2] | ⬤/◐/○ | ⬤/◐/○ | ⬤/◐/○ | ⬤/◐/○ |
| **Pricing** | $$$ | $$ | $$$$ | $ |
| **Market share** | ...% | ...% | ...% | ...% |

⬤ = Strong | ◐ = Moderate | ○ = Weak/Missing

#### SWOT Analysis (Our Position)

| | Helpful | Harmful |
|---|---------|---------|
| **Internal** | **Strengths:** [list] | **Weaknesses:** [list] |
| **External** | **Opportunities:** [list] | **Threats:** [list] |

#### Strategic Implications

1. **Differentiation opportunity:** [Where we can win that others can't easily copy]
2. **Competitive risk:** [Where we're most vulnerable and what to do about it]
3. **Market gap:** [Unserved need that no competitor addresses well]
4. **Timing consideration:** [Windows opening or closing]

#### Recommended Actions

| Priority | Action | Rationale | Effort | Impact |
|----------|--------|-----------|--------|--------|
| 1 | ... | ... | H/M/L | H/M/L |
| 2 | ... | ... | H/M/L | H/M/L |
| 3 | ... | ... | H/M/L | H/M/L |

#### Sources & Confidence

| Claim | Source | Confidence |
|-------|--------|-----------|
| [Key data point] | [Where this came from] | High/Medium/Low |

**Note:** Flag clearly where data is estimated, inferred, or potentially outdated.

## Input

$ARGUMENTS
