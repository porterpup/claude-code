# Chief of Staff Skills Research

Research into third-party skill marketplaces and community repositories to identify skills for building the ultimate AI Chief of Staff.

## Sources Investigated

| Source | URL | Description |
|--------|-----|-------------|
| FindSkill.ai | https://findskill.ai | 1,236+ prompt templates/skills, some premium (Pro) |
| ClaudeSkills.info | https://claudeskills.info | Marketplace (currently returning 403; may require direct browsing) |
| antigravity-awesome-skills | https://github.com/sickn33/antigravity-awesome-skills | 1,340+ agentic skills for Claude Code, Cursor, Codex CLI, Gemini CLI |
| awesome-claude-code | https://github.com/hesreallyhim/awesome-claude-code | 36.7k stars; curated skills, hooks, slash-commands, and plugins for Claude Code |

---

## Recommended Skills by Chief of Staff Function

### 1. Meeting Management
| Skill | Source | Description |
|-------|--------|-------------|
| **Meeting Notes & Action Item Extractor** | FindSkill.ai | Transform meeting transcripts into structured summaries with key decisions, action items with owners and deadlines |
| **Meeting Effectiveness Scorer** | FindSkill.ai | Rate meeting productivity across decision velocity, action clarity, time efficiency, and engagement |

### 2. Communications & Email
| Skill | Source | Description |
|-------|--------|-------------|
| **Professional Email Writer** | FindSkill.ai | Templates for business requests, follow-ups, introductions, and difficult conversations |
| **email-sequence** | antigravity-awesome-skills | Create email sequences that nurture relationships and drive action |
| **copywriting** | antigravity-awesome-skills | Conversion-focused marketing copy for landing pages and emails |
| **LinkedIn Post Writer** | FindSkill.ai | Professional content creation with engagement strategies |

### 3. Strategic Planning & Decision Support
| Skill | Source | Description |
|-------|--------|-------------|
| **brainstorming** | antigravity-awesome-skills | Transforms vague ideas into validated designs through disciplined reasoning |
| **competitive-landscape** | antigravity-awesome-skills | Frameworks for analyzing competition and identifying differentiation |
| **Competitive Analysis Framework** | FindSkill.ai | SWOT, Porter's Five Forces, and market positioning frameworks |
| **market-sizing-analysis** | antigravity-awesome-skills | TAM/SAM/SOM calculation methodologies |
| **Cost-Benefit Analysis** | FindSkill.ai (Pro) | NPV, ROI, IRR calculations with sensitivity testing |
| **Pricing Strategy Analyzer** | FindSkill.ai | Optimal pricing strategies with competitor analysis and margin calculations |

### 4. Project & Task Management
| Skill | Source | Description |
|-------|--------|-------------|
| **Claude Code PM** | awesome-claude-code | Comprehensive project-management workflow with specialized agents and slash-commands |
| **Claude Task Master** | awesome-claude-code | Task management system for AI-driven development |
| **Auto-Claude** | awesome-claude-code | Kanban-style UI for task organization across SDLC |
| **workflow-patterns** | antigravity-awesome-skills | TDD workflow with phase checkpoints |
| **product-manager-toolkit** | antigravity-awesome-skills | Essential tools and frameworks for modern product management |

### 5. Reporting & Briefings
| Skill | Source | Description |
|-------|--------|-------------|
| **Data Storytelling** | FindSkill.ai (Pro) | Transform data insights into compelling narratives that drive action |
| **Executive Summary Writer** | FindSkill.ai | Create concise executive summaries |
| **Vibe-Log** | awesome-claude-code | Session analysis with actionable strategic guidance and HTML reports |
| **analyze-project** | antigravity-awesome-skills | Forensic root cause analyzer; classifies scope deltas |

### 6. Document & Knowledge Management
| Skill | Source | Description |
|-------|--------|-------------|
| **docs-architect** | antigravity-awesome-skills | Creates comprehensive documentation from existing codebases |
| **product-marketing-context** | antigravity-awesome-skills | Reusable product marketing context document with positioning and audience |
| **Contract Reviewer** | FindSkill.ai | Analyze contracts for red flags, missing clauses; plain-English explanations |

### 7. People & Stakeholder Management
| Skill | Source | Description |
|-------|--------|-------------|
| **Onboarding Checklist Creator** | FindSkill.ai | Comprehensive employee onboarding plans covering pre-boarding through 90-day milestones |
| **Performance Review Defender** | FindSkill.ai (Pro) | Translate achievements into corporate language aligned with OKRs and KPIs |
| **Promotion Case Builder** | FindSkill.ai (Pro) | Weekly win tracking, impact metrics, and quarterly narratives |
| **Salary Negotiation Coach** | FindSkill.ai | Market data analysis, negotiation scripts, counter-offer strategies |
| **sales-enablement** | antigravity-awesome-skills | Sales collateral: decks, one-pagers, objection docs, demo scripts |

### 8. Business Planning
| Skill | Source | Description |
|-------|--------|-------------|
| **Business Plan Generator** | FindSkill.ai | Executive summary, market analysis, financial projections, operational strategy |
| **Pitch Deck Creator** | FindSkill.ai | Investor pitch decks using Y Combinator and Sequoia frameworks |
| **seo-plan** | antigravity-awesome-skills | Industry-specific templates, competitive analysis, content strategy |
| **brand-guidelines** | antigravity-awesome-skills | Consistent copy following brand guidelines for UI text and communications |

### 9. Operational Dashboards & Metrics
| Skill | Source | Description |
|-------|--------|-------------|
| **Excel Analytics** | FindSkill.ai (Pro) | Advanced Excel for data analysis, pivot tables, and dashboards |
| **ccflare / better-ccflare** | awesome-claude-code | Usage dashboards with comprehensive metrics |
| **Wealth Gap Analyzer** | FindSkill.ai | Income vs. net worth analysis and spending optimization |

---

## Gaps Identified

These Chief of Staff functions had **no strong skill matches** across any marketplace:

| Function | Notes |
|----------|-------|
| **Calendar/Scheduling** | No dedicated calendar management skill found; would need MCP integration with Google Calendar or Outlook |
| **Travel Planning** | No travel coordination skills found |
| **Expense Tracking** | FindSkill.ai mentions the category but no dedicated skill surfaced |
| **Delegation Frameworks** | No explicit delegation/RACI skill; closest is project management tools |
| **Weekly/Monthly Status Reports** | No templated recurring report skill; could be built from Meeting Notes + Data Storytelling |
| **Inbox Triage / Email Prioritization** | Email writing exists but not inbox management |

---

## Installation Notes

- **FindSkill.ai**: Copy skill prompts directly into your skills folder or CLAUDE.md
- **antigravity-awesome-skills**: Install via `npx antigravity-awesome-skills` — selectively pick skills from the catalog
- **awesome-claude-code**: Follow individual project READMEs for installation (varies per tool)
- **ClaudeSkills.info**: Browse and download; Apache 2.0 licensed for official Anthropic skills

---

## Top 10 Priority Skills for Chief of Staff

1. **Meeting Notes & Action Item Extractor** — Core CoS duty
2. **Professional Email Writer** — Daily communication
3. **Claude Code PM** — Project/task tracking
4. **Data Storytelling** — Executive briefings
5. **Competitive Analysis Framework** — Strategic support
6. **email-sequence** — Stakeholder nurturing
7. **Onboarding Checklist Creator** — People operations
8. **Contract Reviewer** — Legal/vendor support
9. **brainstorming** — Strategic ideation
10. **Cost-Benefit Analysis** — Decision support
