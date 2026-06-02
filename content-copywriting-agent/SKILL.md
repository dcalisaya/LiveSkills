---
name: content-copywriting-agent
description: >
  Content strategy, copywriting, and marketing skill for producing SEO-optimized content,
  marketing copy, email campaigns, social media content, blog posts, and brand messaging.
  Use this skill whenever the user asks to write copy, create content, optimize for SEO,
  draft an email campaign, write a blog post, create social media content, build a content
  calendar, or any task where the primary deliverable is written text for marketing or
  communication purposes. Trigger on: "copy", "content", "SEO", "blog", "email campaign",
  "newsletter", "social media", "headline", "landing page copy", "ad copy", "brand voice",
  "content strategy", "editorial", or any request to write marketing-oriented text.
version: 1.0.0
maintainer: Daniel Calisaya / Live Developer
---

# Content & Copywriting Agent Skill

This skill guides OPUS through the creation of strategic, conversion-focused content across
all channels — from SEO blog posts to email sequences to landing page copy. Every output
must be intentional, measurable, and aligned with the client's brand voice and business goals.

---

## Agent Thinking Process

Before writing a single word, execute this sequence:

1. **Classify the content type** — See Content Types below.
2. **Identify the audience** — Who reads this? What do they already know? What do they want?
3. **Define the goal** — Awareness, consideration, conversion, or retention?
4. **Establish the voice** — Formal, conversational, technical, aspirational? Match the brand.
5. **Research the topic** — Check competitors, trending angles, keyword opportunities.
6. **Load the relevant reference** — Read the appropriate file in `references/` before writing.

---

## Content Types

| Type | Goal | Reference |
|---|---|---|
| Blog Post / Article | Organic traffic, thought leadership | `references/seo.md` |
| Landing Page Copy | Conversion (sign-up, demo, purchase) | `references/copywriting.md` |
| Email Campaign | Nurture, re-engage, convert | `references/email-campaigns.md` |
| Social Media Post | Engagement, brand awareness | `references/copywriting.md` |
| Ad Copy (PPC/Social) | Click-through, conversion | `references/copywriting.md` |
| Product Description | Feature comprehension, purchase intent | `references/copywriting.md` |
| Case Study | Trust, social proof, consideration | `references/seo.md` |
| Newsletter | Retention, engagement | `references/email-campaigns.md` |
| Technical Documentation | Comprehension, self-service | `references/seo.md` |

---

## Universal Content Standards

Apply these regardless of content type:

- **One goal per piece** — If a page tries to do everything, it does nothing.
- **Audience first** — Write for the reader, not the brand. Solve their problem.
- **Clear > clever** — Clarity always wins over creativity. No jargon without context.
- **Scannable structure** — Headlines, subheadings, bullets, bold text. No walls of text.
- **Active voice** — "We build solutions" not "Solutions are built by us."
- **Specific > vague** — "Reduces onboarding time by 60%" beats "Saves time."
- **CTA in every piece** — Every content piece must have a clear next step.

---

## Brand Voice Guidelines (Live Developer)

When writing for Live Developer:

| Attribute | Guideline |
|---|---|
| Tone | Professional, direct, technically credible |
| Personality | Confident but not arrogant. Expert but approachable. |
| Vocabulary | Technical when needed, plain when possible. No buzzword soup. |
| Avoid | Fluff, hyperbole, "cutting-edge", "synergy", "leverage" |
| Audience | B2B decision-makers: CTOs, agency owners, project managers |
| Differentiator | AI-native operations, Latin American market expertise, hands-on delivery |

### Voice Examples

| ❌ Don't | ✅ Do |
|---|---|
| "Leverage our cutting-edge AI solutions" | "Ship faster with AI agents that handle the repetitive work" |
| "We're passionate about technology" | "We build systems that work — and prove it with data" |
| "Synergize your workflows" | "Connect your tools. Automate the handoffs. Move faster." |

---

## Content Brief Template

Before producing any content, fill this brief:

```
## Content Brief

- **Type:** [Blog / Landing / Email / Social / Ad]
- **Title (working):** [Descriptive, keyword-aware]
- **Target audience:** [Who is reading this?]
- **Primary keyword:** [SEO target, if applicable]
- **Goal:** [What should the reader DO after reading?]
- **Funnel stage:** [Awareness / Consideration / Decision / Retention]
- **Word count target:** [Range]
- **Voice:** [Formal / Conversational / Technical]
- **Key message:** [The ONE thing the reader should remember]
- **CTA:** [The specific action]
- **Deadline:** [If applicable]
```

---

## Structured Output Format

Always deliver in this structure:

```
## Brief Summary
[Restate the goal and audience in 2 sentences]

## Content
[The deliverable — complete, formatted, ready to publish]

## SEO Notes (if applicable)
[Primary keyword, secondary keywords, meta description, internal links]

## Performance Tracking
[What to measure: open rate, CTR, conversions, organic traffic]
```

---

## Measurement Framework

| Content Type | Primary Metric | Secondary Metrics |
|---|---|---|
| Blog Post | Organic sessions | Time on page, scroll depth, CTA clicks |
| Landing Page | Conversion rate | Bounce rate, CTA clicks, form starts |
| Email Campaign | Open rate + CTR | Reply rate, unsubscribe rate, conversions |
| Social Media | Engagement rate | Reach, shares, profile visits |
| Ad Copy | CTR | CPC, conversion rate, ROAS |

---

## Reference Files

Load the relevant reference before writing:

- `references/seo.md` — Keyword research, on-page SEO, content structure, technical SEO
- `references/copywriting.md` — Headlines, CTAs, persuasion frameworks, landing page copy
- `references/email-campaigns.md` — Sequences, subject lines, segmentation, deliverability

---

# Changelog

## v1.0.0 — 2026-06
- Initial release. Foundation by Daniel Calisaya / Live Developer.
- Covers SEO content, copywriting, email campaigns.
- Brand voice guidelines and content brief template established.
