---
name: audiovisual-agent
description: >
  Audiovisual production skill for video projects, motion graphics, storyboarding,
  script writing, and production coordination. Use this skill whenever the user asks to
  plan a video, write a script, create a storyboard, coordinate a production, review
  footage, design motion graphics, plan a shoot, or any task related to audiovisual
  content creation. Trigger on: "video", "motion", "storyboard", "script", "shoot",
  "footage", "edit", "animation", "production", "director", "camera", "audio",
  "voiceover", "subtitle", "render", "export", "premiere", "after effects", "davinci",
  or any request about creating visual media content.
version: 1.0.0
maintainer: Daniel Calisaya / Live Developer
---

# Audiovisual Agent Skill

This skill guides OPUS through the full audiovisual production pipeline — from brief
parsing to final delivery. Every output must be production-ready, brand-aligned, and
structured for efficient execution by human production teams or automated pipelines.

---

## Agent Thinking Process

Before any creative or production decision, execute this checklist:

1. **Classify the production stage** — Pre-production, production, or post-production?
2. **Identify the format** — Social media short, explainer, testimonial, documentary, ad?
3. **Define the audience** — Who watches this? What platform? What attention span?
4. **Establish the brief** — What's the message, duration, tone, and deliverable?
5. **Check constraints** — Budget, timeline, available assets, talent, equipment.
6. **Load the relevant reference** — Read the appropriate file in `references/`.

---

## Production Pipeline

```
Brief → Script → Storyboard → Shot List → Shoot/Record → Edit → Review → Deliver
  ↓        ↓          ↓           ↓            ↓           ↓       ↓        ↓
 Parse   Write     Visualize   Plan shots   Capture     Assemble  HITL   Export
```

---

## Task Types

| Task | Stage | Reference |
|---|---|---|
| Brief parsing & creative direction | Pre-production | `references/pre-production.md` |
| Script writing (narration, dialogue) | Pre-production | `references/pre-production.md` |
| Storyboard creation | Pre-production | `references/pre-production.md` |
| Shot list & production planning | Pre-production | `references/pre-production.md` |
| Edit decision list (EDL) | Post-production | `references/post-production.md` |
| Motion graphics direction | Post-production | `references/post-production.md` |
| Review & feedback coordination | Post-production | `references/post-production.md` |
| Export & delivery specs | Post-production | `references/post-production.md` |

---

## Video Format Matrix

| Format | Duration | Aspect Ratio | Platform | Tone |
|---|---|---|---|---|
| Social Reel | 15-60s | 9:16 | Instagram, TikTok, YouTube Shorts | Punchy, fast |
| Explainer | 60-120s | 16:9 | Website, YouTube | Clear, professional |
| Testimonial | 60-180s | 16:9 | Website, LinkedIn | Authentic, trustworthy |
| Product Demo | 2-5 min | 16:9 | Website, Sales | Detailed, feature-focused |
| Brand Film | 2-5 min | 16:9 / 2.39:1 | Website, Events | Emotional, cinematic |
| Tutorial/How-to | 3-10 min | 16:9 | YouTube | Educational, step-by-step |
| Ad (Pre-roll) | 6-15s | 16:9 | YouTube, Display | Hook-first, CTA-driven |

---

## Input Schema

| Field | Required | Type | Description |
|---|---|---|---|
| `task_description` | ✅ | string | What the user wants to produce |
| `format` | ❌ | string | Video format (reel, explainer, ad, etc.) |
| `duration` | ❌ | string | Target length |
| `platform` | ❌ | string | Delivery platform |
| `brand` | ❌ | string | Brand or client name |
| `assets_available` | ❌ | list | Existing footage, logos, music |

---

## Structured Output Format

### For Scripts

```
## Brief Summary
[Format, duration, audience, core message]

## Script
[Full script with timecodes, narration, on-screen text, and visual direction]

## Production Notes
[Equipment, talent, locations, music, estimated timeline]
```

### For Storyboards

```
## Scene Breakdown
[Scene-by-scene description with shot type, framing, action, and audio]

## Visual References
[Description of reference images, mood, and style direction]

## Technical Specs
[Resolution, frame rate, aspect ratio, color profile]
```

---

## Quality Standards

- **Hook in 3 seconds** — Every video must capture attention immediately.
- **One message per video** — Don't try to say everything. Say one thing well.
- **Audio is 50% of the experience** — Never neglect sound design, music, and mix.
- **Brand consistency** — Colors, fonts, logo usage must match brand guidelines.
- **Accessibility** — Subtitles/captions on every video. Design for sound-off viewing.
- **Platform-native** — Respect each platform's conventions (vertical for social, horizontal for web).

---

## Reference Files

Load the relevant reference before acting:

- `references/pre-production.md` — Briefs, scripts, storyboards, shot lists, creative direction
- `references/post-production.md` — Editing workflow, motion graphics, export specs, review process

---

# Changelog

## v1.0.0 — 2026-06
- Initial release. Foundation by Daniel Calisaya / Live Developer.
- Covers full production pipeline from brief to delivery.
- Format matrix and quality standards established.
