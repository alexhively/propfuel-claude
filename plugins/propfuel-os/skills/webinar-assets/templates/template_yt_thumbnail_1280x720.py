"""
PropFuel Webinar — YouTube Thumbnail Template
==============================================
Size: 1280×720 | YouTube standard

USAGE: Edit the CONFIG section below, then run.
For Membership AI webinars, set USE_BLUE_GRADIENT = True.
"""

# ============================================================
# CONFIG — Edit these for each webinar
# ============================================================

TITLE = "Onboarding Campaigns That Keep Members Engaged"
DATE = "June 17, 2026"
SPEAKER = "Brittany Lancor"
USE_BLUE_GRADIENT = False  # True for Membership AI webinars (blue steel title)
TITLE_FONT_SIZE = 84       # 84 default; increase for shorter titles, decrease for longer
BUTTON_TEXT = "Watch Now"
OUTPUT_FILE = "yt_thumbnail.jpg"

# ============================================================
# DO NOT EDIT BELOW — Template engine
# ============================================================

from PIL import Image, ImageDraw, ImageFont
import os, math, random

WIDTH, HEIGHT = 1280, 720
CHARCOAL = (47, 47, 47)
GOLDEN = (251, 192, 45)
DEEP_ORANGE = (240, 90, 40)
PAGE_BG = (244, 241, 234)
MID_GREY = (110, 110, 110)
AI_DARK_EDGE = (31, 58, 81)
AI_SHADOW = (53, 96, 126)
AI_PRIMARY = (74, 127, 165)
FONT_PATH = "/root/.local/share/fonts/DMSans.ttf"
LOGO_PATH = "propfuel_logo.png"  # extracted from webinar template image


def load_font(s, w=700):
    f = ImageFont.truetype(FONT_PATH, s)
    try:
        f.set_variation_by_axes([min(40, max(9, s)), w])
    except:
        pass
    return f


def gen_paper(w, h, seed=42):
    random.seed(seed)
    c = Image.new('RGB', (w, h), PAGE_BG)
    px = c.load()
    for y in range(h):
        for x in range(w):
            n = random.randint(-8, 8)
            px[x, y] = (
                max(0, min(255, PAGE_BG[0] + n)),
                max(0, min(255, PAGE_BG[1] + n)),
                max(0, min(255, PAGE_BG[2] + n - 2)),
            )
    bl = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bl)
    for _ in range(400):
        cx2, cy2 = random.randint(0, w), random.randint(0, h)
        r = random.randint(10, 70)
        col = random.choice([(235, 228, 215), (250, 246, 238)])
        bd.ellipse([cx2 - r, cy2 - r, cx2 + r, cy2 + r], fill=(*col, int(255 * 0.015)))
    return Image.alpha_composite(c.convert('RGBA'), bl).convert('RGB')


def wrap_text(draw, text, font, mw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if draw.textbbox((0, 0), t, font=font)[2] <= mw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def ai_grad_text(canvas, text, font, x, y):
    """Render text with blue steel gradient (Membership AI only)."""
    draw = ImageDraw.Draw(canvas)
    bb = draw.textbbox((x, y), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    grad = Image.new('RGB', (tw + 20, th + 20))
    gp = grad.load()
    for gy in range(grad.height):
        p = gy / max(grad.height - 1, 1)
        if p < 0.45:
            t = p / 0.45
            c = tuple(int(AI_SHADOW[i] + (AI_PRIMARY[i] - AI_SHADOW[i]) * t) for i in range(3))
        else:
            t = (p - 0.45) / 0.55
            c = tuple(int(AI_PRIMARY[i] + (AI_DARK_EDGE[i] - AI_PRIMARY[i]) * t) for i in range(3))
        for gx in range(grad.width):
            gp[gx, gy] = c
    mask = Image.new('L', (tw + 20, th + 20), 0)
    ImageDraw.Draw(mask).text((x - bb[0] + 10, y - bb[1] + 10), text, fill=255, font=font)
    canvas.paste(grad, (bb[0] - 10, bb[1] - 10), mask)
    return bb


def draw_orange_btn(canvas, btn_x, btn_y, bw, bh):
    """Draw orange gradient pill button with shadow."""
    rad = bh // 2
    W, H = canvas.size
    for sy in range(bh + 40):
        for sx in range(bw + 40):
            pr, prr = sx - 20, sy - 16
            cc = max(rad, min(bw - rad, pr))
            cyc = max(rad, min(bh - rad, prr))
            dx, dy = pr - cc, prr - cyc
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= rad:
                continue
            sd = dist - rad
            if sd < 16:
                a = max(0, (16 - sd) / 16) * 0.15
                scx, scy = btn_x - 20 + sx, btn_y - 16 + sy + 4
                if 0 <= scx < W and 0 <= scy < H:
                    ex = canvas.getpixel((scx, scy))
                    canvas.putpixel((scx, scy), tuple(int(ex[i] * (1 - a) + [200, 120, 50][i] * a) for i in range(3)))
    for by3 in range(bh):
        for bx in range(bw):
            hp = bx / max(bw - 1, 1)
            cr = int(DEEP_ORANGE[0] + (GOLDEN[0] - DEEP_ORANGE[0]) * hp)
            cg = int(DEEP_ORANGE[1] + (GOLDEN[1] - DEEP_ORANGE[1]) * hp)
            cb = int(DEEP_ORANGE[2] + (GOLDEN[2] - DEEP_ORANGE[2]) * hp)
            ins = False
            if rad <= bx <= bw - rad:
                ins = True
            elif bx < rad:
                d2 = by3 - rad if by3 < rad else by3 - (bh - rad) if by3 > bh - rad else 0
                d1 = rad - bx
                if rad <= by3 <= bh - rad:
                    ins = True
                elif d1 * d1 + d2 * d2 <= rad * rad:
                    ins = True
            elif bx > bw - rad:
                d2 = by3 - rad if by3 < rad else by3 - (bh - rad) if by3 > bh - rad else 0
                d1 = bx - (bw - rad)
                if rad <= by3 <= bh - rad:
                    ins = True
                elif d1 * d1 + d2 * d2 <= rad * rad:
                    ins = True
            if ins:
                scx, scy = btn_x + bx, btn_y + by3
                if 0 <= scx < W and 0 <= scy < H:
                    canvas.putpixel((scx, scy), (cr, cg, cb))


def build():
    canvas = gen_paper(WIDTH, HEIGHT)
    draw = ImageDraw.Draw(canvas)

    # Horizontal gradient top bar
    for y in range(14):
        for x in range(WIDTH):
            p = x / max(WIDTH - 1, 1)
            canvas.putpixel((x, y), (
                int(DEEP_ORANGE[0] + (GOLDEN[0] - DEEP_ORANGE[0]) * p),
                int(DEEP_ORANGE[1] + (GOLDEN[1] - DEEP_ORANGE[1]) * p),
                int(DEEP_ORANGE[2] + (GOLDEN[2] - DEEP_ORANGE[2]) * p),
            ))

    lm = 72

    # Logo
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo_h = 92
    logo = logo.resize((int(logo.width * logo_h / logo.height), logo_h), Image.LANCZOS)
    la = logo.load()
    for ly in range(logo.height):
        for lx in range(logo.width):
            r, g, b, a = la[lx, ly]
            if r > 218 and g > 213 and b > 208:
                la[lx, ly] = (r, g, b, 0)
    logo_x = WIDTH - logo.width - 44
    canvas.paste(logo, (logo_x, 34), logo)
    draw = ImageDraw.Draw(canvas)

    # Header
    fl = load_font(28, 700)
    fi = load_font(19, 500)
    draw.text((lm, 36), "WEBINAR REPLAY", fill=CHARCOAL, font=fl)
    lb = draw.textbbox((lm, 36), "WEBINAR REPLAY", font=fl)
    draw.text((lm, lb[3] + 6), f"{DATE}  ·  {SPEAKER}", fill=MID_GREY, font=fi)
    ibb = draw.textbbox((lm, lb[3] + 6), f"{DATE}  ·  {SPEAKER}", font=fi)
    div_y = ibb[3] + 14
    draw.line([(lm, div_y), (logo_x - 40, div_y)], fill=(227, 221, 210), width=1)

    # Title
    ft = load_font(TITLE_FONT_SIZE, 800)
    tmp = Image.new('RGB', (1, 1))
    td = ImageDraw.Draw(tmp)
    lines = wrap_text(td, TITLE, ft, WIDTH - lm * 2)
    lhs = [td.textbbox((0, 0), l, font=ft)[3] - td.textbbox((0, 0), l, font=ft)[1] for l in lines]
    ls = 10
    title_h = sum(lhs) + ls * (len(lines) - 1)

    # Button measurements
    fb = load_font(28, 700)
    bbb = td.textbbox((0, 0), BUTTON_TEXT, font=fb)
    btw, bth = bbb[2] - bbb[0], bbb[3] - bbb[1]
    bpx, bpy, bisp = 36, 20, 40
    bw = btw + bisp + bpx * 2
    bh = bth + bpy * 2

    # Center title+button block
    gap = 65
    total_block = title_h + gap + bh
    ct = div_y + 10
    cb = HEIGHT - 10
    bs = ct + (cb - ct - total_block) // 2 - 12

    # Draw title lines
    yc = bs
    for i, l in enumerate(lines):
        if USE_BLUE_GRADIENT:
            ai_grad_text(canvas, l, ft, lm, yc)
            draw = ImageDraw.Draw(canvas)
        else:
            draw.text((lm, yc), l, fill=CHARCOAL, font=ft)
        yc += lhs[i] + ls

    # Button
    btn_y = bs + title_h + gap
    draw_orange_btn(canvas, lm, btn_y, bw, bh)
    draw = ImageDraw.Draw(canvas)
    tx = lm + bpx + 2
    tcy = btn_y + bh // 2
    draw.polygon([(tx, tcy - 11), (tx, tcy + 11), (tx + 16, tcy)], fill=(255, 255, 255))
    draw.text((lm + bpx + bisp - 4, btn_y + (bh - bth) // 2 - bbb[1]), BUTTON_TEXT, fill=(255, 255, 255), font=fb)

    canvas.save(OUTPUT_FILE, "JPEG", quality=92)
    print(f"✓ {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE) / 1024:.0f} KB)")


if __name__ == "__main__":
    build()
