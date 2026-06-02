# Email Campaigns Reference — Live Developer Stack

## Email Strategy Framework

Before writing any email, answer:

1. **Who receives this?** — Segment, persona, funnel stage.
2. **What's the ONE goal?** — Click, reply, buy, activate, re-engage.
3. **Why should they care?** — What's in it for them RIGHT NOW?
4. **What's the next step?** — One clear CTA. Not two. One.

---

## Email Types & Sequences

### Transactional (Automated, Triggered)

| Email | Trigger | Goal |
|---|---|---|
| Welcome | Sign-up | Activate, set expectations |
| Onboarding (1-3) | Days 1, 3, 7 after sign-up | Feature adoption |
| Password reset | Request | Security |
| Invoice/receipt | Payment | Confirmation |
| Deliverable notification | Status change | Keep client informed |

### Marketing (Campaigns)

| Email | Cadence | Goal |
|---|---|---|
| Newsletter | Weekly/biweekly | Engagement, thought leadership |
| Product update | On release | Feature awareness |
| Case study | Monthly | Social proof, consideration |
| Re-engagement | After 30/60/90 days inactive | Win back |
| Promotional | Seasonal/event | Conversion |

---

## Subject Line Formulas

### Proven Patterns

| Formula | Example | Best For |
|---|---|---|
| **[Number] + [Benefit]** | "3 ways to ship faster this week" | Newsletter |
| **Question** | "Still chasing client approvals?" | Re-engagement |
| **How to [Outcome]** | "How to cut review cycles in half" | Educational |
| **[Name], [personal hook]** | "Daniel, your Q2 results are in" | Personalized |
| **[Urgency] + [Benefit]** | "Last day: 40% off annual plans" | Promotional |
| **Curiosity gap** | "We analyzed 500 agency workflows. Here's what we found." | Content |
| **Social proof** | "Why 120+ agencies switched to LiveApp" | Consideration |

### Subject Line Rules

- **Under 50 characters** — mobile truncates at ~40.
- **No ALL CAPS or excessive punctuation** — triggers spam filters.
- **Preview text matters** — the 80-100 chars after the subject. Don't waste them.
- **Personalization works** — first name in subject increases open rates ~20%.
- **A/B test every campaign** — always test 2 subject lines.

---

## Email Copy Structure

### Short Email (CTA-Focused)

```
Subject: [Short, benefit-driven hook]
Preview: [Extends the subject, adds context]

Hi [Name],

[One paragraph — state the value or news. 2-3 sentences max.]

[One paragraph — why it matters to THEM. Be specific.]

[CTA Button: Action Verb + Outcome]

Cheers,
[Sender Name]
[Title], Live Developer
```

### Narrative Email (Story-Driven)

```
Subject: [Curiosity hook]
Preview: [Sets up the story]

Hi [Name],

[Opening hook — a problem, a surprising fact, or a micro-story. 2 sentences.]

[Build tension — what went wrong, what was at stake.]

[The turn — how the solution changed things.]

[Connect to the reader — "You might be facing the same thing."]

[CTA: single, clear next step]

— [Sender]
```

---

## Welcome Sequence (3-Email Onboarding)

### Email 1: Welcome (Immediate)

```
Subject: Welcome to LiveApp — here's your first step
Preview: Set up takes 2 minutes. Let's go.

Hi [Name],

Thanks for signing up for LiveApp. You're about to save hours on
deliverable management — here's how to get started:

1. Create your first project
2. Add your team (or go solo)
3. Upload your first deliverable

[CTA: Create Your First Project]

If you have questions, just reply to this email. A human reads it.

— Daniel Calisaya, Live Developer
```

### Email 2: Value Demonstration (Day 2)

```
Subject: How GIZ Ecuador cut review cycles by 70%
Preview: From 9 days to 2.5 days. Here's how.

Hi [Name],

Before LiveApp, GIZ Ecuador managed deliverables over email.
Reviews took 9 days on average. Deadlines slipped constantly.

After switching to LiveApp, review cycles dropped to 2.5 days.
Client satisfaction scores went from 7.1 to 9.3.

The difference? Automated review workflows and a client portal
that replaced 47 email threads per project.

[CTA: See How It Works]

— Daniel
```

### Email 3: Activation Push (Day 5)

```
Subject: [Name], did you finish setting up?
Preview: Need help? Here are your options.

Hi [Name],

I noticed you signed up but haven't created a project yet.
No worries — here are three ways to get started:

• Watch a 3-minute walkthrough [link]
• Book a 15-minute setup call [link]
• Reply to this email and tell me what you're working on

[CTA: Watch the Walkthrough]

— Daniel
```

---

## Segmentation Strategy

### Segments to Build

| Segment | Criteria | Use For |
|---|---|---|
| New sign-ups (0-7 days) | Created < 7 days ago | Onboarding sequence |
| Active users | Logged in last 14 days | Product updates, tips |
| At-risk | No login in 14-30 days | Re-engagement |
| Churned | No login in 60+ days | Win-back campaign |
| Paying customers | Active subscription | Upsell, referral, case study |
| Free tier | No subscription | Conversion campaigns |

### Personalization Variables

```
{{first_name}}        — "Daniel"
{{company_name}}      — "Live Developer"
{{plan_name}}         — "Pro"
{{projects_count}}    — "12"
{{days_since_signup}} — "14"
{{last_login_date}}   — "May 28, 2026"
```

---

## Deliverability Checklist

```
□ Sending domain authenticated (SPF, DKIM, DMARC)
□ Warm up new sending domains (start low, increase gradually)
□ Unsubscribe link in every email (required by CAN-SPAM)
□ Physical mailing address in footer (required by CAN-SPAM)
□ Clean list quarterly (remove bounces, inactive > 6 months)
□ Double opt-in for new subscribers
□ Monitor bounce rate (keep < 2%)
□ Monitor spam complaint rate (keep < 0.1%)
□ Test emails in Litmus or Email on Acid before sending
□ Send from a real person name, not "noreply@"
```

### DNS Records for Email Authentication

```
# SPF
TXT  @  "v=spf1 include:_spf.google.com include:sendgrid.net ~all"

# DKIM (provided by email service)
CNAME  s1._domainkey  s1.domainkey.u12345.wl.sendgrid.net

# DMARC
TXT  _dmarc  "v=DMARC1; p=quarantine; rua=mailto:dmarc@livedeveloper.com; pct=100"
```

---

## Metrics & Benchmarks

| Metric | B2B SaaS Benchmark | Target |
|---|---|---|
| Open rate | 20-25% | > 25% |
| Click-through rate (CTR) | 2-4% | > 4% |
| Click-to-open rate (CTOR) | 10-15% | > 15% |
| Unsubscribe rate | < 0.5% | < 0.3% |
| Bounce rate | < 2% | < 1% |
| Reply rate (cold) | 5-10% | > 8% |

### What to Test

| Element | Test Method |
|---|---|
| Subject line | A/B test (50/50 split) |
| Send time | Test 3 different times, measure opens |
| CTA button vs text link | A/B test |
| Short vs long copy | A/B test |
| Personalization | With name vs without |
| Sender name | Person name vs company name |
