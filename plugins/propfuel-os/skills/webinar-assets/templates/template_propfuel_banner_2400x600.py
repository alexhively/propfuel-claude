"""
PropFuel Webinar — Platform Banner Template
============================================
Size: 2400×600 | PropFuel platform full-width

USAGE: Edit the CONFIG section below, then run.
This template has: vertical orange gradient left bar, "WATCH THE RECORDING"
header, "Webinar Replay" button (bottom right).
"""

# ============================================================
# CONFIG — Edit these for each webinar
# ============================================================

TITLE = "Onboarding Campaigns That Keep Members Engaged"
TITLE_FONT_SIZE = 110      # 110 default for this size
HEADER_TEXT = "WATCH THE RECORDING"
BUTTON_TEXT = "Webinar Replay"
OUTPUT_FILE = "propfuel_banner.jpg"

# ============================================================
# DO NOT EDIT BELOW — Template engine
# ============================================================

from PIL import Image, ImageDraw, ImageFont
import os, math, random

WIDTH, HEIGHT = 2400, 600
CHARCOAL = (47, 47, 47)
GOLDEN = (251, 192, 45)
DEEP_ORANGE = (240, 90, 40)
PAGE_BG = (244, 241, 234)
FONT_PATH = "/root/.local/share/fonts/DMSans.ttf"
LOGO_PATH = "propfuel_logo.png"


def load_font(s, w=700):
    f = ImageFont.truetype(FONT_PATH, s)
    try: f.set_variation_by_axes([min(40, max(9, s)), w])
    except: pass
    return f


def gen_paper(w, h, seed=44):
    random.seed(seed)
    c = Image.new('RGB', (w, h), PAGE_BG); px = c.load()
    for y in range(h):
        for x in range(w):
            n = random.randint(-8, 8)
            px[x, y] = (max(0, min(255, PAGE_BG[0]+n)), max(0, min(255, PAGE_BG[1]+n)), max(0, min(255, PAGE_BG[2]+n-2)))
    bl = Image.new('RGBA', (w, h), (0, 0, 0, 0)); bd = ImageDraw.Draw(bl)
    for _ in range(600):
        cx2, cy2 = random.randint(0, w), random.randint(0, h); r = random.randint(10, 60)
        bd.ellipse([cx2-r, cy2-r, cx2+r, cy2+r], fill=(*random.choice([(235,228,215),(250,246,238)]), int(255*0.015)))
    return Image.alpha_composite(c.convert('RGBA'), bl).convert('RGB')


def wrap_text(draw, text, font, mw):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = f"{cur} {w}".strip()
        if draw.textbbox((0,0), t, font=font)[2] <= mw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def draw_orange_btn(canvas, btn_x, btn_y, bw, bh):
    rad = bh // 2; W, H = canvas.size
    for sy in range(bh+40):
        for sx in range(bw+40):
            pr, prr = sx-20, sy-16
            cc = max(rad, min(bw-rad, pr)); cyc = max(rad, min(bh-rad, prr))
            dx, dy = pr-cc, prr-cyc; dist = math.sqrt(dx*dx+dy*dy)
            if dist <= rad: continue
            sd = dist-rad
            if sd < 14:
                a = max(0, (14-sd)/14)*0.13
                scx, scy = btn_x-20+sx, btn_y-16+sy+3
                if 0 <= scx < W and 0 <= scy < H:
                    ex = canvas.getpixel((scx, scy))
                    canvas.putpixel((scx, scy), tuple(int(ex[i]*(1-a)+[200,120,50][i]*a) for i in range(3)))
    for by3 in range(bh):
        for bx in range(bw):
            hp = bx/max(bw-1, 1)
            cr = int(DEEP_ORANGE[0]+(GOLDEN[0]-DEEP_ORANGE[0])*hp)
            cg = int(DEEP_ORANGE[1]+(GOLDEN[1]-DEEP_ORANGE[1])*hp)
            cb = int(DEEP_ORANGE[2]+(GOLDEN[2]-DEEP_ORANGE[2])*hp)
            ins = False
            if rad <= bx <= bw-rad: ins = True
            elif bx < rad:
                d2 = by3-rad if by3 < rad else by3-(bh-rad) if by3 > bh-rad else 0; d1 = rad-bx
                if rad <= by3 <= bh-rad: ins = True
                elif d1*d1+d2*d2 <= rad*rad: ins = True
            elif bx > bw-rad:
                d2 = by3-rad if by3 < rad else by3-(bh-rad) if by3 > bh-rad else 0; d1 = bx-(bw-rad)
                if rad <= by3 <= bh-rad: ins = True
                elif d1*d1+d2*d2 <= rad*rad: ins = True
            if ins:
                scx, scy = btn_x+bx, btn_y+by3
                if 0 <= scx < W and 0 <= scy < H: canvas.putpixel((scx, scy), (cr, cg, cb))


def build():
    canvas = gen_paper(WIDTH, HEIGHT); draw = ImageDraw.Draw(canvas)

    # Left gradient bar (vertical: golden top → deep orange bottom)
    for x in range(14):
        for y in range(HEIGHT):
            vp = y / max(HEIGHT-1, 1)
            canvas.putpixel((x, y), (
                int(GOLDEN[0]+(DEEP_ORANGE[0]-GOLDEN[0])*vp),
                int(GOLDEN[1]+(DEEP_ORANGE[1]-GOLDEN[1])*vp),
                int(GOLDEN[2]+(DEEP_ORANGE[2]-GOLDEN[2])*vp),
            ))

    draw = ImageDraw.Draw(canvas)
    lm = 88

    # Logo
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo_h = 150; logo = logo.resize((int(logo.width*logo_h/logo.height), logo_h), Image.LANCZOS)
    la = logo.load()
    for ly in range(logo.height):
        for lx in range(logo.width):
            r, g, b, a = la[lx, ly]
            if r > 218 and g > 213 and b > 208: la[lx, ly] = (r, g, b, 0)
    canvas.paste(logo, (WIDTH-logo.width-60, 30), logo)
    draw = ImageDraw.Draw(canvas)

    # Header
    fl = load_font(34, 600)
    draw.text((lm, 40), HEADER_TEXT, fill=CHARCOAL, font=fl)
    lb = draw.textbbox((lm, 40), HEADER_TEXT, font=fl)

    # Title
    ft = load_font(TITLE_FONT_SIZE, 800)
    tmp = Image.new('RGB', (1, 1)); td = ImageDraw.Draw(tmp)
    lines = wrap_text(td, TITLE, ft, WIDTH-lm-550)
    lhs = [td.textbbox((0,0), l, font=ft)[3]-td.textbbox((0,0), l, font=ft)[1] for l in lines]
    ls = 10; title_h = sum(lhs)+ls*(len(lines)-1)

    ct = lb[3]+14; cb = HEIGHT-16
    ty = ct+(cb-ct-title_h)//2-20

    yc = ty
    for i, l in enumerate(lines):
        draw.text((lm, yc), l, fill=CHARCOAL, font=ft); yc += lhs[i]+ls

    # Button — bottom right
    fb = load_font(42, 700); bbb = td.textbbox((0,0), BUTTON_TEXT, font=fb)
    btw, bth = bbb[2]-bbb[0], bbb[3]-bbb[1]
    bpx, bpy, bisp = 48, 26, 52; bw = btw+bisp+bpx*2; bh = bth+bpy*2

    btn_x = WIDTH-60-bw; btn_y = HEIGHT-90-bh
    draw_orange_btn(canvas, btn_x, btn_y, bw, bh)
    draw = ImageDraw.Draw(canvas)
    tx = btn_x+bpx+4; tcy = btn_y+bh//2
    draw.polygon([(tx, tcy-14), (tx, tcy+14), (tx+20, tcy)], fill=(255, 255, 255))
    draw.text((btn_x+bpx+bisp, btn_y+(bh-bth)//2-bbb[1]), BUTTON_TEXT, fill=(255, 255, 255), font=fb)

    canvas.save(OUTPUT_FILE, "JPEG", quality=92)
    print(f"✓ {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE)/1024:.0f} KB)")


if __name__ == "__main__":
    build()
