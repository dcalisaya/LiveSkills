# Landing Pages Reference — Live Developer Stack

## Purpose & Conversion Logic

A landing page has ONE primary goal. Before building, identify:
- **The offer** — What is being promoted? (product, service, demo, download)
- **The audience** — Who lands here and what do they already know?
- **The CTA** — What is the ONE action this page drives?
- **The objection** — What is the #1 reason someone would NOT convert?

Structure the page to answer the objection before asking for the action.

---

## Standard Section Architecture

```
[1] Hero              — Hook + CTA above the fold
[2] Social Proof      — Logos, numbers, trust signals (optional, above fold on high-traffic)
[3] Problem           — Articulate the pain. Make them feel understood.
[4] Solution          — Introduce the product/service as the answer.
[5] Features/Benefits — 3–6 key capabilities. Lead with benefit, follow with feature.
[6] How It Works      — Optional 3-step process block for complex offerings.
[7] Testimonials      — Real quotes with names, roles, companies.
[8] FAQ               — Address the 5 most common objections.
[9] Final CTA         — Repeat the primary CTA. Create urgency if appropriate.
[10] Footer           — Links, legal, contact.
```

---

## Hero Section Patterns

### Pattern A: Statement + Subtext + CTA
Best for: B2B SaaS, professional services.

```html
<section class="hero">
  <div class="hero__eyebrow">For Marketing Agencies</div>
  <h1 class="hero__headline">Automate Your Client Deliverables With AI</h1>
  <p class="hero__subtext">
    LiveApp orchestrates your production workflow — from brief to delivery —
    so your team ships faster and your clients stay informed.
  </p>
  <div class="hero__actions">
    <a href="#demo" class="btn btn--primary">See It In Action</a>
    <a href="#features" class="btn btn--ghost">Learn More</a>
  </div>
</section>
```

### Pattern B: Bold Headline + Metric + CTA
Best for: high-confidence products with strong numbers.

```html
<h1>Ship Deliverables <span class="accent">3× Faster</span></h1>
<p class="hero__metric">Join 120+ agencies already on LiveApp</p>
```

### Pattern C: Problem-First
Best for: audiences that are pain-aware but solution-unaware.

```html
<h1>Tired of Losing Hours to Project Status Updates?</h1>
<p>Most agencies waste 8+ hours/week on manual check-ins. There's a better way.</p>
```

---

## CSS Architecture (cPanel Vanilla)

```css
/* 
 * Design token foundation
 * NOTE: These are a subset of the full token set in design-system.md.
 * For the canonical source of truth, see: frontend-ui-agent/references/design-system.md
 */
:root {
  /* Colors — aligned with design-system.md */
  --bg-base:            #0d0d0d;
  --bg-surface:         #161616;
  --bg-surface-2:       #1e1e1e;
  --accent:             #e8ff00;         /* Live Developer electric yellow */
  --accent-muted:       #b8cc00;
  --text-primary:       #f0f0f0;
  --text-secondary:     #8a8a8a;
  --border-default:     #2a2a2a;

  /* Typography */
  --font-display: 'Syne', sans-serif;     /* headings */
  --font-body: 'DM Sans', sans-serif;     /* body text */
  --font-mono: 'JetBrains Mono', monospace;

  /* Type scale */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;
  --text-5xl: 3rem;
  --text-6xl: 3.75rem;

  /* Spacing (8px grid) */
  --space-1: 0.5rem;   /* 8px */
  --space-2: 1rem;     /* 16px */
  --space-3: 1.5rem;   /* 24px */
  --space-4: 2rem;     /* 32px */
  --space-6: 3rem;     /* 48px */
  --space-8: 4rem;     /* 64px */
  --space-12: 6rem;    /* 96px */
  --space-16: 8rem;    /* 128px */

  /* Layout */
  --max-width: 1200px;
  --gutter: var(--space-4);
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-full: 9999px;

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
  --transition-slow: 400ms ease;
}
```

---

## Feature Block Patterns

### 3-column icon grid (most common)

```html
<section class="features">
  <div class="features__grid">
    <div class="feature-card">
      <div class="feature-card__icon"><!-- SVG --></div>
      <h3 class="feature-card__title">Automated Review Cycles</h3>
      <p class="feature-card__desc">Clients approve deliverables directly in the portal — no more email chains.</p>
    </div>
    <!-- repeat × 3 -->
  </div>
</section>
```

### Split layout (image + copy)

```html
<section class="split-feature">
  <div class="split-feature__media"><!-- screenshot or illustration --></div>
  <div class="split-feature__copy">
    <span class="label">Real-time Collaboration</span>
    <h2>Everyone on the same page, always.</h2>
    <p>...</p>
    <a href="#" class="btn btn--primary">See How</a>
  </div>
</section>
```

---

## Animation Patterns (CSS-only, no JS required)

```css
/* Entrance animation — staggered children */
.hero > * {
  opacity: 0;
  transform: translateY(24px);
  animation: fadeUp var(--transition-slow) forwards;
}
.hero > *:nth-child(1) { animation-delay: 0ms; }
.hero > *:nth-child(2) { animation-delay: 100ms; }
.hero > *:nth-child(3) { animation-delay: 200ms; }
.hero > *:nth-child(4) { animation-delay: 300ms; }

@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

/* Hover lift on cards */
.feature-card {
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}
.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.4);
}
```

---

## Google Fonts Loading (Performance)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet">
```

---

## CTA Best Practices

- Primary CTA: max 4 words. Action verb + outcome. ("Start Free Trial", "Book a Demo", "See It Live")
- Ghost/secondary CTA: softer ask. ("Learn More", "See Pricing", "Watch the Video")
- Never two primary CTAs competing side by side with the same visual weight.
- CTA color: accent color only. No other UI element should use the exact same color.
- Above-the-fold CTA must be visible without scrolling on 1280px viewport.
