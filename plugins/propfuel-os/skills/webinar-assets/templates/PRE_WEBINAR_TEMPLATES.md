# PropFuel Pre-Webinar Asset Templates

Use this file as a reference in any chat. Paste it and say:
**"Here are my PropFuel webinar templates. Create the full pre-webinar set for: [title], [date], [time], [description]"**

---

## What gets produced (3 assets)

| Asset | Size | Update |
|-------|------|--------|
| Zoom Banner | 1280×400px | Headline, date, time |
| PropFuel Email Banner | 2400×600px | Headline, date, time, description |
| Web Pop-up | 1080×1080px | Headline, date, time, description |

## Fixed across all assets (never change)
- Speaker: **Brittany Lancor**
- Duration: **30 min**
- PropFuel logo (cropped from reference banner)
- Brand colors: cream `#F4F1EA`, orange `#F47C2C`, yellow `#FBC02D`
- Font: **DM Sans**

---

## ZOOM BANNER SPEC — 1280×400px

**Layout:**
- Left vertical gradient bar (8px), orange→yellow, `#F47C2C → #FBC02D`
- Cream `#F4F1EA` background with paper texture
- "LIVE WEBINAR" eyebrow — orange, 13px, 600 weight, uppercase, letter-spacing 0.08em
- PropFuel logo — top-right, 88px wide
- Headline — DM Sans 700, 60px, `#2F2F2F`, lh 1.1, anchored so it's vertically centered between eyebrow bottom (y≈91) and divider (y≈285); use absolute positioning `top: 270px`
- Divider — y=285px, `#E3DDD2`, 1px
- Bottom row — date pill (gradient, pill shape, calendar icon, white text 14px), time (16px bold), duration (13px grey), speaker right-aligned (15px)
- Date pill gradient: `linear-gradient(to right, #F47C2C, #FBC02D)`

**Fields to update:**
1. Headline text
2. Date (in pill)
3. Time

---

## EMAIL BANNER SPEC — 2400×600px

**Layout:** Same as Zoom Banner scaled to 2400×600px
- Left gradient bar: 15px
- Logo: 165px wide
- Eyebrow: 24px
- Headline: 112px, `font-weight: 700`, top: 50% transform translateY(calc(-50% - 26px))
- Divider: y=427px
- Bottom meta row: top=480px — date pill (26px), time (30px bold), duration (24px), speaker (26px)

**Fields to update:**
1. Headline text
2. Date
3. Time
4. Description (optional — not shown in banner but used for email body context)

---

## WEB POP-UP SPEC — 1080×1080px

**Layout:**
- Top horizontal gradient bar: 14px, `#F47C2C → #FBC02D`, border-radius 40px 40px 0 0
- Card: `border-radius: 40px`, cream `#F4F1EA` bg + paper texture via `::before`
- "LIVE WEBINAR" — orange, 22px, 600, uppercase, absolute `top: 94px, left: 80px`
- Logo — absolute `top: 74px, right: 72px`, 110px wide
- Headline — DM Sans **800**, 76px, `#2F2F2F`, lh 1.05, ls -0.025em, absolute `top: 242px, left/right: 80px`
- Divider — absolute `top: 553px`, `#D8D3C8`
- Datetime row — absolute `top: 605px`; date+time 34px bold `#2F2F2F`, duration 30px regular `#6E6E6E`, dots `#BDBDBD`
- Description — absolute `top: 691px`, **29px**, weight 400, `#6E6E6E`, lh 1.6
- Speaker — absolute `top: 944px, left: 80px`, **29px** weight 400 `#6E6E6E`, name only in bold `#2F2F2F`
- Button — absolute `top: 903px, right: 72px`, **365×101px**, `border-radius: 31px` (NOT pill), gradient `#F4852B → #FDBC2E`, white text 30px bold, arrow is inline SVG (not unicode →):
  ```
  <svg width="28" height="18" viewBox="0 0 28 18" fill="none">
    <line x1="0" y1="9" x2="24" y2="9" stroke="white" stroke-width="2.8" stroke-linecap="round"/>
    <polyline points="16,1 25,9 16,17" fill="none" stroke="white" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  ```

**Fields to update:**
1. Headline text
2. Date
3. Time
4. Description paragraph

---

## HOW TO USE IN A NEW CHAT

Paste this file and say:

> "Using my PropFuel pre-webinar templates, create all 3 assets for:
> - Title: [webinar title]
> - Date: [e.g. Jul 15, 2026]
> - Time: [e.g. 1:00 PM ET]
> - Description: [2-3 sentence description for the pop-up]"

Claude will produce:
- `zoom_banner_[topic].png` — 1280×400px
- `email_banner_[topic]_2400x600.png` — 2400×600px
- `popup_[topic]_1080x1080.png` — 1080×1080px

