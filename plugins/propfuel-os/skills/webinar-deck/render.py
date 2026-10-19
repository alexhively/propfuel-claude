#!/usr/bin/env python3
# Bundled copy of the content repurposer templates/deck/render.py (source of truth); refresh it with cp when that file changes.
"""PropFuel webinar deck renderer. One deck spec (JSON) → an editable PPTX (talk track in the speaker notes; opens in
Google Slides) and a PDF in the house look (HTML rendered by headless Chrome). Layouts mirror the 2026 house decks
(knowledge/webinars/DECK-BRAIN.md has the layout library and when to use each).

  python3 templates/deck/render.py deck.json [--out DIR] [--no-pdf] [--no-pptx]

Spec: {"title": "...", "slides": [{"layout": "cover", ...fields, "notes": "talk track"}]}. Fields per layout: LAYOUTS below.
A field left out is simply not drawn. Text in *asterisks* is set in the orange accent (one phrase per headline at most)."""
import html, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
# One self-contained file: the logo travels inside it (the OS doc "Skill - webinar-deck - renderer.md" is this file).
LOGO_B64 = "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"
def logo_path():
    p = HERE / 'propfuel_logo.png'
    if not p.exists():
        p = Path(tempfile.gettempdir()) / 'propfuel_logo.png'
        if not p.exists(): p.write_bytes(__import__('base64').b64decode(LOGO_B64))
    return p
def find_chrome():
    import glob, os
    c = [os.environ.get('CHROME'), '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', shutil.which('google-chrome'), shutil.which('chromium'), shutil.which('chromium-browser')]
    c += sorted(glob.glob(os.path.expanduser('~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome')))
    return next((x for x in c if x and Path(x).exists()), None)
INK, MUTED, CREAM, CARD, LINE = '2F2F2F', '6E6E6E', 'F4F1EA', 'FBF9F4', 'E3DDD2'
ORANGE, YELLOW, ORANGE_INK = 'F47C2C', 'FBC02D', 'E2621B'

# layout → fields it draws (documentation + validation)
LAYOUTS = {
    'cover': ['eyebrow', 'title', 'subtitle', 'tagline'],
    'host': ['pill', 'name', 'role', 'blurb', 'bullets', 'photo'],
    'about': ['pill', 'headline', 'lines', 'pillars', 'tagline'],
    'agenda': ['title', 'items', 'footer'],
    'poll': ['pill', 'question', 'sub'],
    'section': ['pill', 'headline', 'sub'],
    'reframe': ['eyebrow', 'line1', 'line2', 'body', 'kicker'],
    'problem-list': ['pill', 'headline', 'items', 'kicker'],
    'cards': ['pill', 'headline', 'sub', 'cards', 'kicker'],
    'framework': ['pill', 'headline', 'sub'],
    'case-study': ['pill', 'client', 'sub', 'challenge', 'approach', 'stat', 'stat_label', 'metrics'],
    'image': ['pill', 'headline', 'sub', 'image', 'caption'],
    'bar-answers': ['pill', 'headline', 'bars', 'lines', 'kicker'],
    'steps': ['pill', 'headline', 'sub', 'steps', 'footer'],
    'three-things': ['headline', 'items'],
    'next-session': ['pill', 'line1', 'line2', 'body', 'cta'],
    'qa': ['headline', 'sub'],
    'close-cta': ['title', 'lines', 'cta'],
    'quote': ['quote', 'who'],
}

# ---------------------------------------------------------------- HTML / PDF
def esc(s):
    s = html.escape(str(s or ''))
    return re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)

def pill(t): return f'<span class="pill">{esc(t)}</span>' if t else ''

def slide_html(s, base):
    L, g = s['layout'], s.get
    if L == 'cover':
        body = f'<div class="center">{pill(g("eyebrow"))}<h1 class="xl">{esc(g("title"))}</h1><p class="sub">{esc(g("subtitle"))}</p><p class="tag">{esc(g("tagline") or "Know and Grow Your Membership")}</p></div>'
    elif L == 'host':
        photo = f'<img class="photo" src="{(base / g("photo")).resolve().as_uri()}">' if g('photo') else '<div class="photo ph"></div>'
        bl = ''.join(f'<li>{esc(b)}</li>' for b in g('bullets') or [])
        body = f'<div class="host">{photo}<div>{pill(g("pill") or "YOUR HOST")}<h1>{esc(g("name"))}</h1><p class="role">{esc(g("role"))}</p><p class="body">{esc(g("blurb"))}</p><ul class="dots">{bl}</ul></div></div>'
    elif L == 'about':
        ln = ''.join(f'<li>{esc(x)}</li>' for x in g('lines') or [])
        pl = ''.join(f'<div class="pillar"><div class="ico"></div><b>{esc(p.get("label"))}</b><span>{esc(p.get("text"))}</span></div>' for p in g('pillars') or [])
        body = f'{pill(g("pill") or "ABOUT US")}<h1>{esc(g("headline"))}</h1><hr><ul class="dash">{ln}</ul><div class="pillars">{pl}</div><p class="tag left">{esc(g("tagline") or "")}</p>'
    elif L == 'agenda':
        it = ''.join(f'<div class="row"><span class="num">{i + 1:02d}</span><span>{esc(x)}</span></div>' for i, x in enumerate(g('items') or []))
        body = f'<h1>{esc(g("title") or "What we’re covering today")}</h1><div class="rows">{it}</div><p class="foot">{esc(g("footer") or "30 MINUTES  |  Q&A AT THE END")}</p>'
    elif L in ('poll', 'section', 'framework', 'qa'):
        p = g('pill') or {'poll': 'QUICK POLL', 'qa': ''}.get(L, '')
        h = g('question') or g('headline') or ('Questions?' if L == 'qa' else '')
        body = f'<div class="center">{pill(p)}<h1 class="xl">{esc(h)}</h1><p class="sub">{esc(g("sub"))}</p></div>'
    elif L == 'reframe':
        body = f'<div class="vmid"><p class="eyebrow">{esc(g("eyebrow"))}</p><h1>{esc(g("line1"))}<br><em>{esc(g("line2"))}</em></h1><hr class="short"><p class="body">{esc(g("body"))}</p></div><p class="kicker">{esc(g("kicker"))}</p>'
    elif L == 'problem-list':
        it = ''.join(f'<div class="item"><i>{i + 1}</i><span>{esc(x)}</span></div>' for i, x in enumerate(g('items') or []))
        body = f'{pill(g("pill"))}<h1>{esc(g("headline"))}</h1><div class="items">{it}</div><p class="kicker">{esc(g("kicker"))}</p>'
    elif L == 'cards':
        cs = g('cards') or []
        it = ''.join(f'<div class="card"><p class="lab">{esc(c.get("label"))}</p>{"<h3>" + esc(c.get("title")) + "</h3>" if c.get("title") else ""}<p>{esc(c.get("text"))}</p></div>' for c in cs)
        body = f'{pill(g("pill"))}<h1>{esc(g("headline"))}</h1><p class="sub left">{esc(g("sub"))}</p><div class="cards n{len(cs)}">{it}</div><p class="kicker">{esc(g("kicker"))}</p>'
    elif L == 'case-study':
        ms = ''.join(f'<div class="m"><span>{esc(m.get("label"))}</span><b>{esc(m.get("value"))}</b></div>' for m in g('metrics') or [])
        body = (f'{pill(g("pill") or "IN PRACTICE")}<h1>{esc(g("client"))}</h1><p class="sub left">{esc(g("sub"))}</p><div class="cs"><div>'
                f'<p class="lab">THE CHALLENGE</p><p>{esc(g("challenge"))}</p><p class="lab">THE APPROACH</p><p>{esc(g("approach"))}</p></div>'
                f'<div class="statbox"><b class="stat">{esc(g("stat"))}</b><span>{esc(g("stat_label"))}</span>{ms}</div></div>')
    elif L == 'image':
        img = f'<img class="shot" src="{(base / g("image")).resolve().as_uri()}">' if g('image') else '<div class="shot ph">screenshot</div>'
        body = f'{pill(g("pill"))}<h1>{esc(g("headline"))}</h1><p class="sub left">{esc(g("sub"))}</p>{img}<p class="caption">{esc(g("caption"))}</p>'
    elif L == 'bar-answers':
        bars = g('bars') or []; mx = max([b.get('value', 0) for b in bars] or [1]) or 1
        it = ''.join(f'<div class="bar"><span>{esc(b.get("label"))}</span><i style="width:{60 * b.get("value", 0) / mx:.1f}%"></i><b>{esc(b.get("value"))}</b></div>' for b in bars)
        ln = ''.join(f'<p class="small">{esc(x)}</p>' for x in g('lines') or [])
        body = f'{pill(g("pill"))}<h1>{esc(g("headline"))}</h1><div class="bars">{it}</div>{ln}<p class="kicker">{esc(g("kicker"))}</p>'
    elif L == 'steps':
        it = ''.join(f'<div class="card"><p class="lab">{esc(x.get("label"))}</p><p>{esc(x.get("text"))}</p></div>' + ('<span class="arrow">→</span>' if i < len(g('steps')) - 1 else '') for i, x in enumerate(g('steps') or []))
        body = f'{pill(g("pill") or "HOW IT WORKS")}<h1>{esc(g("headline"))}</h1><p class="sub left">{esc(g("sub"))}</p><div class="steps">{it}</div><p class="kicker">{esc(g("footer"))}</p>'
    elif L == 'three-things':
        it = ''.join(f'<div class="row"><span class="num">{i + 1:02d}</span><div><b>{esc(x.get("title"))}</b><p class="small">{esc(x.get("text"))}</p></div></div>' for i, x in enumerate(g('items') or []))
        body = f'<h1>{esc(g("headline") or "Three things to do this week.")}</h1><div class="rows">{it}</div>'
    elif L == 'next-session':
        body = f'<div class="center">{pill(g("pill") or "ONE MORE THING")}<h2>{esc(g("line1"))}</h2><h1 class="xl"><em>{esc(g("line2"))}</em></h1><p class="sub">{esc(g("body"))}</p><span class="btn ghost">{esc(g("cta") or "Link to register in chat")}</span></div>'
    elif L == 'close-cta':
        ln = ''.join(f'<p class="body">{esc(x)}</p>' for x in g('lines') or [])
        body = f'<div class="center"><h1 class="xl"><em>{esc(g("title") or "Know and Grow Your Membership")}</em></h1>{ln}<span class="btn">{esc(g("cta") or "Schedule a call — link in chat")}</span></div>'
    elif L == 'quote':
        body = f'<div class="center"><p class="quote">“{esc(g("quote"))}”</p><p class="sub">{esc(g("who"))}</p></div>'
    else:
        raise SystemExit(f'Unknown layout {L!r}. Layouts: {", ".join(LAYOUTS)}')
    return f'<section class="slide L-{L}"><img class="logo" src="{logo_path().as_uri()}">{body}</section>'

CSS = f"""
@font-face {{ font-family: 'DM Sans'; src: local('DM Sans'), local('DMSans-Regular'); }}
@page {{ size: 1920px 1080px; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ width: 1920px; }}
body {{ font-family: 'DM Sans', sans-serif; color: #{INK}; background: #{CREAM}; }}
.slide {{ width: 1920px; height: 1079px; break-inside: avoid; break-after: page; padding: 110px 120px; position: relative; overflow: hidden; background: #{CREAM}; display: flex; flex-direction: column; }}
.logo {{ position: absolute; top: 48px; right: 56px; width: 64px; }}
h1 {{ font-size: 64px; line-height: 1.08; letter-spacing: -0.02em; font-weight: 700; margin: 18px 0 10px; text-wrap: balance; }}
h1.xl {{ font-size: 96px; }} h2 {{ font-size: 44px; font-weight: 600; margin-top: 24px; }}
h3 {{ font-size: 28px; margin-bottom: 8px; }}
em {{ font-style: normal; color: #{ORANGE}; }}
.pill {{ align-self: flex-start; background: linear-gradient(90deg, #{ORANGE}, #{YELLOW}); color: #fff; font-size: 20px; font-weight: 700; letter-spacing: .08em; padding: 8px 22px; border-radius: 999px; text-transform: uppercase; }}
.center {{ margin: auto; text-align: center; display: flex; flex-direction: column; align-items: center; }} .center .pill {{ align-self: center; }}
.sub {{ font-size: 32px; color: #{MUTED}; margin-top: 8px; }} .sub.left {{ text-align: left; }}
.tag {{ font-size: 34px; font-weight: 700; color: #{ORANGE}; margin-top: 90px; border-bottom: 2px solid #{YELLOW}55; }} .tag.left {{ margin-top: auto; align-self: flex-start; }}
.body {{ font-size: 28px; line-height: 1.5; color: #{INK}; max-width: 1300px; }}
.small {{ font-size: 22px; color: #{MUTED}; margin-top: 6px; }}
.kicker {{ margin-top: auto; font-size: 26px; font-weight: 600; color: #{ORANGE_INK}; }}
.eyebrow {{ font-size: 20px; letter-spacing: .14em; color: #{MUTED}; text-transform: uppercase; }}
hr {{ border: 0; border-top: 2px solid #{LINE}; margin: 24px 0; }} hr.short {{ width: 120px; border-top: 4px solid #{ORANGE}; }}
.vmid {{ margin: auto 0; }}
.host {{ display: flex; gap: 90px; align-items: center; margin: auto 0; }}
.photo {{ width: 520px; height: 620px; object-fit: cover; border-radius: 24px; box-shadow: 0 24px 60px rgb(120 110 95 / .25); }} .ph {{ background: #{LINE}; }}
.role {{ font-size: 32px; font-weight: 600; color: #{ORANGE}; margin-bottom: 26px; }}
ul {{ padding: 0; list-style: none; }} .dots li, .dash li {{ font-size: 24px; margin: 14px 0; padding-left: 30px; position: relative; }}
.dots li::before {{ content: ''; position: absolute; left: 4px; top: 11px; width: 10px; height: 10px; border-radius: 50%; background: #{ORANGE}; }}
.dash li::before {{ content: '—'; position: absolute; left: 0; color: #{ORANGE}; }}
.pillars {{ display: flex; justify-content: space-around; margin-top: 50px; }}
.pillar {{ text-align: center; width: 380px; display: flex; flex-direction: column; align-items: center; gap: 12px; font-size: 22px; color: #{MUTED}; }}
.pillar b {{ color: #{INK}; letter-spacing: .14em; font-size: 24px; }} .ico {{ width: 84px; height: 84px; border-radius: 50%; background: #{YELLOW}; }}
.rows {{ margin-top: 60px; }} .row {{ display: flex; gap: 48px; align-items: baseline; padding: 26px 0; border-bottom: 2px solid #{LINE}; font-size: 32px; }}
.num {{ font-size: 52px; font-weight: 700; color: #{ORANGE}; min-width: 90px; }} .row b {{ font-size: 32px; }}
.foot {{ margin-top: auto; font-size: 20px; letter-spacing: .16em; color: #{MUTED}; }}
.items {{ margin-top: 50px; display: grid; gap: 22px; }} .item {{ background: #{CARD}; border: 2px solid #{LINE}; border-radius: 18px; padding: 26px 32px; font-size: 28px; display: flex; gap: 22px; align-items: center; }}
.item i {{ font-style: normal; width: 44px; height: 44px; border-radius: 50%; background: #{ORANGE}; color: #fff; display: grid; place-items: center; font-weight: 700; flex: none; }}
.cards {{ display: grid; gap: 30px; margin-top: 46px; }} .cards.n2 {{ grid-template-columns: 1fr 1fr; }} .cards.n3 {{ grid-template-columns: repeat(3, 1fr); }} .cards.n4 {{ grid-template-columns: repeat(4, 1fr); }}
.card {{ background: #{CARD}; border: 2px solid #{LINE}; border-radius: 18px; padding: 34px; font-size: 24px; line-height: 1.45; box-shadow: 0 10px 30px rgb(120 110 95 / .10); }}
.lab {{ font-size: 18px; font-weight: 700; letter-spacing: .12em; color: #{ORANGE}; text-transform: uppercase; margin: 0 0 12px; }}
.cs {{ display: grid; grid-template-columns: 1.3fr 1fr; gap: 60px; margin-top: 40px; font-size: 26px; line-height: 1.45; }} .cs p {{ margin-bottom: 18px; }}
.statbox {{ background: #{CARD}; border: 2px solid #{LINE}; border-radius: 18px; padding: 40px; display: flex; flex-direction: column; gap: 10px; }}
.stat {{ font-size: 110px; color: #{ORANGE}; line-height: 1; }} .statbox > span {{ font-size: 24px; color: #{MUTED}; margin-bottom: 20px; }}
.m {{ display: flex; justify-content: space-between; border-top: 2px solid #{LINE}; padding-top: 12px; font-size: 22px; }}
.shot {{ max-height: 620px; max-width: 100%; margin: 30px auto 0; border-radius: 16px; box-shadow: 0 20px 50px rgb(120 110 95 / .2); }} .shot.ph {{ width: 1100px; height: 560px; display: grid; place-items: center; color: #{MUTED}; }}
.caption {{ text-align: center; font-size: 22px; color: #{MUTED}; margin-top: 18px; }}
.bars {{ margin: 50px 0 30px; display: grid; gap: 22px; }} .bar {{ display: flex; align-items: center; gap: 24px; font-size: 26px; }}
.bar span {{ width: 420px; }} .bar i {{ height: 34px; border-radius: 17px; background: linear-gradient(90deg, #{ORANGE}, #{YELLOW}); }} .bar b {{ font-size: 26px; }}
.steps {{ display: flex; align-items: stretch; gap: 18px; margin-top: 60px; }} .steps .card {{ flex: 1; }} .arrow {{ align-self: center; font-size: 40px; color: #{ORANGE}; }}
.btn {{ margin-top: 50px; background: linear-gradient(90deg, #{ORANGE}, #{YELLOW}); color: #fff; font-weight: 700; font-size: 26px; padding: 20px 46px; border-radius: 999px; }} .btn.ghost {{ background: #{CARD}; color: #{INK}; border: 2px solid #{LINE}; }}
.quote {{ font-size: 60px; line-height: 1.25; font-weight: 600; max-width: 1500px; }}
"""

def render_pdf(spec, out, base):
    doc = '<!doctype html><html><head><meta charset="utf-8"><style>' + CSS + '</style></head><body>' + ''.join(slide_html(s, base) for s in spec['slides']) + '</body></html>'
    tmp = Path(tempfile.mkdtemp()) / 'deck.html'; tmp.write_text(doc)
    shutil.copy(tmp, out.with_suffix('.html'))
    chrome = find_chrome()
    if not chrome:
        print('No Chrome/Chromium found: wrote the HTML only (set CHROME=/path/to/chrome, or pip install playwright && playwright install chromium).'); return
    subprocess.run([chrome, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={out.with_suffix(".pdf")}', tmp.as_uri()], check=True, capture_output=True)

# ---------------------------------------------------------------- PPTX (editable, native text)
def render_pptx(spec, out, base):
    from pptx import Presentation
    from pptx.util import Emu, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    PX = 6350  # EMU per px at 1920 wide = 13.333 in
    prs = Presentation(); prs.slide_width, prs.slide_height = Emu(1920 * PX), Emu(1080 * PX)
    blank = prs.slide_layouts[6]
    rgb = lambda h: RGBColor.from_string(h)

    def box(sl, x, y, w, h, text, size=28, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
        if not text: return None
        tb = sl.shapes.add_textbox(Emu(x * PX), Emu(y * PX), Emu(w * PX), Emu(h * PX)); tf = tb.text_frame
        tf.word_wrap = True; tf.vertical_anchor = anchor
        for k, para in enumerate(str(text).split('\n')):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph(); p.alignment = align
            for j, part in enumerate(re.split(r'\*(.+?)\*', para)):  # odd parts were *accented*
                if not part: continue
                r = p.add_run(); r.text = part; f = r.font; f.name = 'DM Sans'; f.size = Pt(size * .75); f.bold = bold
                f.color.rgb = rgb(ORANGE if j % 2 else color)
        return tb

    def pill_shape(sl, x, y, text, center=False):
        if not text: return
        w = 34 + len(text) * 13
        if center: x = 960 - w / 2
        sh = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(int(x * PX)), Emu(y * PX), Emu(int(w * PX)), Emu(46 * PX))
        sh.adjustments[0] = 0.5; sh.line.fill.background()
        sh.fill.gradient(); sh.fill.gradient_angle = 0
        st = sh.fill.gradient_stops; st[0].color.rgb = rgb(ORANGE); st[1].color.rgb = rgb(YELLOW)
        tf = sh.text_frame; tf.margin_top = tf.margin_bottom = 0; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = text.upper(); r.font.name = 'DM Sans'; r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = rgb('FFFFFF')

    def card(sl, x, y, w, h):
        sh = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(x * PX), Emu(y * PX), Emu(w * PX), Emu(h * PX))
        sh.adjustments[0] = 0.08; sh.fill.solid(); sh.fill.fore_color.rgb = rgb(CARD); sh.line.color.rgb = rgb(LINE); sh.shadow.inherit = False
        return sh

    for s in spec['slides']:
        sl = prs.slides.add_slide(blank); g = s.get; L = s['layout']
        bg = sl.background.fill; bg.solid(); bg.fore_color.rgb = rgb(CREAM)
        sl.shapes.add_picture(str(logo_path()), Emu(1800 * PX), Emu(48 * PX), width=Emu(64 * PX))
        C = PP_ALIGN.CENTER
        if L == 'cover':
            pill_shape(sl, 0, 330, g('eyebrow'), True); box(sl, 160, 400, 1600, 140, g('title'), 96, True, align=C)
            box(sl, 160, 560, 1600, 60, g('subtitle'), 32, color=MUTED, align=C); box(sl, 160, 720, 1600, 60, g('tagline') or 'Know and Grow Your Membership', 34, True, ORANGE, C)
        elif L == 'host':
            if g('photo'): sl.shapes.add_picture(str(base / g('photo')), Emu(120 * PX), Emu(230 * PX), height=Emu(620 * PX))
            else: card(sl, 120, 230, 520, 620)
            pill_shape(sl, 730, 300, g('pill') or 'YOUR HOST'); box(sl, 730, 370, 1050, 90, g('name'), 64, True)
            box(sl, 730, 470, 1050, 50, g('role'), 32, True, ORANGE); box(sl, 730, 540, 1050, 160, g('blurb'), 28)
            box(sl, 730, 720, 1050, 160, '\n'.join('•  ' + b for b in g('bullets') or []), 24)
        elif L == 'about':
            pill_shape(sl, 120, 150, g('pill') or 'ABOUT US'); box(sl, 120, 220, 1500, 170, g('headline'), 64, True)
            box(sl, 120, 420, 1500, 110, '\n'.join('—  ' + x for x in g('lines') or []), 24, color=MUTED)
            ps = g('pillars') or []
            for i, p in enumerate(ps):
                x = 120 + i * (1680 // max(len(ps), 1))
                box(sl, x, 600, 1680 // max(len(ps), 1) - 40, 50, p.get('label'), 24, True, align=C)
                box(sl, x, 660, 1680 // max(len(ps), 1) - 40, 90, p.get('text'), 22, color=MUTED, align=C)
            box(sl, 120, 900, 1200, 60, g('tagline'), 34, True, ORANGE)
        elif L in ('agenda', 'three-things'):
            box(sl, 120, 130, 1600, 100, g('title') or g('headline') or ('What we’re covering today' if L == 'agenda' else 'Three things to do this week.'), 64, True)
            for i, it in enumerate(g('items') or []):
                y = 300 + i * 130; box(sl, 120, y, 110, 80, f'{i + 1:02d}', 52, True, ORANGE)
                if isinstance(it, dict): box(sl, 260, y, 1500, 50, it.get('title'), 32, True); box(sl, 260, y + 50, 1500, 60, it.get('text'), 22, color=MUTED)
                else: box(sl, 260, y + 10, 1500, 70, it, 32)
            if L == 'agenda': box(sl, 120, 960, 1200, 40, g('footer') or '30 MINUTES  |  Q&A AT THE END', 20, color=MUTED)
        elif L in ('poll', 'section', 'framework', 'qa', 'quote'):
            pill_shape(sl, 0, 360, g('pill') or {'poll': 'QUICK POLL'}.get(L, ''), True)
            box(sl, 160, 430, 1600, 220, g('question') or g('headline') or (('“' + g('quote') + '”') if g('quote') else 'Questions?'), 60 if L == 'quote' else 88, True, align=C, anchor=MSO_ANCHOR.MIDDLE)
            box(sl, 160, 680, 1600, 80, g('sub') or g('who'), 32, color=MUTED, align=C)
        elif L == 'reframe':
            box(sl, 120, 330, 1600, 40, g('eyebrow'), 20, color=MUTED); box(sl, 120, 380, 1680, 220, (g('line1') or '') + '\n*' + (g('line2') or '') + '*', 64, True)
            box(sl, 120, 640, 1400, 120, g('body'), 28); box(sl, 120, 940, 1680, 60, g('kicker'), 26, True, ORANGE_INK)
        elif L == 'problem-list':
            pill_shape(sl, 120, 130, g('pill')); box(sl, 120, 190, 1680, 100, g('headline'), 64, True)
            for i, it in enumerate(g('items') or []):
                y = 340 + i * 130; card(sl, 120, y, 1680, 100); box(sl, 170, y + 22, 1600, 60, f'{i + 1}.  {it}', 28)
            box(sl, 120, 940, 1680, 60, g('kicker'), 26, True, ORANGE_INK)
        elif L in ('cards', 'steps'):
            pill_shape(sl, 120, 130, g('pill') or ('HOW IT WORKS' if L == 'steps' else '')); box(sl, 120, 190, 1680, 100, g('headline'), 64, True)
            box(sl, 120, 300, 1680, 50, g('sub'), 30, color=MUTED)
            cs = g('cards') or g('steps') or []; n = max(len(cs), 1); w = (1680 - 30 * (n - 1)) // n
            for i, c in enumerate(cs):
                x = 120 + i * (w + 30); card(sl, x, 400, w, 400)
                box(sl, x + 30, 430, w - 60, 40, c.get('label'), 18, True, ORANGE)
                box(sl, x + 30, 480, w - 60, 60, c.get('title'), 28, True); box(sl, x + 30, 540 if c.get('title') else 490, w - 60, 280, c.get('text'), 24)
            box(sl, 120, 940, 1680, 60, g('kicker') or g('footer'), 26, True, ORANGE_INK)
        elif L == 'case-study':
            pill_shape(sl, 120, 130, g('pill') or 'IN PRACTICE'); box(sl, 120, 190, 1100, 90, g('client'), 64, True); box(sl, 120, 290, 1100, 50, g('sub'), 30, color=MUTED)
            box(sl, 120, 380, 950, 40, 'THE CHALLENGE', 18, True, ORANGE); box(sl, 120, 420, 950, 180, g('challenge'), 26)
            box(sl, 120, 620, 950, 40, 'THE APPROACH', 18, True, ORANGE); box(sl, 120, 660, 950, 200, g('approach'), 26)
            card(sl, 1160, 380, 640, 520); box(sl, 1200, 410, 560, 140, g('stat'), 96, True, ORANGE); box(sl, 1200, 560, 560, 50, g('stat_label'), 24, color=MUTED)
            box(sl, 1200, 640, 560, 240, '\n'.join(f'{m.get("label")}:  {m.get("value")}' for m in g('metrics') or []), 22)
        elif L == 'image':
            pill_shape(sl, 120, 130, g('pill')); box(sl, 120, 190, 1680, 100, g('headline'), 64, True); box(sl, 120, 290, 1680, 50, g('sub'), 30, color=MUTED)
            if g('image'): sl.shapes.add_picture(str(base / g('image')), Emu(360 * PX), Emu(370 * PX), height=Emu(560 * PX))
            else: card(sl, 410, 370, 1100, 560)
            box(sl, 120, 960, 1680, 40, g('caption'), 22, color=MUTED, align=C)
        elif L == 'bar-answers':
            pill_shape(sl, 120, 130, g('pill')); box(sl, 120, 190, 1680, 100, g('headline'), 64, True)
            bars = g('bars') or []; mx = max([b.get('value', 0) for b in bars] or [1]) or 1
            for i, b in enumerate(bars):
                y = 340 + i * 70; box(sl, 120, y, 420, 50, b.get('label'), 26)
                sh = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(560 * PX), Emu((y + 8) * PX), Emu(max(int(1000 * b.get('value', 0) / mx), 8) * PX), Emu(34 * PX))
                sh.adjustments[0] = 0.5; sh.line.fill.background(); sh.fill.solid(); sh.fill.fore_color.rgb = rgb(ORANGE)
                box(sl, 1600, y, 200, 50, str(b.get('value')), 26, True)
            box(sl, 120, 360 + len(bars) * 70, 1680, 200, '\n'.join(g('lines') or []), 22, color=MUTED); box(sl, 120, 940, 1680, 60, g('kicker'), 26, True, ORANGE_INK)
        elif L == 'next-session':
            pill_shape(sl, 0, 300, g('pill') or 'ONE MORE THING', True); box(sl, 160, 370, 1600, 70, g('line1'), 44, True, align=C)
            box(sl, 160, 450, 1600, 140, '*' + (g('line2') or '') + '*', 88, True, align=C); box(sl, 260, 610, 1400, 120, g('body'), 30, color=MUTED, align=C)
            box(sl, 160, 760, 1600, 50, g('cta') or 'Link to register in chat', 26, True, align=C)
        elif L == 'close-cta':
            box(sl, 160, 300, 1600, 140, '*' + (g('title') or 'Know and Grow Your Membership') + '*', 88, True, align=C)
            box(sl, 260, 470, 1400, 260, '\n'.join(g('lines') or []), 28, align=C); box(sl, 160, 780, 1600, 60, g('cta') or 'Schedule a call — link in chat', 28, True, ORANGE, C)
        else:
            raise SystemExit(f'Unknown layout {L!r}')
        if g('notes'): sl.notes_slide.notes_text_frame.text = g('notes')
    prs.save(out.with_suffix('.pptx'))

def main():
    a = sys.argv[1:]
    if not a: raise SystemExit(__doc__)
    src = Path(a[0]); spec = json.loads(src.read_text())
    outdir = Path(a[a.index('--out') + 1]) if '--out' in a else src.parent; outdir.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(spec['slides']):
        if s.get('layout') not in LAYOUTS: raise SystemExit(f'Slide {i + 1}: unknown layout {s.get("layout")!r}')
    out = outdir / (re.sub(r'[^a-z0-9]+', '-', spec.get('title', 'deck').lower()).strip('-') or 'deck')
    if '--no-pptx' not in a: render_pptx(spec, out, src.parent)
    if '--no-pdf' not in a: render_pdf(spec, out, src.parent)
    print('wrote', ', '.join(str(out.with_suffix(x)) for x in (['.pptx'] if '--no-pptx' not in a else []) + (['.pdf'] if '--no-pdf' not in a else [])))

if __name__ == '__main__':
    main()
