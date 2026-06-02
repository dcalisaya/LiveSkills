# SEO Reference — Live Developer Stack

## SEO Strategy Framework

Every piece of content must answer:

1. **What is the target keyword?** — One primary, 2-4 secondary.
2. **What is the search intent?** — Informational, navigational, transactional, or commercial.
3. **Who ranks now?** — Analyze the top 5 results. What format do they use? What's missing?
4. **What's our angle?** — How is our content better, deeper, or more current?

---

## Keyword Research Process

### Step 1: Seed Keywords

Start from the business problem, not from a tool:

```
Business: "We help agencies automate deliverables"

Seed keywords:
- agency project management
- automate client deliverables
- agency workflow automation
- SaaS for creative agencies
- deliverable tracking software
```

### Step 2: Expand with Intent Categories

| Intent | Keywords | Content Type |
|---|---|---|
| Informational | "how to automate agency workflows" | Blog post, guide |
| Commercial | "best project management tools for agencies" | Comparison, listicle |
| Transactional | "agency project management software pricing" | Landing page |
| Navigational | "LiveApp login", "LiveApp demo" | Product page |

### Step 3: Prioritize

| Factor | Weight | Description |
|---|---|---|
| Relevance | High | Does this match what we sell? |
| Volume | Medium | Are people actually searching for this? |
| Difficulty | Medium | Can we realistically rank? (Domain authority matters) |
| Intent alignment | High | Will this searcher become a customer? |

---

## On-Page SEO Checklist

Apply to every page or blog post:

```
□ Primary keyword in title tag (front-loaded)
□ Primary keyword in H1 (naturally, not stuffed)
□ Primary keyword in first 100 words
□ Primary keyword in URL slug
□ Meta description (150-160 chars) with keyword + CTA
□ H2/H3 subheadings include secondary keywords
□ Internal links to 2-3 related pages
□ External links to 1-2 authoritative sources
□ Images have descriptive alt text with keywords
□ URL is clean and short (/agency-workflow-automation not /p?id=4827)
□ Content is 1500+ words for informational, 500+ for transactional
□ Schema markup (Article, FAQ, or Product as appropriate)
```

---

## Content Structure for SEO

### Blog Post Template (Informational)

```markdown
# [Primary Keyword] — [Benefit or Angle]

[Hook paragraph — state the problem, promise a solution. 2-3 sentences. Include primary keyword.]

## Table of Contents
[Auto-generated or manual — improves UX and may trigger featured snippets]

## What is [Topic]?
[Definition section — targets featured snippet. Keep first paragraph under 50 words.]

## Why [Topic] Matters for [Audience]
[Build relevance. Connect to reader's pain points.]

## How to [Do the Thing]: Step-by-Step
### Step 1: [Action]
### Step 2: [Action]
### Step 3: [Action]

## [Primary Keyword] Best Practices
[Listicle section — 5-7 bullet points. Each is a scannable standalone tip.]

## Common Mistakes to Avoid
[Negative angle — "don't do X" content performs well for engagement.]

## FAQ
[3-5 questions in Q&A format. Use FAQ schema markup.]

## Conclusion
[Summarize key takeaway. CTA to related content or product.]
```

### Landing Page SEO

```html
<!-- Title tag -->
<title>Agency Workflow Automation | LiveApp by Live Developer</title>

<!-- Meta description -->
<meta name="description" content="Automate your agency's deliverable workflow with LiveApp. Ship 3× faster with AI-powered project management. Start free trial.">

<!-- Open Graph -->
<meta property="og:title" content="Agency Workflow Automation | LiveApp">
<meta property="og:description" content="Ship deliverables 3× faster with AI-powered automation.">
<meta property="og:image" content="https://livedeveloper.com/og/liveapp-preview.png">
<meta property="og:type" content="website">

<!-- Canonical -->
<link rel="canonical" href="https://livedeveloper.com/liveapp">
```

---

## Technical SEO

### Required for Every Site

```html
<!-- robots.txt -->
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Sitemap: https://livedeveloper.com/sitemap.xml
```

```xml
<!-- sitemap.xml (auto-generate, update on publish) -->
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://livedeveloper.com/</loc>
    <lastmod>2026-06-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://livedeveloper.com/blog/agency-workflow-automation</loc>
    <lastmod>2026-05-28</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

### Performance (Core Web Vitals)

| Metric | Target | Impact |
|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | Ranking factor |
| FID (First Input Delay) | < 100ms | Ranking factor |
| CLS (Cumulative Layout Shift) | < 0.1 | Ranking factor |
| TTFB (Time to First Byte) | < 600ms | Indirect |

### Performance Checklist

```
□ Images: WebP format, lazy loading, explicit width/height
□ Fonts: preconnect, display=swap, subset if possible
□ CSS: critical CSS inlined, rest deferred
□ JavaScript: async/defer, no render-blocking scripts
□ Caching: Cache-Control headers on static assets (1 year)
□ Compression: Brotli or gzip on server
□ CDN: Cloudflare proxied for static assets
```

---

## Schema Markup (Structured Data)

### Article

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Automate Agency Workflows in 2026",
  "author": {
    "@type": "Person",
    "name": "Daniel Calisaya"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Live Developer"
  },
  "datePublished": "2026-06-01",
  "dateModified": "2026-06-01",
  "description": "Step-by-step guide to automating agency deliverables..."
}
</script>
```

### FAQ

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is agency workflow automation?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Agency workflow automation uses software to..."
      }
    }
  ]
}
</script>
```

---

## Internal Linking Strategy

- Every new page links to 2-3 existing related pages.
- Every existing related page gets a link back to the new page.
- Use descriptive anchor text (not "click here").
- Create content clusters: one pillar page + 5-10 supporting articles.
- Update sitemap after every publish.

---

## Content Refresh Cadence

| Content Type | Review Cycle | Action |
|---|---|---|
| Evergreen blog post | Quarterly | Update stats, add new sections |
| Comparison/listicle | Monthly | Check competitors, update rankings |
| Landing page | After every feature release | Update copy and screenshots |
| Case study | Annually | Refresh metrics, add updates |
