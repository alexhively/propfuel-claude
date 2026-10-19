#!/usr/bin/env python3
"""
build_prewebinar_assets.py — builds the 3 PropFuel pre-webinar assets from the project templates.

  Zoom banner      1280x400   TEMPLATE_zoom_banner_1280x400.html
  Email banner     2400x600   TEMPLATE_email_banner_2400x600.html
  Web pop-up       1080x1080  TEMPLATE_popup_1080x1080.html

It does, in code, exactly what was done by hand in every approved session:
  - swaps the blocked Google Fonts @import for a local DM Sans @font-face
  - replaces title / date / time / duration / speaker / description / eyebrow / CTA text
  - appends a CSS override block before </style> (base template is never edited)
  - applies an approved sizing preset, then MEASURES the render and nudges font-size until it fits
  - renders at 2x, downsamples with LANCZOS, saves JPG quality=100 subsampling=0

Presets (see MASTER_CONTEXT doc, section "Sizing presets"):
  auto      (default) try one-line; if the title can't fit on one line, use two-line
  one-line  Oct 15 2026 approved look: single-line headline, grown eyebrow + meta row
  two-line  LONG_TITLE_PATTERN.md values (~80-char title wrapping to exactly 2 lines)
  base      the raw template sizes (June 2026 originals; smallest meta row)

Examples:
  python3 build_prewebinar_assets.py --title "How to Win Back Lapsed Members" \
      --date "Oct 28, 2026" --time "2:00 PM ET" --duration "1 hr" --speaker "Ryan Graham" \
      --description "Two or three sentences for the pop-up." --slug win_back_lapsed_members

  # series session with the subtitle line, 30 min, Brittany:
  python3 build_prewebinar_assets.py --title "Engaging Members Through Events" \
      --subtitle "Session 3 of The Year In Between: how to earn the renewal before renewal season ever starts" \
      --date "Aug 6, 2026" --time "1:00 PM ET" --description "..." --slug yib_s3

  # internal event, no speaker, no duration, different eyebrow:
  python3 build_prewebinar_assets.py --title "PropFuel Client Advisory Board" --date "Sep 23, 2026" \
      --time "11:00 AM ET" --eyebrow "Live Session" --no-speaker --no-duration --only zoom --slug cab
"""
import argparse, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_html_to_jpg import render  # noqa: E402

FONT_TTF = os.path.expanduser("~/.local/share/fonts/DMSans.ttf")
GOOGLE_IMPORT_RE = re.compile(r"@import url\('https://fonts\.googleapis\.com[^']*'\);")
FONT_FACE = ("@font-face { font-family: 'DM Sans'; src: url('file://%s') format('truetype'); "
             "font-weight: 100 1000; }" % FONT_TTF)

# ---------------------------------------------------------------- presets (CSS appended before </style>)
PRESETS = {
  "zoom": {
    "base": "",
    "two-line": """
  .eyebrow { font-size: 16px; top: 30px; }
  .headline { top: 128px; transform: none; right: 40px; font-size: 45px; line-height: 1.15;
              letter-spacing: -0.015em; max-width: 1140px; }
  .date-pill { font-size: 18px; padding: 11px 22px; gap: 10px; }
  .date-pill svg { width: 19px; height: 19px; }
  .time-text { font-size: 20px; } .dot-sep { font-size: 20px; }
  .duration-text { font-size: 17px; } .speaker-text { font-size: 19px; }""",
    "one-line": """
  .eyebrow { font-size: 21px; top: 28px; }
  .headline { max-width: 1150px; white-space: nowrap; font-size: 68px; }
  .bottom-row { top: 317px; gap: 20px; }
  .date-pill { font-size: 20px; padding: 12px 24px; gap: 11px; }
  .date-pill svg { width: 21px; height: 21px; }
  .time-text { font-size: 22px; } .dot-sep { font-size: 22px; }
  .duration-text { font-size: 19px; } .speaker-text { font-size: 21px; }""",
  },
  "email": {
    "base": "",
    "two-line": """
  .eyebrow { font-size: 30px; top: 44px; }
  .headline { top: 218px; transform: none; right: 257px; font-size: 80px; line-height: 1.15;
              letter-spacing: -0.015em; max-width: 1993px; }
  .date-pill { font-size: 33px; padding: 20px 42px; gap: 16px; }
  .date-pill svg { width: 33px; height: 33px; }
  .time-text { font-size: 38px; } .dot-sep { font-size: 38px; }
  .duration-text { font-size: 31px; } .speaker-text { font-size: 35px; }""",
    "one-line": """
  .eyebrow { font-size: 39px; top: 44px; }
  .headline { font-size: 127px; white-space: nowrap; right: auto; }
  .bottom-row { top: 470px; gap: 38px; }
  .date-pill { font-size: 37px; padding: 22px 44px; gap: 20px; }
  .date-pill svg { width: 39px; height: 39px; }
  .time-text { font-size: 41px; } .dot-sep { font-size: 41px; }
  .duration-text { font-size: 36px; } .speaker-text { font-size: 39px; }""",
  },
  "popup": {
    "base": "",
    "two-line": "\n  .headline { font-size: 66px; }",
    "one-line": "\n  .headline { font-size: 76px; }",   # pop-up never forces a single line
  },
}

# Series-subtitle variant (July/Aug 2026 "The Year In Between" sessions). Headline + subtitle are
# centered as ONE block between eyebrow and divider. Zoom values are the approved July 17 numbers;
# email/pop-up values are proportional starting points (nudge after looking at the render).
SUBTITLE_CSS = {
  "zoom": """
  .title-block { position: absolute; top: 175px; transform: translateY(-50%); left: 80px; right: 52px; z-index: 3; }
  .title-block .headline { position: static; transform: none; font-size: 56px; line-height: 1.15;
                           max-width: 1050px; margin: 0 0 16px 0; white-space: normal; }
  .subtitle { font-size: 20px; font-weight: 500; color: #6E6E6E; line-height: 1.35; max-width: 1080px; margin: 0; }""",
  "email": """
  .title-block { position: absolute; top: 262px; transform: translateY(-50%); left: 150px; right: 96px; z-index: 3; }
  .title-block .headline { position: static; transform: none; font-size: 104px; line-height: 1.12;
                           max-width: 1960px; margin: 0 0 28px 0; white-space: normal; }
  .subtitle { font-size: 36px; font-weight: 500; color: #6E6E6E; line-height: 1.35; max-width: 2100px; margin: 0; }""",
  "popup": """
  .title-block { position: absolute; top: 215px; left: 80px; right: 80px; z-index: 3; }
  .title-block .headline { position: static; font-size: 64px; }
  .subtitle { margin-top: 22px; font-size: 26px; font-weight: 500; color: #6E6E6E; line-height: 1.4; }""",
}

SIZES = {"zoom": (1280, 400), "email": (2400, 600), "popup": (1080, 1080)}
TEMPLATE_FILES = {"zoom": "TEMPLATE_zoom_banner_1280x400.html",
                  "email": "TEMPLATE_email_banner_2400x600.html",
                  "popup": "TEMPLATE_popup_1080x1080.html"}
OUT_NAMES = {"zoom": "zoom_banner_{slug}_1280x400", "email": "email_banner_{slug}_2400x600",
             "popup": "popup_{slug}_1080x1080"}
# Right edge the headline text must stay inside (divider right edge minus a small margin)
MAX_TEXT_RIGHT = {"zoom": 1280 - 52 - 8, "email": 2400 - 96 - 10}
MIN_ONELINE_FONT = {"zoom": 50, "email": 94}
MIN_TWOLINE_FONT = {"zoom": 36, "email": 64}
POPUP_DIVIDER_TOP = 553
POPUP_DIVIDER_TOP_PROOF = 470   # with a proof line the pop-up divider moves up to make room

# Proof line (Webinar Proof Map.md): premier case study result for the webinar's use case.
PROOF_CSS = {
  "zoom": ".proof { margin-left: 22px; max-width: 335px; padding-left: 10px; border-left: 3px solid #F47C2C; font-size: 15px; font-weight: 700; color: #2F2F2F; line-height: 1.25; }",
  "email": ".proof { margin-left: 44px; max-width: 780px; padding-left: 18px; border-left: 5px solid #F47C2C; font-size: 28px; font-weight: 700; color: #2F2F2F; line-height: 1.25; }",
  "popup": """
  .proof { position: absolute; left: 80px; right: 72px; top: 776px; z-index: 3; padding-left: 26px; border-left: 6px solid #F47C2C; }
  .proof-label { display: block; font-size: 20px; font-weight: 600; letter-spacing: 0.08em; color: #F47C2C; text-transform: uppercase; margin-bottom: 4px; }
  .proof-text { display: block; font-size: 30px; font-weight: 700; color: #2F2F2F; line-height: 1.25; letter-spacing: -0.01em; }
  .eyebrow { top: 94px; } .headline { top: 222px; }
  .divider { top: 470px; } .datetime-row { top: 522px; } .description { top: 608px; }""",
}


def ensure_font():
    if not os.path.isfile(FONT_TTF) or os.path.getsize(FONT_TTF) == 0:
        subprocess.run(["bash", os.path.join(HERE, "install_dmsans.sh")], check=False)


def fill(kind, src, a):
    """Replace every editable field in the template. Base templates are never modified on disk."""
    s = GOOGLE_IMPORT_RE.sub(FONT_FACE, src, count=1)
    title_html = a.title.replace("&", "&amp;")
    if a.subtitle:
        if True:
            s = re.sub(r'<h1 class="headline">.*?</h1>',
                       f'<div class="title-block"><h1 class="headline">{title_html}</h1>'
                       f'<p class="subtitle">{a.subtitle}</p></div>', s, flags=re.S)
    else:
        s = re.sub(r'<h1 class="headline">.*?</h1>', f'<h1 class="headline">{title_html}</h1>', s, flags=re.S)
    s = re.sub(r'class="eyebrow">[^<]*<', f'class="eyebrow">{a.eyebrow}<', s)
    s = re.sub(r'[A-Z][a-z]{2} \d{1,2}, \d{4}', a.date, s)          # Jun 17, 2026 -> date
    s = re.sub(r'\d{1,2}:\d{2} [AP]M ET', a.time, s)                 # 12:00 PM ET -> time
    if kind in ("zoom", "email"):
        if a.no_duration:
            s = re.sub(r'\s*<span class="dot-sep">·</span>\s*<span class="duration-text">[^<]*</span>', '', s)
        else:
            s = re.sub(r'Duration: [^<]+', f'Duration: {a.duration}', s)
        if a.no_speaker:
            s = re.sub(r'\s*<div class="speaker-push"></div>\s*<span class="speaker-text">.*?</span>', '', s, flags=re.S)
        else:
            s = re.sub(r'(Speaker: )<strong>[^<]+</strong>', rf'\1<strong>{a.speaker}</strong>', s)
    else:  # popup
        if a.no_duration:
            s = re.sub(r'\s*<span class="dot-sep">·</span>\s*<span class="dur-text">[^<]*</span>', '', s)
        else:
            s = re.sub(r'<span class="dur-text">[^<]*</span>', f'<span class="dur-text">{a.duration}</span>', s)
        if a.no_speaker:
            s = re.sub(r'\s*<span class="speaker-text">.*?</span>', '', s, flags=re.S)
        else:
            s = re.sub(r'(Speaker: )<strong>[^<]+</strong>', rf'\1<strong>{a.speaker}</strong>', s)
        desc = (a.description or "").replace("&", "&amp;")
        s = re.sub(r'<p class="description">.*?</p>', f'<p class="description">{desc}</p>', s, flags=re.S)
        s = s.replace('<div class="cta-btn">Register Free ', f'<div class="cta-btn">{a.cta} ')
    if a.proof:
        p = a.proof.replace("&", "&amp;")
        if kind == "popup":
            s = s.replace('<span class="speaker-text">', f'<div class="proof"><span class="proof-label">Proof</span><span class="proof-text">{p}</span></div>\n  <span class="speaker-text">', 1)
        else:
            s = s.replace('<div class="speaker-push">', f'<div class="proof">{p}</div>\n    <div class="speaker-push">', 1)
        s = with_css(s, PROOF_CSS[kind])
    return s


def with_css(html, css):
    return html.replace("</style>", css + "\n  " + "</style>", 1)


def build_one(kind, a, tdir, outdir):
    src = open(os.path.join(tdir, TEMPLATE_FILES[kind]), encoding="utf-8").read()
    filled = fill(kind, src, a)
    w, h = SIZES[kind]
    base_name = OUT_NAMES[kind].format(slug=a.slug)
    html_path = os.path.join(outdir, base_name + ".html")
    jpg_path = os.path.join(outdir, base_name + ".jpg")

    def attempt(css, note):
        open(html_path, "w", encoding="utf-8").write(with_css(filled, css))
        m = render(html_path, jpg_path, w, h, return_metrics=True)
        return m

    if a.subtitle:
        css = SUBTITLE_CSS[kind] + (PRESETS[kind]["two-line"] if kind != "popup" else "")
        # keep the meta-row bump from two-line but let the title-block rule win for the headline
        css = css.replace("transform: none; right: 40px;", "").replace("transform: none; right: 257px;", "")
        size = {"zoom": 56, "email": 104, "popup": 64}[kind]
        while True:
            m = attempt(css, "subtitle")
            sub_bottom = m["subtitle_box"]["bottom"] if m.get("subtitle_box") else 0
            limit = {"zoom": 285 - 14, "email": 427 - 20, "popup": POPUP_DIVIDER_TOP - 24}[kind]
            if sub_bottom <= limit or size <= {"zoom": 40, "email": 72, "popup": 48}[kind]:
                break
            size -= 2
            css = css.replace(f"font-size: {size + 2}px; line-height", f"font-size: {size}px; line-height", 1) \
                     .replace(f"position: static; font-size: {size + 2}px;", f"position: static; font-size: {size}px;", 1)
        print(f"  [{kind}] subtitle variant: headline {size}px, {m.get('headline_lines')} line(s), "
              f"subtitle bottom {sub_bottom:.0f} (limit {limit})")
        return jpg_path

    preset = a.preset
    if kind == "popup":
        pop_div = POPUP_DIVIDER_TOP_PROOF if a.proof else POPUP_DIVIDER_TOP
        css = PRESETS["popup"]["two-line" if preset == "two-line" else "base"]
        size = 66 if preset == "two-line" else 76
        while True:
            m = attempt(css, preset)
            bottom = m["headline_box"]["bottom"] if m.get("headline_box") else 0
            if bottom <= pop_div - 24 or size <= 52:
                break
            size -= 2
            css = f"\n  .headline {{ font-size: {size}px; }}"
        print(f"  [popup] headline {size}px, bottom={bottom:.0f} (divider at {pop_div})")
        return jpg_path

    # zoom / email
    if preset in ("auto", "one-line"):
        css = PRESETS[kind]["one-line"]
        size = 68 if kind == "zoom" else 127
        while True:
            m = attempt(css, "one-line")
            right = m.get("headline_text_right") or 0
            if right <= MAX_TEXT_RIGHT[kind]:
                print(f"  [{kind}] one-line at {size}px (text right edge {right:.0f} <= {MAX_TEXT_RIGHT[kind]})")
                return jpg_path
            if size - 2 < MIN_ONELINE_FONT[kind]:
                if preset == "one-line":
                    print(f"  [{kind}] WARNING: could not fit on one line even at {size}px; delivering anyway")
                    return jpg_path
                break  # auto: fall through to two-line
            size -= 2
            css = PRESETS[kind]["one-line"].replace(f"font-size: {68 if kind=='zoom' else 127}px",
                                                     f"font-size: {size}px")
        preset = "two-line"
    if preset == "two-line":
        css = PRESETS[kind]["two-line"]
        size = 45 if kind == "zoom" else 80
        while True:
            m = attempt(css, "two-line")
            lines = m.get("headline_lines") or 2
            if lines <= 2 or size - 2 < MIN_TWOLINE_FONT[kind]:
                print(f"  [{kind}] two-line at {size}px ({lines} lines)")
                return jpg_path
            size -= 2
            css = PRESETS[kind]["two-line"].replace(f"font-size: {45 if kind=='zoom' else 80}px",
                                                     f"font-size: {size}px")
    # base
    attempt("", "base")
    print(f"  [{kind}] base template sizes")
    return jpg_path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True)
    ap.add_argument("--date", required=True, help='e.g. "Oct 28, 2026" (Mon D, YYYY)')
    ap.add_argument("--time", required=True, help='e.g. "1:00 PM ET"')
    ap.add_argument("--duration", default="30 min", help='"30 min" (default) or "1 hr" — ASK if not given')
    ap.add_argument("--speaker", default="Brittany Lancor")
    ap.add_argument("--description", default="", help="pop-up paragraph (2-3 sentences, no speaker name)")
    ap.add_argument("--subtitle", default="", help="series line under the title, e.g. 'Session 3 of The Year In Between: ...'")
    ap.add_argument("--eyebrow", default="Live Webinar", help='"Live Webinar" | "Live Deminar" | "Live Session"')
    ap.add_argument("--cta", default="Register Free", help="pop-up button text")
    ap.add_argument("--preset", default="auto", choices=["auto", "one-line", "two-line", "base"])
    ap.add_argument("--proof", default="", help="proof line from Webinar Proof Map.md (REQUIRED for promo sets; <= 90 chars)")
    ap.add_argument("--no-speaker", action="store_true")
    ap.add_argument("--no-duration", action="store_true")
    ap.add_argument("--only", nargs="*", choices=["zoom", "email", "popup"], default=["zoom", "email", "popup"])
    ap.add_argument("--slug", default=None)
    ap.add_argument("--templates", default=os.path.join(HERE, "..", "templates"))
    ap.add_argument("--out", default="/mnt/user-data/outputs" if os.path.isdir("/mnt/user-data/outputs") else "./out")
    a = ap.parse_args()
    if not a.proof:
        print("WARNING: no --proof. Every promo set needs the premier case study proof line (Webinar Proof Map.md).", file=sys.stderr)
    elif len(a.proof) > 90:
        ap.error("--proof must be 90 characters or fewer")
    if not a.slug:
        a.slug = re.sub(r"[^a-z0-9]+", "_", a.title.lower()).strip("_")[:40]
    tdir = os.path.abspath(a.templates)
    if not os.path.isdir(tdir) and os.path.isdir("/mnt/project"):
        tdir = "/mnt/project"
    os.makedirs(a.out, exist_ok=True)
    ensure_font()
    print(f"Templates: {tdir}\nOutput:    {a.out}\nPreset:    {a.preset}")
    outs = []
    for kind in a.only:
        outs.append(build_one(kind, a, tdir, a.out))
    print("\nDelivered:")
    for o in outs:
        print("  " + o)


if __name__ == "__main__":
    main()
