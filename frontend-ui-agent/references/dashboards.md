# Dashboards & Admin Panels Reference — Live Developer Stack

## Dashboard Design Philosophy

A dashboard is a **decision support tool**. Every element should help the user take an action
or understand a status. Remove anything that doesn't serve that purpose.

Design order: **Information architecture → Data hierarchy → Layout → Visual polish**

---

## Dashboard Types

### 1. Metrics Dashboard (KPI Overview)
Goal: At a glance, show the health of a system/project.
Pattern: Stat cards → Chart → Table → Alerts

### 2. Operations Dashboard (Live Activity)
Goal: Monitor ongoing processes, catch issues.
Pattern: Status indicators → Live feed → Queue lists → Actions

### 3. Management Admin Panel (CRUD)
Goal: Read, create, update, delete records.
Pattern: Sidebar nav → Data table → Detail panel/drawer

### 4. Client Portal (Read-mostly)
Goal: External client reviews deliverables, approves, comments.
Pattern: Card gallery → Review modal → Timeline → Status badges

---

## Layout Patterns

### Sidebar + Main Content (Standard Admin)

```html
<div class="app-shell">
  <aside class="sidebar">
    <div class="sidebar__logo"><!-- brand --></div>
    <nav class="sidebar__nav">
      <a class="nav-item nav-item--active" href="#">Dashboard</a>
      <a class="nav-item" href="#">Projects</a>
      <a class="nav-item" href="#">Deliverables</a>
      <a class="nav-item" href="#">Clients</a>
    </nav>
    <div class="sidebar__footer"><!-- user profile --></div>
  </aside>

  <main class="main-content">
    <header class="page-header">
      <h1 class="page-title">Dashboard</h1>
      <div class="page-actions"><!-- primary action button --></div>
    </header>
    <div class="page-body"><!-- content --></div>
  </main>
</div>
```

```css
.app-shell {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
  background: var(--bg-base);
}

.sidebar {
  display: flex;
  flex-direction: column;
  padding: var(--space-3);
  background: var(--bg-surface);
  border-right: 1px solid var(--border-default);
  position: sticky;
  top: 0;
  height: 100vh;
}

.main-content {
  padding: var(--space-4) var(--space-6);
  overflow-y: auto;
}
```

---

## Stat Cards

```html
<div class="stat-grid">
  <div class="stat-card">
    <span class="stat-card__label">Active Projects</span>
    <span class="stat-card__value">24</span>
    <span class="stat-card__delta stat-card__delta--up">+3 this week</span>
  </div>
  <!-- repeat -->
</div>
```

```css
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}

.stat-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: var(--space-3) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  transition: border-color var(--transition-fast);
}

.stat-card:hover {
  border-color: var(--accent);
}

.stat-card__label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-card__value {
  font-size: var(--text-4xl);
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.stat-card__delta--up { color: #4ade80; font-size: var(--text-sm); }
.stat-card__delta--down { color: #f87171; font-size: var(--text-sm); }
```

---

## Data Tables

```html
<div class="table-wrapper">
  <table class="data-table">
    <thead>
      <tr>
        <th class="data-table__th">Project</th>
        <th class="data-table__th">Client</th>
        <th class="data-table__th">Status</th>
        <th class="data-table__th data-table__th--right">Due</th>
        <th class="data-table__th"></th>
      </tr>
    </thead>
    <tbody>
      <tr class="data-table__row">
        <td class="data-table__td">Brand Kit v2</td>
        <td class="data-table__td">GIZ Ecuador</td>
        <td class="data-table__td">
          <span class="badge badge--review">In Review</span>
        </td>
        <td class="data-table__td data-table__td--right">Jun 15</td>
        <td class="data-table__td">
          <button class="btn btn--ghost btn--sm">Open</button>
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

```css
.data-table { width: 100%; border-collapse: collapse; }
.data-table__th {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-secondary);
  padding: var(--space-2) var(--space-2);
  text-align: left;
  border-bottom: 1px solid var(--border-default);
}
.data-table__td {
  padding: var(--space-2);
  border-bottom: 1px solid var(--border-default);
  font-size: var(--text-sm);
  color: var(--text-primary);
}
.data-table__row:hover .data-table__td { background: var(--bg-surface-2); }
```

---

## Status Badges

```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 10px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: 0.03em;
}
.badge--draft     { background: #1e1e1e; color: #8a8a8a; border: 1px solid #2a2a2a; }
.badge--review    { background: #1a1a2e; color: #818cf8; border: 1px solid #3730a3; }
.badge--approved  { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.badge--revision  { background: #2d1515; color: #f87171; border: 1px solid #7f1d1d; }
.badge--live      { background: #022c22; color: #34d399; border: 1px solid #065f46; }
```

---

## Chart Integration (Chart.js — no build required)

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>

<canvas id="deliverableChart" width="600" height="280"></canvas>

<script>
const ctx = document.getElementById('deliverableChart')
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
      label: 'Deliverables Shipped',
      data: [12, 19, 8, 24, 18, 31],
      backgroundColor: 'rgba(232, 255, 0, 0.7)',  // accent with opacity
      borderColor: '#e8ff00',
      borderWidth: 1,
      borderRadius: 4,
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#f0f0f0', font: { family: 'DM Sans' } } },
    },
    scales: {
      x: { ticks: { color: '#8a8a8a' }, grid: { color: '#2a2a2a' } },
      y: { ticks: { color: '#8a8a8a' }, grid: { color: '#2a2a2a' } },
    }
  }
})
</script>
```

---

## Navigation Items & Active States

```css
.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 10px var(--space-2);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  text-decoration: none;
  transition: color var(--transition-fast), background var(--transition-fast);
}
.nav-item:hover {
  color: var(--text-primary);
  background: var(--bg-surface-2);
}
.nav-item--active {
  color: var(--text-primary);
  background: var(--bg-surface-2);
  border-left: 2px solid var(--accent);
  padding-left: calc(var(--space-2) - 2px);
}
```

---

## Loading & Empty States

Always implement these — they define a production-grade UI:

```html
<!-- Skeleton loader -->
<div class="skeleton skeleton--text"></div>
<div class="skeleton skeleton--card"></div>

<!-- Empty state -->
<div class="empty-state">
  <div class="empty-state__icon"><!-- SVG --></div>
  <h3 class="empty-state__title">No deliverables yet</h3>
  <p class="empty-state__desc">Create your first deliverable to start the review cycle.</p>
  <button class="btn btn--primary">Create Deliverable</button>
</div>
```

```css
.skeleton {
  background: linear-gradient(90deg, var(--bg-surface) 25%, var(--bg-surface-2) 50%, var(--bg-surface) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
  border-radius: var(--radius-sm);
}
.skeleton--text { height: 16px; width: 60%; margin-bottom: 8px; }
.skeleton--card { height: 120px; width: 100%; }

@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```
