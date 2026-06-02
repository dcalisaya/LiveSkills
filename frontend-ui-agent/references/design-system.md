# Design System Reference — Live Developer Stack

## Philosophy

A design system is a set of constraints that make good decisions automatic.
Its purpose: eliminate inconsistency, accelerate implementation, enforce quality.

This reference defines the foundational tokens and component primitives used across
all Live Developer client and internal products.

---

## Design Tokens

### Color Palettes

#### Dark Theme (Default — all internal products + modern client sites)

```css
:root[data-theme="dark"] {
  --bg-base:          #0a0a0a;
  --bg-surface:       #111111;
  --bg-surface-2:     #181818;
  --bg-surface-3:     #222222;
  --bg-overlay:       rgba(0, 0, 0, 0.72);

  --border-subtle:    #1e1e1e;
  --border-default:   #2a2a2a;
  --border-strong:    #404040;

  --text-primary:     #f5f5f5;
  --text-secondary:   #a0a0a0;
  --text-tertiary:    #606060;
  --text-disabled:    #3a3a3a;

  --accent:           #e8ff00;     /* Live Developer signature */
  --accent-muted:     #b8cc00;
  --accent-subtle:    rgba(232, 255, 0, 0.08);

  --status-success:   #4ade80;
  --status-warning:   #fbbf24;
  --status-error:     #f87171;
  --status-info:      #60a5fa;
}
```

#### Light Theme (Client sites, documents, print-adjacent)

```css
:root[data-theme="light"] {
  --bg-base:          #ffffff;
  --bg-surface:       #f8f8f8;
  --bg-surface-2:     #f0f0f0;
  --bg-surface-3:     #e8e8e8;

  --border-subtle:    #ebebeb;
  --border-default:   #e0e0e0;
  --border-strong:    #c8c8c8;

  --text-primary:     #111111;
  --text-secondary:   #555555;
  --text-tertiary:    #909090;

  --accent:           #1a1a1a;
  --accent-muted:     #333333;
  --accent-subtle:    rgba(0, 0, 0, 0.06);
}
```

---

## Typography System

```css
/* Font loading — include in <head> */
/*
  Display/Headings: Syne (clean, geometric, modern technical feel)
  Body: DM Sans (readable, neutral, professional)
  Code/Data: JetBrains Mono (technical credibility)
*/

:root {
  --font-display: 'Syne', sans-serif;
  --font-body: 'DM Sans', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Scale — 1.25 Major Third ratio */
  --text-2xs:  0.64rem;   /* 10px */
  --text-xs:   0.75rem;   /* 12px */
  --text-sm:   0.875rem;  /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg:   1.125rem;  /* 18px */
  --text-xl:   1.25rem;   /* 20px */
  --text-2xl:  1.5rem;    /* 24px */
  --text-3xl:  1.875rem;  /* 30px */
  --text-4xl:  2.25rem;   /* 36px */
  --text-5xl:  3rem;      /* 48px */
  --text-6xl:  3.75rem;   /* 60px */
  --text-7xl:  4.5rem;    /* 72px */

  /* Leading (line-height) */
  --leading-none:   1;
  --leading-tight:  1.25;
  --leading-snug:   1.375;
  --leading-normal: 1.5;
  --leading-relaxed:1.625;

  /* Tracking (letter-spacing) */
  --tracking-tight: -0.025em;
  --tracking-normal: 0em;
  --tracking-wide:   0.025em;
  --tracking-wider:  0.05em;
  --tracking-widest: 0.1em;
}
```

### Type Roles

```css
.heading-display {
  font-family: var(--font-display);
  font-size: var(--text-6xl);
  font-weight: 800;
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
  color: var(--text-primary);
}
.heading-1 {
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: 700;
  line-height: var(--leading-tight);
}
.heading-2 {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 600;
  line-height: var(--leading-snug);
}
.heading-3 {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 600;
}
.label {
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: var(--tracking-widest);
  color: var(--text-secondary);
}
.body-lg {
  font-family: var(--font-body);
  font-size: var(--text-lg);
  line-height: var(--leading-relaxed);
  color: var(--text-secondary);
}
.body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
}
```

---

## Spacing Scale (8px Grid)

```css
:root {
  --space-px:  1px;
  --space-0-5: 0.25rem;  /* 4px */
  --space-1:   0.5rem;   /* 8px */
  --space-1-5: 0.75rem;  /* 12px */
  --space-2:   1rem;     /* 16px */
  --space-3:   1.5rem;   /* 24px */
  --space-4:   2rem;     /* 32px */
  --space-5:   2.5rem;   /* 40px */
  --space-6:   3rem;     /* 48px */
  --space-8:   4rem;     /* 64px */
  --space-10:  5rem;     /* 80px */
  --space-12:  6rem;     /* 96px */
  --space-16:  8rem;     /* 128px */
  --space-20:  10rem;    /* 160px */
  --space-24:  12rem;    /* 192px */
}
```

---

## Component Primitives

### Buttons

```css
/* Base */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-1);
  padding: 10px var(--space-3);
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: 600;
  line-height: 1;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all var(--transition-fast);
  text-decoration: none;
  white-space: nowrap;
}
.btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* Variants */
.btn--primary {
  background: var(--accent);
  color: #000;
  border-color: var(--accent);
}
.btn--primary:hover { background: var(--accent-muted); border-color: var(--accent-muted); }

.btn--secondary {
  background: var(--bg-surface-3);
  color: var(--text-primary);
  border-color: var(--border-default);
}
.btn--secondary:hover { background: var(--bg-surface-2); }

.btn--ghost {
  background: transparent;
  color: var(--text-secondary);
  border-color: var(--border-default);
}
.btn--ghost:hover { color: var(--text-primary); background: var(--bg-surface-2); }

.btn--danger {
  background: transparent;
  color: var(--status-error);
  border-color: var(--status-error);
}
.btn--danger:hover { background: rgba(248, 113, 113, 0.1); }

/* Sizes */
.btn--sm { padding: 6px var(--space-2); font-size: var(--text-xs); }
.btn--lg { padding: 14px var(--space-4); font-size: var(--text-base); }
.btn--icon { padding: 10px; }
.btn:disabled { opacity: 0.4; cursor: not-allowed; pointer-events: none; }
```

### Cards

```css
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}
.card--interactive:hover {
  border-color: var(--border-strong);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  cursor: pointer;
}
.card--accent:hover { border-color: var(--accent); }
```

### Form Inputs

```css
.input {
  width: 100%;
  padding: 10px var(--space-2);
  background: var(--bg-surface-2);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  transition: border-color var(--transition-fast);
  outline: none;
}
.input::placeholder { color: var(--text-tertiary); }
.input:focus { border-color: var(--accent); }
.input:invalid { border-color: var(--status-error); }
```

### Dividers

```css
.divider {
  height: 1px;
  background: var(--border-default);
  margin: var(--space-4) 0;
}
.divider--vertical {
  width: 1px;
  height: 100%;
  background: var(--border-default);
}
```

---

## Shadow Scale

```css
:root {
  --shadow-sm:  0 1px 3px rgba(0,0,0,0.3);
  --shadow-md:  0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg:  0 8px 24px rgba(0,0,0,0.5);
  --shadow-xl:  0 16px 48px rgba(0,0,0,0.6);
  --shadow-glow: 0 0 20px rgba(232,255,0,0.15);  /* accent glow for featured elements */
}
```

---

## Border Radius Scale

```css
:root {
  --radius-none: 0px;
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-xl:   16px;
  --radius-2xl:  24px;
  --radius-full: 9999px;
}
```

---

## CSS Reset (Minimal — include before tokens)

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
body { font-family: var(--font-body); color: var(--text-primary); background: var(--bg-base); line-height: var(--leading-normal); -webkit-font-smoothing: antialiased; }
img, video { display: block; max-width: 100%; }
button, input, select, textarea { font: inherit; }
a { color: inherit; }
```
