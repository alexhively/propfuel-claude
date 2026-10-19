# Pre-Webinar Assets — Long Title Pattern

When a session title is long enough to wrap to 2 lines instead of the usual 1,
the default template font sizes push the headline past the divider. Use these
adjusted values instead. Reference example: "Converting Students to
Professional Membership: Questions to Ask Before Graduation" (~82 characters).

Everything else (colors, logo, eyebrow position, meta row layout, divider
position) stays exactly as in the base templates — only the `.headline` rule
and the meta row font sizes change.

---

## ZOOM BANNER — 1280×400px

```css
.headline {
  position: absolute;
  top: 128px;
  left: 80px;
  right: 40px;
  font-size: 45px;          /* down from default 60px */
  font-weight: 700;
  color: #2F2F2F;
  line-height: 1.15;
  letter-spacing: -0.015em;
  max-width: 1140px;        /* up from default 900px, uses more of the available width */
  z-index: 3;
}
```

Meta row (bumped up from default so it doesn't look undersized next to the
bigger headline block):

```css
.eyebrow { font-size: 16px; }         /* default 13px */
.date-pill { font-size: 18px; padding: 11px 22px; gap: 10px; }   /* default 14px / 9px 18px */
.date-pill svg { width: 19px; height: 19px; }                     /* default 15px */
.time-text { font-size: 20px; }       /* default 16px */
.dot-sep { font-size: 20px; }         /* default 16px */
.duration-text { font-size: 17px; }   /* default 13px */
.speaker-text { font-size: 19px; }    /* default 15px */
```

---

## EMAIL BANNER — 2400×600px

```css
.headline {
  position: absolute;
  top: 218px;
  left: 150px;
  right: 257px;
  font-size: 80px;          /* down from default 112px */
  font-weight: 700;
  color: #2F2F2F;
  line-height: 1.15;
  letter-spacing: -0.015em;
  max-width: 1993px;
  z-index: 3;
}
```

Meta row:

```css
.eyebrow { font-size: 30px; }         /* default 24px */
.date-pill { font-size: 33px; padding: 20px 42px; gap: 16px; }   /* default 26px / 16px 34px */
.date-pill svg { width: 33px; height: 33px; }                     /* default 26px */
.time-text { font-size: 38px; }       /* default 30px */
.dot-sep { font-size: 38px; }         /* default 30px */
.duration-text { font-size: 31px; }   /* default 24px */
.speaker-text { font-size: 35px; }    /* default 26px */
```

---

## POP-UP — 1080×1080px

```css
.headline {
  font-size: 66px;          /* down from default 76px */
  /* position/left/right/line-height unchanged from base template */
}
```

---

## Workflow note

For a long title, render once at the base template's default sizes first,
check the output — if the headline wraps to 3+ lines and crowds or overlaps
the divider, drop in the values above as a starting point, then nudge
`top` and `font-size` slightly based on the actual line count and length of
this specific title. These values were tuned for an ~80-82 character title
wrapping to exactly 2 lines; a title of a different length may need slightly
different numbers.
