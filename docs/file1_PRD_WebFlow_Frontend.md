# 🚀 RevAI — Product Requirements, Website Flow & Frontend Guidelines
### ETH India Hackathon

---

# PART 1 — PRODUCT REQUIREMENTS DOCUMENT (PRD)

## 1.1 Product Overview

| Field | Detail |
|---|---|
| **Product Name** | RevAI |
| **Tagline** | "Close More. Lose Less. Automatically." |
| **Type** | AI-native Sales & Revenue Operations Platform |
| **Target Users** | B2B Sales Teams, Revenue Ops Leaders, Account Executives, SDRs |

---

## 1.2 Problem Statement

Sales teams lose deals not from lack of data — but from inability to act on signals at the right time:

- SDRs spend **60–70% of their time** on research and writing cold outreach
- AEs don't know a deal is at risk until the prospect goes dark
- Customer success teams discover churn signals **weeks after** the intervention window
- Competitive intel lives in docs no one reads at the right moment

**RevAI** embeds AI agents directly into the CRM and communication stack to act on these signals automatically — in real-time, at scale.

---

## 1.3 Core Agent Modules

### 🔍 Agent 1 — Prospecting Intelligence Agent
**Goal:** Research, score, and generate personalized outreach sequences autonomously.

**Inputs:**
- Ideal Customer Profile (ICP) definition
- Target company domains / LinkedIn URLs
- CRM data (existing customers for lookalike modeling)

**Outputs:**
- Scored prospect list with fit signals
- Personalized multi-touch email sequences (3–5 steps)
- Engagement-based sequence adjustments (if opened but not replied → adjust tone/CTA)

**Key Behaviors:**
- Scrapes public data: LinkedIn, news, job postings, funding rounds, product reviews
- Scores prospects on ICP fit (0–100)
- Writes outreach referencing real prospect triggers ("Saw you just raised Series B...")
- Monitors reply/open rates → regenerates sequences automatically

---

### 🧠 Agent 2 — Deal Intelligence Agent
**Goal:** Monitor pipeline health, detect risks, and suggest recovery plays.

**Inputs:**
- CRM deal stages, close dates, deal values
- Email/calendar engagement data
- Call transcripts (if integrated)

**Outputs:**
- Deal health score (0–100) with color-coded risk flags
- Risk signals: engagement drop, competitor mention, stakeholder change, silence > N days
- Recovery play: specific talking points, next action suggestion, auto-draft email

**Key Behaviors:**
- Monitors email thread velocity (days since last interaction)
- Detects competitor names in email threads
- Identifies decision-maker changes using LinkedIn signals
- Generates "rescue email" drafts on risk trigger

---

### 📉 Agent 3 — Revenue Retention Agent
**Goal:** Predict churn from usage + sentiment, trigger intervention workflows.

**Inputs:**
- Product usage data (API events, feature adoption, login frequency)
- Customer support tickets (sentiment)
- NPS scores / survey responses
- Contract renewal dates

**Outputs:**
- Churn probability score per account (0–100%)
- Churn reason classification (usage drop / support frustration / budget signal)
- Intervention playbook: which team should act, when, with what message
- Auto-generated outreach or escalation email

**Key Behaviors:**
- Segments accounts into risk tiers (Red / Yellow / Green)
- Triggers auto-outreach for yellow accounts
- Escalates red accounts to human CSM with briefing note
- Tracks intervention outcomes to improve future predictions

---

### ⚔️ Agent 4 — Competitive Intelligence Agent
**Goal:** Track market signals, push relevant battlecards into active deals.

**Inputs:**
- Competitor website changes (monitored via diff)
- G2/Capterra reviews
- Twitter/LinkedIn mentions
- Active deal context from CRM

**Outputs:**
- Updated battlecard per competitor (auto-refreshed weekly)
- Real-time alert when competitor mentioned in active deal
- Context-specific positioning blurb injected into deal notes

**Key Behaviors:**
- Web crawls competitor sites weekly for pricing/feature changes
- Analyzes review sentiments for competitor weaknesses
- Pushes relevant battlecard section into CRM deal view when competitor detected

---

## 1.4 Key Demo Metrics

| Metric | Target |
|---|---|
| Outreach personalization speed | 10x faster than manual |
| Deal risk detection lead time | 7+ days earlier |
| Pipeline conversion rate | Simulated +15–25% |
| Churn prediction accuracy | >75% on simulated dataset |
| Sequence open rate (simulated) | >40% (vs industry avg 20%) |

---

## 1.5 Integrations

| System | Integration Type |
|---|---|
| HubSpot / Salesforce CRM | OAuth + REST API |
| Gmail / Outlook | Gmail MCP / OAuth |
| Google Calendar | Calendar MCP |
| LinkedIn | Proxycurl API / scraping |
| Slack | Webhook notifications |
| Apollo.io / Hunter.io | Prospect data enrichment |
| Anthropic Claude | LLM backbone |
| Serper API | Web search for research |

---

## 1.6 Tech Stack Summary

### Frontend
| Layer | Technology |
|---|---|
| Framework | Next.js 14 (App Router) |
| Styling | Tailwind CSS + shadcn/ui |
| State | Zustand |
| Charts | Recharts |
| Animations | Framer Motion |
| Icons | Lucide React |

### Backend
| Layer | Technology |
|---|---|
| API Server | FastAPI (Python) |
| Agent Orchestration | LangGraph |
| LLM | Anthropic Claude 3.5 Sonnet |
| Task Queue | Celery + Redis |
| Scheduler | APScheduler |

### Data & Storage
| Layer | Technology |
|---|---|
| Primary DB | PostgreSQL |
| Vector Store | Pinecone / Chroma |
| Cache | Redis |
| File Storage | Supabase Storage |

### DevOps / Demo
| Tool | Purpose |
|---|---|
| Docker Compose | Local multi-service setup |
| Vercel | Frontend deployment |
| Railway / Render | Backend deployment |
| ngrok | Webhook tunneling for demo |

---

# PART 2 — WEBSITE FLOW

## 2.1 Full Page Architecture

```
/ (Landing Page — public)
  ├── /auth/login
  ├── /auth/signup
  └── /dashboard  ← (protected, requires auth)
        │
        ├── /dashboard/overview
        │     └── Pipeline health summary, active alerts, agent activity feed
        │
        ├── /dashboard/prospects          ← Prospecting Agent
        │     ├── /prospects/research     ← Run research on target companies
        │     ├── /prospects/sequences    ← View / edit outreach sequences
        │     └── /prospects/engagement  ← Track email open/reply rates
        │
        ├── /dashboard/deals              ← Deal Intelligence Agent
        │     ├── /deals/pipeline         ← Kanban board + risk heat map
        │     ├── /deals/[id]             ← Deal detail + AI signals + recovery play
        │     └── /deals/recovery         ← Recovery plays queue
        │
        ├── /dashboard/retention          ← Revenue Retention Agent
        │     ├── /retention/accounts     ← Churn score per account
        │     ├── /retention/alerts       ← Triggered interventions log
        │     └── /retention/playbooks    ← Intervention templates
        │
        ├── /dashboard/competitive        ← Competitive Intel Agent
        │     ├── /competitive/battlecards ← Per-competitor cards
        │     └── /competitive/alerts     ← Active deal signal alerts
        │
        ├── /dashboard/integrations       ← Connect CRM, Gmail, Slack
        └── /dashboard/settings           ← ICP config, scoring thresholds
```

---

## 2.2 User Journey Flows

### Flow 1 — New User Onboarding
```
Sign Up
  → Connect CRM (HubSpot OAuth button)
  → Connect Gmail (OAuth)
  → Define ICP (company size, industry, buyer role form)
  → Run first prospect research (enter 1 company to test)
  → View scored prospect card
  → Approve outreach sequence
  → Done — redirected to dashboard/overview
```

### Flow 2 — Daily AE (Account Executive) Workflow
```
Login → Dashboard Overview
  → Alert banner: "⚠️ Acme Corp went dark (12 days, deal worth $45k)"
  → Click alert → Deal detail page opens
  → AI panel shows: risk signals (silence + competitor mention)
  → Click "Generate Recovery Play"
  → AI streams: diagnosis + email draft + call talking points
  → AE edits email → clicks "Send via Gmail"
  → Deal health score updates
```

### Flow 3 — CS Manager Churn Review
```
Login → Retention Dashboard
  → Filter: Red accounts (churn score > 70)
  → Click account → Detail slide-over opens
  → See: usage drop chart + support ticket sentiment + churn score breakdown
  → Recommended intervention card: "Schedule executive sponsor call"
  → Click "Execute Intervention"
  → Agent drafts outreach email
  → CSM edits + sends → intervention_status = "triggered"
```

### Flow 4 — SDR Prospecting Run
```
Login → Prospects → Research Tab
  → Fill form: company name, domain, contact name, contact email
  → Click "Run Research"
  → Agent runs (progress indicator visible): Research → Enrich → Score → Write Sequence
  → Prospect card appears: ICP Score 82/100 with fit signals
  → Click prospect → Right drawer opens
  → Review 3-step email sequence
  → Click "Approve Sequence" → status becomes "approved"
  → Sequence enters send queue
```

### Flow 5 — Competitive Alert in Active Deal
```
Competitive agent runs (background, scheduled)
  → Detects "CompetitorX" mentioned in email thread on deal "FinTrack Ltd"
  → Creates competitive_alert linked to deal
  → Slack notification sent to AE: "⚔️ Competitor mentioned in FinTrack deal"
  → AE opens deal → Competitive Intel panel appears
  → Shows relevant battlecard section + "How We Win" talking points
  → AE uses talking points in next call
```

---

## 2.3 Navigation Structure

### Left Sidebar (240px expanded / 64px collapsed)
```
[RevAI Logo]

MAIN
  🏠 Overview
  👥 Prospects
  📊 Deals
  📉 Retention
  ⚔️  Competitive

SETTINGS
  🔌 Integrations
  ⚙️  Settings

[User Avatar + Name]
[Collapse Arrow]
```

### Top Bar (persistent)
```
[Global Search Bar]        [🔔 Notifications]  [🤖 Agent Status]  [Avatar]
                                                   ↑
                           Shows: agents running / idle / error
```

### Agent Status Indicator (top right)
- 🟢 Green dot = all agents running normally
- 🟡 Amber dot = 1+ agent running a task
- 🔴 Red dot = agent error, needs attention

---

# PART 3 — FRONTEND GUIDELINES

## 3.1 Aesthetic Direction

**Theme: "Mission Control"**

Dark, data-dense, precision-oriented. Think: Bloomberg Terminal meets Linear.app. Power-user energy. This is where deals get saved.

**Mood:** Confident, surgical, high-stakes.  
**One thing users remember:** The glowing red deal cards that scream "act now."

---

## 3.2 Color System

```css
:root {
  /* Backgrounds */
  --bg-base:      #0A0B0F;   /* near-black — main background */
  --bg-surface:   #111318;   /* card / panel surfaces */
  --bg-elevated:  #1A1D26;   /* hover states, nested panels */
  --border:       #232630;   /* subtle borders */
  --border-hover: #363B4D;   /* hover border */

  /* Accent Colors */
  --accent-primary:  #00E5FF;  /* electric cyan — primary actions, links */
  --accent-success:  #00C853;  /* green — healthy deals, positive signals */
  --accent-warning:  #FFB300;  /* amber — risk signals, warnings */
  --accent-danger:   #FF1744;  /* red — critical alerts, churn risk */
  --accent-purple:   #7C3AED;  /* purple — AI-generated content */
  --accent-blue:     #2979FF;  /* blue — informational */

  /* Text */
  --text-primary:   #F0F2F8;
  --text-secondary: #8B92A8;
  --text-muted:     #4A5168;

  /* Health Score Colors */
  --health-green:   #00C853;
  --health-amber:   #FFB300;
  --health-red:     #FF1744;
}
```

### Color Usage Rules
- **Cyan** (`--accent-primary`): CTA buttons, active nav items, links, progress indicators
- **Green** (`--accent-success`): Healthy deal cards (left border), positive metrics, "Approved" status
- **Amber** (`--accent-warning`): Risk signals, yellow accounts, "At Risk" badges
- **Red** (`--accent-danger`): Critical alerts, churn > 70, silent deals > 10 days
- **Purple** (`--accent-purple`): AI-generated content labels, agent action badges
- Never use pure white (#FFFFFF) — always use `--text-primary`

---

## 3.3 Typography

```css
/* Display / Headings — monospace for the "terminal intelligence" feel */
font-family: 'Space Mono', 'JetBrains Mono', monospace;

/* Body / Labels / UI text */
font-family: 'DM Sans', 'Geist', sans-serif;

/* Data / Numbers / Scores */
font-family: 'Berkeley Mono', 'Fira Code', monospace;
```

### Type Scale
```
H1 (page title):    28px / Space Mono / font-weight: 700
H2 (section title): 20px / Space Mono / font-weight: 600
H3 (card title):    16px / DM Sans   / font-weight: 600
Body:               14px / DM Sans   / font-weight: 400
Caption / Label:    12px / DM Sans   / font-weight: 500
Data / Number:      20px / Space Mono / font-weight: 700
Small data:         13px / Fira Code  / font-weight: 400
```

**Import in layout.tsx:**
```html
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet" />
```

---

## 3.4 Component Design Patterns

### Deal Card (Kanban)
```
┌─ [GREEN/AMBER/RED left border 3px] ────────────────┐
│  Acme Corp                         $45,000          │
│  Sarah Chen · Enterprise           ●  82            │
│  Stage: Proposal · 3d ago          [AE initials]    │
└────────────────────────────────────────────────────┘
```
- Left border color = health status (green/amber/red)
- Health score badge top-right: colored number
- Days since contact shown in muted text
- Hover state: border brightens, slight elevation (box-shadow)
- Red-tinted background (`rgba(255,23,68,0.05)`) for at-risk cards

### Prospect Row (Table)
- ICP Score badge: pill shape, green > 70 / amber 40–70 / red < 40
- Fit signals: small chips in muted color, max 3 shown + "+N more"
- Status chip: "Researching" (cyan) / "Qualified" (green) / "Sequence Sent" (blue) / "Low Fit" (muted)
- Row hover: subtle background lift

### AI Action Panel (Right Drawer, 420px)
```
┌─ AI RECOVERY PLAY ──────── [⚙️] [✕] ┐
│                                       │
│  DIAGNOSIS                            │
│  Deal went silent after pricing call  │
│                                       │
│  SIGNALS DETECTED                     │
│  [⚠ 12 days silence] [⚔ CompetitorX] │
│                                       │
│  RECOMMENDED ACTION                   │
│  Send re-engagement email...          │
│                                       │
│  EMAIL DRAFT              [✏️ Edit]   │
│  Subject: Quick thought...            │
│  Body: Hi Sarah, wanted to share...   │
│                                       │
│  [📨 Send via Gmail]  [📋 Copy]       │
└───────────────────────────────────────┘
```
- Slides in from right, overlays main content (not push layout)
- AI text streams character-by-character (typing effect)
- Purple left accent strip to indicate AI content
- "Signals detected" chips at top with severity icons

### Agent Activity Feed
```
[🔍] 14:23  Researching FinTrack Ltd...              prospecting
[⚠️] 14:19  Risk detected: Acme Corp (silence)       deal-intel
[⚔️] 14:15  CompetitorX mention found in TechStart   competitive
[📉] 14:10  Churn score updated: CloudOps → 78%      retention
```
- Monospace font for timestamps
- Icon + color coded by agent type
- Smooth append animation (no layout jump)
- Scrollable, max 50 entries visible

### Health Score Gauge (Arc)
- SVG arc gauge, 0–100
- Color transitions: green (60–100) → amber (30–60) → red (0–30)
- Large number in center (Space Mono, 32px)
- Label below: "Deal Health"

### Churn Score Pill
```
[██████░░░░]  73%  HIGH RISK
```
- Filled bar with color gradient
- Percentage in monospace
- Risk label: HIGH / MEDIUM / LOW in uppercase

---

## 3.5 Animation Rules

### Page Transitions
```css
/* Cards entrance — staggered upward fade-in */
animation: fadeUp 0.3s ease forwards;
animation-delay: calc(var(--index) * 0.05s);

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### Micro-interactions
- **Card hover**: `box-shadow: 0 0 0 1px var(--border-hover), 0 4px 20px rgba(0,229,255,0.05);` + `transform: translateY(-1px)`
- **Button press**: `transform: scale(0.97)` for 100ms
- **Alert badge pulse**: CSS `@keyframes pulse` on red dot for critical alerts
- **Score changes**: Animated number roll using `CountUp` library or CSS counter

### AI Streaming Text
```javascript
// Typewriter effect for AI-generated content
const typeWriter = (text, element, speed = 12) => {
  let i = 0;
  const timer = setInterval(() => {
    element.textContent += text[i++];
    if (i === text.length) clearInterval(timer);
  }, speed);
};
```

### Loading States
- Use **skeleton screens only** — never spinners for content areas
- Skeleton: `bg-[#1A1D26]` with animated shimmer gradient
- For agent "thinking": animated 3-dot pulse in cyan

### Drawer / Modal
- Slide-in from right: `transform: translateX(100%) → translateX(0)`, duration 200ms, ease-out
- Backdrop: `rgba(0,0,0,0.6)` fade-in

---

## 3.6 Layout Principles

### Desktop (> 1280px)
- Left sidebar: 240px (collapsible to 64px)
- Main content: `calc(100vw - 240px)`
- 3-panel layout on detail views: List (320px) | Detail (flex-grow) | AI Panel (420px)
- Top bar: 56px height, sticky

### Tablet (768px–1280px)
- Sidebar collapses to icon-only (64px)
- 2-panel max: List | Detail (AI panel becomes bottom sheet)

### Mobile (< 768px)
- Bottom tab navigation (5 tabs: Overview, Prospects, Deals, Retention, Competitive)
- Single column layout
- AI panel = full-screen modal
- Floating "+" action button for quick prospect research

---

## 3.7 Spacing & Border Radius

```css
/* Spacing scale (use these values only) */
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;

/* Border radius */
--radius-sm: 4px;   /* chips, badges */
--radius-md: 8px;   /* cards, inputs */
--radius-lg: 12px;  /* panels, modals */
--radius-xl: 16px;  /* drawers */
```

---

## 3.8 Tailwind Config Extensions

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        base: '#0A0B0F',
        surface: '#111318',
        elevated: '#1A1D26',
        border: '#232630',
        cyan: { DEFAULT: '#00E5FF', dark: '#00B2CC' },
        success: '#00C853',
        warning: '#FFB300',
        danger: '#FF1744',
        purple: '#7C3AED',
      },
      fontFamily: {
        mono: ['Space Mono', 'JetBrains Mono', 'monospace'],
        sans: ['DM Sans', 'Geist', 'sans-serif'],
        data: ['Fira Code', 'Berkeley Mono', 'monospace'],
      },
    },
  },
};
```

---

## 3.9 Critical Don'ts
- ❌ No pure white backgrounds anywhere
- ❌ No purple gradients on white (generic AI aesthetic)
- ❌ No Inter or Roboto fonts
- ❌ No spinner loading states (use skeletons)
- ❌ No cards without visual health/status signal
- ❌ No modals that push layout — use overlaying drawers
- ❌ No more than 3 accent colors visible on any single screen

---

*RevAI | File 1 of 4 — PRD, Website Flow & Frontend Guidelines*
*ETH India Hackathon*
