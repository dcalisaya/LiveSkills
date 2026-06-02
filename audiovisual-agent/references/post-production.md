# Post-Production Reference — Live Developer Stack

## Editing Workflow

```
Import → Organize → Rough Cut → Fine Cut → Color → Audio → Graphics → Review → Export
```

### Stage Details

| Stage | Goal | Tools |
|---|---|---|
| Import & Organize | Sync, label, bin clips | DaVinci Resolve, Premiere |
| Rough Cut (Assembly) | Sequence structure, timing | Timeline editor |
| Fine Cut | Pacing, transitions, trimming | Timeline editor |
| Color Grading | Mood, consistency, brand colors | DaVinci Resolve (Color page) |
| Audio Mix | Levels, music, SFX, narration | DaVinci Fairlight, Audition |
| Motion Graphics | Titles, lower thirds, transitions | After Effects, Fusion |
| Review | Client feedback, HITL approval | Frame.io, Google Drive |
| Export | Platform-specific renders | Media Encoder, Resolve Deliver |

---

## Edit Decision List (EDL) Format

When directing an editor, provide cuts as an EDL:

```
## Edit Decision List — [Project Name]

| Cut # | In | Out | Duration | Source Clip | Notes |
|---|---|---|---|---|---|
| 1 | 00:00 | 00:03 | 3s | logo_reveal_v2.mov | Fade from black, 1s hold |
| 2 | 00:03 | 00:08 | 5s | office_wide_01.mov | Cut on beat, music starts |
| 3 | 00:08 | 00:12 | 4s | inbox_cu_screen.mov | Match cut from laptop |
| 4 | 00:12 | 00:18 | 6s | app_screenrec_v3.mp4 | Smooth scroll, add cursor highlight |
| 5 | 00:18 | 00:23 | 5s | split_comparison.mov | Before/after wipe transition |
| 6 | 00:23 | 00:26 | 3s | endcard_cta.psd | Fade in CTA text, hold 2s |
```

---

## Color Grading

### Process

1. **Balance** — Correct white balance, exposure, and contrast for consistency.
2. **Match** — Ensure all shots from the same scene look consistent.
3. **Look** — Apply the creative grade (mood, tone, brand alignment).
4. **Verify** — Check on multiple displays (monitor, phone, projector).

### Common Looks

| Look | Description | Use For |
|---|---|---|
| Clean Corporate | Neutral, balanced, slightly desaturated | B2B, presentations |
| Warm Documentary | Lifted shadows, warm tones, organic | Testimonials, behind-the-scenes |
| High Contrast | Deep blacks, bright highlights, punchy | Tech products, modern brands |
| Cinematic Teal/Orange | Split toning, filmic feel | Brand films, trailers |
| Bright & Clean | Slightly overexposed, light shadows | Lifestyle, wellness, SaaS |

### Scopes to Check

- **Waveform** — Exposure (keep highlights below 100 IRE, shadows above 0)
- **Vectorscope** — Color balance (skin tones should sit on the skin tone line)
- **Parade** — RGB channel balance (even distribution = neutral white balance)

---

## Audio Mix Guidelines

### Level Standards

| Element | Target Level (LUFS) | Notes |
|---|---|---|
| Dialogue / Narration | -12 to -14 LUFS | Clearest element, always on top |
| Music (under narration) | -24 to -30 LUFS | Duck under voice, swell in gaps |
| Music (standalone) | -14 to -16 LUFS | When no narration is present |
| Sound Effects | -18 to -24 LUFS | Subtle, supportive, not distracting |
| Overall mix | -14 LUFS (YouTube) / -16 LUFS (broadcast) | Platform-dependent |

### Audio Checklist

```
□ Narration is clear and intelligible at all times
□ Music ducks under dialogue automatically (sidechain or keyframes)
□ No clipping (peaks stay below -1 dBFS)
□ Consistent levels across all cuts (no jarring volume changes)
□ Room tone / ambient fill between dialogue edits
□ De-essing applied if sibilance is present
□ Low-cut filter on dialogue (remove rumble below 80 Hz)
□ Audio fades at start and end (avoid hard cuts)
```

---

## Motion Graphics Specifications

### Lower Thirds

```
Position: Bottom left, 10% from edge
Size: Max 1/4 screen width
Font: Brand display font (Syne or equivalent)
Duration: 4-6 seconds
Animation: Slide in from left (200ms ease-out) → Hold → Fade out (150ms)
Background: Semi-transparent dark (#000000 at 60% opacity)
```

### Title Cards

```
Position: Center
Size: Max 60% screen width
Font: Brand display font, 700 weight
Duration: 3-5 seconds
Animation: Scale from 95% to 100% + fade in (300ms ease-out)
Background: Full-bleed background color or footage
```

### Animated Callouts / Annotations

```
Style: Line + circle + text (minimal, not cluttered)
Color: Brand accent color only
Animation: Draw-on effect (line draws, circle appears, text fades in)
Duration: Hold 3-4 seconds, then fade out
```

---

## Export Specifications

### Platform-Specific Settings

| Platform | Resolution | Frame Rate | Codec | Bitrate | Audio | Aspect Ratio |
|---|---|---|---|---|---|---|
| YouTube | 3840×2160 or 1920×1080 | 24/30 fps | H.264 / H.265 | 35-45 Mbps (4K) | AAC 320kbps | 16:9 |
| Instagram Reels | 1080×1920 | 30 fps | H.264 | 10-15 Mbps | AAC 256kbps | 9:16 |
| TikTok | 1080×1920 | 30 fps | H.264 | 10-15 Mbps | AAC 256kbps | 9:16 |
| LinkedIn | 1920×1080 | 30 fps | H.264 | 15-20 Mbps | AAC 256kbps | 16:9 |
| Website (embedded) | 1920×1080 | 24/30 fps | H.264 | 8-12 Mbps | AAC 192kbps | 16:9 |
| Client Master | 3840×2160 | 24 fps | ProRes 422 HQ | ~220 Mbps | PCM 48kHz | 16:9 |

### File Naming Convention

```
[client]_[project]_[format]_[version]_[date].[ext]

Examples:
acme_annual-report_explainer_v2_20260601.mp4
livedeveloper_liveapp-launch_reel_v1_20260601.mp4
livedeveloper_liveapp-launch_reel_v1_20260601_master.mov
```

### Delivery Checklist

```
□ Exported in correct platform specs
□ Audio levels checked (LUFS meter)
□ Subtitles/captions file included (.srt)
□ Thumbnail created (if YouTube/social)
□ Master file archived (ProRes/high-quality)
□ Client approved final version
□ All project files organized and backed up
□ Metadata added (title, description, tags for SEO)
```

---

## Review Process (HITL)

### Feedback Collection

Use timecoded feedback to avoid ambiguity:

```
## Review Feedback — [Project Name] — [Version]

| Timecode | Reviewer | Feedback | Priority |
|---|---|---|---|
| 00:05 | Daniel | "This cut feels too abrupt — add a dissolve" | Should fix |
| 00:12 | Client | "Can we see more of the dashboard here?" | Must fix |
| 00:20 | Daniel | "Music is too loud under narration" | Must fix |
| General | Client | "Love the color grade, keep as is" | ✅ Approved |
```

### Version Control

```
v1 — Rough cut (internal review)
v2 — Fine cut with feedback applied (client review #1)
v3 — Final cut with all revisions (client review #2)
v_final — Approved, exported, delivered
```

Never overwrite a previous version. Always increment.
