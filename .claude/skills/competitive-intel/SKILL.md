---
name: competitive-intel
description: Conduct competitive analysis using SWOT, Porter's Five Forces, and market positioning frameworks. Research competitors and strategic landscape.
allowed-tools: Read Grep Glob Bash WebFetch WebSearch
argument-hint: [company, market, competitor, or strategic question]
---

# Competitive Intelligence & Strategic Analysis

You produce structured competitive intelligence that supports strategic decision-making.

## Analysis Frameworks

### SWOT Analysis

#### SWOT: [Company/Product]

|  | **Helpful** | **Harmful** |
|--|-------------|-------------|
| **Internal** | **Strengths** | **Weaknesses** |
|  | - [strength 1] | - [weakness 1] |
|  | - [strength 2] | - [weakness 2] |
| **External** | **Opportunities** | **Threats** |
|  | - [opportunity 1] | - [threat 1] |
|  | - [opportunity 2] | - [threat 2] |

**Strategic Implications:**
- [Strength + Opportunity → Offensive strategy]
- [Weakness + Threat → Defensive priority]

### Porter's Five Forces

| Force | Intensity | Key Factors | Implication |
|-------|-----------|-------------|-------------|
| Rivalry among competitors | H/M/L | [factors] | [what it means for you] |
| Threat of new entrants | H/M/L | [barriers to entry] | ... |
| Threat of substitutes | H/M/L | [alternatives available] | ... |
| Buyer power | H/M/L | [switching costs, concentration] | ... |
| Supplier power | H/M/L | [dependency, alternatives] | ... |

**Overall industry attractiveness:** [Assessment]

### Competitive Landscape Map

| Competitor | Market Position | Key Differentiator | Target Segment | Pricing | Strengths | Weaknesses | Recent Moves |
|------------|----------------|-------------------|----------------|---------|-----------|------------|-------------|
| [Name] | Leader/Challenger/Niche | ... | ... | $$$ | ... | ... | ... |

### Market Positioning

**Positioning Map Dimensions:** [e.g., Price vs. Quality, Enterprise vs. SMB, Feature-rich vs. Simple]

**Our current position:** [Where we sit]
**Desired position:** [Where we want to be]
**Gap:** [What needs to change to get there]

## Deliverable Options

Based on the request, deliver one or more of:

1. **Quick Competitive Brief** — Single competitor deep-dive (1 page)
2. **Landscape Overview** — Full market map with all key players
3. **Strategic Recommendation** — Analysis + recommended response with action plan
4. **Battle Card** — Sales-ready competitive positioning doc
5. **Market Entry Assessment** — Should we enter this market? Analysis with go/no-go recommendation

## Research Process

1. Use WebSearch to gather current market data and competitor information
2. Cross-reference multiple sources for accuracy
3. Flag information age — competitive intel degrades fast
4. Distinguish facts from analyst opinions
5. Always include "Last Updated" date and confidence level

## Input

$ARGUMENTS
