#!/usr/bin/env python3
"""gong-promo: cut one client moment from a Gong recording into a PropFuel "Client stories" clip (1080x1920), and QA it.

  promo.py check                      ffmpeg / ffprobe / Pillow / numpy present?
  promo.py render spec.json           -> spec["out"] (mp4, H.264 + AAC: the clip + the approved logo sting end card)
  promo.py qa clip.mp4 [sheet.jpg]    size, codec, length, audio-tail checks and a contact sheet (exit 1 on failure)

spec.json: {"src": "call.mp4", "out": "clip.mp4", "person": "Kate Elliott", "org": "Elevate",
            "head": "Our numbers have [pretty much doubled.]",     # headline: words said in the clip, in order; [..] = gold highlight
            "face": [x, y, w, h] or omitted,                       # the speaker's tile in the recording (omitted: name tile)
            "sentences": [[start_s, end_s, "verbatim text"], ...]} # the client's consecutive Gong sentences
The look is the approved cream "Client stories" style (layout, type, colours, tile, caption pill, name card, end card are
copied from the propfuel-meta-ads testimonial renderer). What this script adds: the cut starts on the quietest 10 ms before
the first word and ends on the MEASURED end of the last word (audio energy, never the transcript) plus real room tone; pauses
over 0.7 s between sentences are cut to a breath; captions are exactly the spoken text; frames where Gong shows someone else
under the client's words get the client's name tile.
Caption word timing is estimated from sentence times and the voiced stretches of the audio (Gong has no word times).
"""
import json, re, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent.parent / "assets"
W, H, FPS = 1080, 1920, 30
CREAM, CHAR, MID, STEEL, GOLD, WHITE = (244, 241, 234), (47, 47, 47), (110, 110, 110), (74, 127, 165), (251, 192, 45), (255, 255, 255)
L = dict(logo_y=210, logo_h=60, head_y=310, head_size=72, head_h=300, panel=(40, 660, 1000), cap_gap=36, cap_size=48, name_size=34)  # house 9x16
BOUNDS = (40, 200, 1040, 1560)  # Reels/Stories: keep content inside x 40-1040, y 200-1560 (house layout)
END_SECS = 4.5  # approved v4 logo sting
STING_VOL = 0.4
SR = 16000
GAP_MAX, GAP_KEEP = 0.7, 0.3  # pauses between sentences longer than this are cut to this much room tone
ROOM_END = 0.4  # room tone kept after the last word, before the end card
QUIET_DB = 12  # "quiet" = within this many dB of the call's room-tone floor


def sh(*a, **k):
    return subprocess.run([str(x) for x in a], check=True, capture_output=True, **k)


def font(weight, size):
    return ImageFont.truetype(str(HERE / f"DMSans-{weight}.ttf"), size)


def ease(t):
    return t * t * (3 - 2 * t)


# ---------- audio measurement ----------
def read_db(src, t0, t1):
    """5 ms RMS in dB over [t0, t1] -> (t0, db array)."""
    t0 = max(0.0, t0)
    raw = sh("ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", src, "-vn", "-ac", "1", "-ar", SR, "-f", "s16le", "-").stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32)
    n = len(x) // 80
    return t0, 20 * np.log10(np.sqrt((x[: n * 80].reshape(n, 80) ** 2).mean(1)) + 1)


def floor_db(src, a, b):
    _, db = read_db(src, a - 5, b + 5)
    return float(np.percentile(db[db > 5], 5)) if (db > 5).any() else 0.0


def snap_in(src, t):
    """Quietest 10 ms just before the first word, so the cut lands between words."""
    t0, db = read_db(src, t - 0.35, t + 0.1)
    e = np.convolve(db, np.ones(2) / 2, mode="same")
    return t0 + int(np.argmin(e)) * 0.005


def room_tail(src, b, floor):
    """(end, room_s, decay): end of the last word measured from audio, plus ROOM_END of room tone. Exits if the speaker runs on."""
    t0, db = read_db(src, b - 0.4, b + 2.2)
    quiet = db < floor + QUIET_DB
    first = int(0.25 / 0.005)  # never decide inside the first 250 ms: the word may still be sounding past its transcript end
    d = next((i for i in range(first, len(db) - 10) if quiet[i:i + 10].all()), None)  # 50 ms of room tone = the word has decayed
    if d is None:
        raise SystemExit(f"FAIL: no pause within 2 s after {b:.2f}s: the speaker runs on. End the quote at a sentence with a pause after it.")
    o = next((i for i in range(d, len(db) - 5) if not quiet[i:i + 6].any()), None)  # 30 ms of sound = something new starts
    end = t0 + d * 0.005 + ROOM_END
    if o is not None:
        end = min(end, t0 + o * 0.005 - 0.02)
    return round(end, 3), round(end - (t0 + d * 0.005), 3), t0 + d * 0.005


def brand(t):
    return re.sub(r"\bprop ?fuel\b", "PropFuel", t.replace("…", "").replace("  ", " "), flags=re.I)


def word_times(src, s0, s1, toks, floor, cap=None):
    """Spread the words over the VOICED time of the sentence (pauses inside it get no words): [(t0, t1)] in call seconds."""
    t0, db = read_db(src, s0 - 0.1, s1 + 0.15)
    v = db > floor + QUIET_DB
    idx = np.flatnonzero(v)
    lo = t0 + (idx[idx * 0.005 + t0 >= s0 - 0.05][0] if (idx * 0.005 + t0 >= s0 - 0.05).any() else 0) * 0.005 if len(idx) else s0
    hi = min(cap or 1e9, t0 + (idx[-1] + 1) * 0.005) if len(idx) else s1
    sel = np.flatnonzero(v & (np.arange(len(v)) * 0.005 + t0 >= lo - 1e-9) & (np.arange(len(v)) * 0.005 + t0 <= hi))
    if len(sel) < len(toks) * 3:
        sel = np.arange(int(round((lo - t0) / 0.005)), max(int(round((hi - t0) / 0.005)), int(round((lo - t0) / 0.005)) + 1))
    wt = np.array([len(w) + 2 for w in toks], float)
    cuts = np.concatenate([[0], np.cumsum(wt)]) / wt.sum() * (len(sel) - 1)
    return [(t0 + sel[int(round(cuts[i]))] * 0.005, t0 + sel[int(round(cuts[i + 1]))] * 0.005) for i in range(len(toks))]


# ---------- plan: sentences -> parts (cuts) with caption words ----------
def plan(spec):
    src, sents = spec["src"], spec["sentences"]
    floor = floor_db(src, sents[0][0], sents[-1][1])
    groups, cur = [], [sents[0]]
    for s in sents[1:]:
        if s[0] - cur[-1][1] > GAP_MAX:
            groups.append(cur); cur = []
        cur.append(s)
    groups.append(cur)
    parts, t_clip = [], 0.0
    for gi, g in enumerate(groups):
        a = snap_in(src, g[0][0])
        last = gi == len(groups) - 1
        end, room, decay = room_tail(src, g[-1][1], floor)
        if not last:  # inner cut: keep only a short breath after the word
            end = min(end, decay + GAP_KEEP)
        words = []
        for k, s in enumerate(g):
            toks = brand(s[2]).split()
            tt = word_times(src, s[0], s[1], toks, floor, cap=decay if k == len(g) - 1 else None)
            words += [(max(t_clip, x0 - a + t_clip), max(t_clip, x1 - a + t_clip), w) for (x0, x1), w in zip(tt, toks)]
        parts.append(dict(a=a, b=end, t=t_clip, words=words, room=room))
        t_clip += end - a
    return parts, t_clip, floor


# ---------- headline, captions, tile (copied from the house renderer) ----------
_MASKS, _SHADOWS, _RING, _BG, _LOGOS = {}, {}, {}, {}, {}


def rounded_mask(size, r):
    if (size, r) not in _MASKS:
        m = Image.new("L", size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=255)
        _MASKS[(size, r)] = m
    return _MASKS[(size, r)]


def shadow_card(base, box, r=28, blur=22, alpha=55):
    key = (base.size, tuple(box))
    if key not in _SHADOWS:
        x, y, w, h = box
        s = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(s).rounded_rectangle([x, y + 10, x + w, y + h + 10], r, fill=(60, 45, 20, alpha))
        _SHADOWS[key] = s.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(_SHADOWS[key])


def wave_ring(w, h, lv, r=24):
    """Active-speaker ring: a crisp gold edge plus a soft glow that swells with the voice. Paste at (x - margin, y - margin)."""
    q = round(min(lv, 1) * 16)
    key = (w, h, q)
    if key not in _RING:
        k, m = q / 16, 96
        lay = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
        glow = Image.new("RGBA", lay.size, (0, 0, 0, 0))
        spread = 4 + 14 * k
        ImageDraw.Draw(glow).rounded_rectangle([m - spread, m - spread, m + w + spread, m + h + spread], r + spread,
                                               outline=GOLD + (round(70 + 150 * k),), width=round(6 + 10 * k))
        lay.alpha_composite(glow.filter(ImageFilter.GaussianBlur(6 + 8 * k)))
        ImageDraw.Draw(lay).rounded_rectangle([m - 5, m - 5, m + w + 4, m + h + 4], r + 4, outline=GOLD + (round(170 + 85 * k),), width=5)
        _RING[key] = (lay, m)
    return _RING[key]


def logo_at(h):
    if h not in _LOGOS:
        lg = Image.open(HERE / "PF_Main_Logo_Yellow.png").convert("RGBA")
        _LOGOS[h] = lg.resize((round(lg.width * h / lg.height), h), Image.LANCZOS)
    return _LOGOS[h]


def parse_head(head):
    toks, hl = [], False
    for w in head.split():
        if "[" in w:
            hl, w = True, w.replace("[", "")
        end = "]" in w
        toks.append((w.replace("]", ""), hl))
        if end:
            hl = False
    return toks


def headline(head, glow):
    key = (head, round(glow, 2))
    if key in _BG:
        return _BG[key].copy()
    im = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(im)
    lg = logo_at(L["logo_h"])
    im.alpha_composite(lg, (44, L["logo_y"]))
    d.text((44 + lg.width + 16, L["logo_y"] + L["logo_h"] / 2), "Client stories", font=font("SemiBold", round(L["logo_h"] * 0.5)), fill=STEEL, anchor="lm")
    toks = parse_head("“" + head.strip().replace("]", "]", 1))
    toks = [(w, h) for w, h in toks]
    toks[-1] = (toks[-1][0] + "”", toks[-1][1])
    size = L["head_size"]
    while True:
        f = font("Bold", size)
        sp = d.textlength(" ", font=f)
        lines, cur, x = [], [], 0
        for w, h in toks:
            ww = d.textlength(w, font=f)
            if cur and x + ww > W - 88:
                lines.append(cur); cur, x = [], 0
            cur.append((w, h, x, ww)); x += ww + sp
        lines.append(cur)
        lh = size * 1.14
        if len(lines) * lh <= L["head_h"] or size < 24:
            break
        size -= 2
    y0 = L["head_y"] + (L["head_h"] - len(lines) * lh) / 2 - size * 0.1
    for i, ln in enumerate(lines):
        y = y0 + i * lh
        run = [t for t in ln if t[1]]
        if run and glow > 0:
            x0, x1 = 44 + run[0][2], 44 + run[-1][2] + run[-1][3]
            d.rounded_rectangle([x0 - size * 0.14, y + size * 0.08, x1 + size * 0.14, y + size * 1.12], size * 0.18,
                                fill=tuple(round(c * glow + b * (1 - glow)) for c, b in zip(GOLD, CREAM)))
        for w, h, x, ww in ln:
            d.text((44 + x, y), w, font=f, fill=CHAR)
    _BG[key] = im
    return im.copy()


def chip(im, x, y, size, text="RECORDED CLIENT CALL"):
    d = ImageDraw.Draw(im)
    f = font("Bold", size)
    tw = d.textlength(text, font=f)
    pad, dot = round(size * 0.6), size * 0.62
    w, h = pad * 2 + dot + pad * 0.7 + tw, size + pad * 1.4
    d.rounded_rectangle([x, y, x + w, y + h], h / 2, fill=(30, 30, 30, 215))
    d.ellipse([x + pad, y + h / 2 - dot / 2, x + pad + dot, y + h / 2 + dot / 2], fill=(225, 72, 60))
    d.text((x + pad + dot + pad * 0.7, y + h / 2), text, font=f, fill=WHITE, anchor="lm")


def chunks_for(words, maxn=4, maxdur=1.6):
    """Caption chunks. A lone word merges into its neighbour (never one word alone)."""
    out, cur = [], []
    for w in words:
        if cur and (len(cur) >= maxn or w[1] - cur[0][0] > maxdur or cur[-1][2][-1] in ".?!,"):
            out.append(cur); cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    k = 0
    while k < len(out):
        if len(out[k]) == 1 and len(out) > 1:
            if k + 1 < len(out) and len(out[k + 1]) <= 4 and not out[k][0][2].endswith((".", "?", "!")):
                out[k + 1] = out[k] + out[k + 1]; del out[k]; continue
            if k > 0 and len(out[k - 1]) <= 4:
                out[k - 1] += out[k]; del out[k]; continue
        k += 1
    return out


def pill(chunk):
    d = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    f = font("Bold", L["cap_size"])
    ws = [d.textlength(w[2], font=f) for w in chunk]
    return sum(ws) + d.textlength(" ", font=f) * (len(chunk) - 1) + 56, ws


def captions(im, y0, chunks, now):
    cur = next((c for c in chunks if c[0][0] - 0.08 <= now <= c[-1][1] + 0.3), None)
    if not cur:
        return
    d = ImageDraw.Draw(im)
    f = font("Bold", L["cap_size"])
    bw, ws = pill(cur)
    bh = L["cap_size"] * 1.25 + 28
    x0 = (W - bw) / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 20, fill=CHAR)
    x, sp = x0 + 28, d.textlength(" ", font=f)
    for (t0, t1, w), ww in zip(cur, ws):
        d.text((x, y0 + bh / 2), w, font=f, fill=GOLD if t0 <= now < t1 + 0.12 else WHITE, anchor="lm")
        x += ww + sp


def name_card(im, y, person, org):
    d = ImageDraw.Draw(im)
    d.text((W / 2, y), person, font=font("Bold", L["name_size"]), fill=CHAR, anchor="mt")
    d.text((W / 2, y + L["name_size"] * 1.25), f"{org} · PropFuel client", font=font("Medium", round(L["name_size"] * 0.8)), fill=MID, anchor="mt")


_AV = {}


def name_tile(w, h, who):
    """The speaker's tile when there's no footage of them at that moment: dark tile, initials, name label."""
    if (w, h, who) in _AV:
        return _AV[(w, h, who)]
    S = 2
    im = Image.new("RGB", (w * S, h * S), (44, 50, 60))
    d = ImageDraw.Draw(im)
    cx, cy, r = w * S / 2, h * S * 0.46, h * S * 0.19
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=STEEL)
    d.text((cx, cy), "".join(p[0] for p in who.split()[:2]), font=font("Bold", round(r * 0.9)), fill=WHITE, anchor="mm")
    fs = round(h * S * 0.07)
    f = font("SemiBold", fs)
    tw, pad = d.textlength(who, font=f), fs * 0.5
    d.rounded_rectangle([fs * 0.6, h * S - fs * 2.1, fs * 0.6 + tw + pad * 2, h * S - fs * 0.6], fs * 0.3, fill=(20, 22, 26))
    d.text((fs * 0.6 + pad, h * S - fs * 1.35), who, font=f, fill=WHITE, anchor="lm")
    _AV[(w, h, who)] = im.resize((w, h), Image.LANCZOS)
    return _AV[(w, h, who)]


class Sting:
    """The approved icon sting (plane, trace, fuel fill) over cream from the alpha master, then the tagline and demo button."""
    def __init__(self):
        self.S, self.cy = 1080, H * 0.36
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", str(HERE / "sting-alpha-1080.webm"), "-vf", "scale=1080:1080",
                                   "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
        self.last = None

    def frame(self, t):
        raw = self.p.stdout.read(self.S * self.S * 4)
        if len(raw) == self.S * self.S * 4:
            self.last = Image.frombytes("RGBA", (self.S, self.S), raw)
        im = Image.new("RGBA", (W, H), CREAM + (255,))
        if self.last is not None:
            im.alpha_composite(self.last, (round((W - self.S) / 2), round(self.cy - self.S / 2)))
        d = ImageDraw.Draw(im)
        fs, y = 84, self.cy + 216 + 64
        for k, line in enumerate(("Know and Grow", "Your Membership")):
            a = ease(min(max((t - 2.92 - 0.12 * k) / 0.45, 0), 1))
            if a > 0:
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(lay).text((W / 2, y + (1 - a) * 28), line, font=font("Bold", fs), fill=CHAR + (round(255 * a),), anchor="mt")
                im.alpha_composite(lay)
            y += fs * 1.2
        y += 40
        a = ease(min(max((t - 3.35) / 0.4, 0), 1))
        if a > 0:
            bw, bh = 520, 112
            xs = np.linspace(0, 1, bw)[None, :, None]
            arr = (np.array((244, 124, 44)) * (1 - xs) + np.array(GOLD) * xs).repeat(bh, axis=0).astype(np.uint8)
            btn = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
            btn.paste(Image.fromarray(arr), (0, 0), rounded_mask((bw, bh), bh // 2))
            ImageDraw.Draw(btn).text((bw / 2, bh / 2), "Book a demo", font=font("Bold", 46), fill=WHITE, anchor="mm")
            btn.putalpha(Image.eval(btn.getchannel("A"), lambda v: round(v * a)))
            im.alpha_composite(btn, (round((W - bw) / 2), round(y)))
        return im.convert("RGB")

    def close(self):
        self.p.kill()


# ---------- footage: the speaker's tile, minus frames where Gong shows someone else ----------
def tile_box(face):
    fx, fy, fw, fh = face
    if abs(fw / fh - 16 / 9) < 0.02:
        return face
    if fw / fh > 16 / 9:
        nw = round(fh * 16 / 9); return [fx + (fw - nw) // 2, fy, nw, fh]
    nh = round(fw * 9 / 16); return [fx, fy + (fh - nh) // 2, fw, nh]


def live_mask(src, a, b, box):
    """True while the speaker is the face in the tile. Gong switches the tile to whoever makes a sound, so staff faces
    appear under client words. Reference = the most typical frame of the clip; short flickers are smoothed (0.6 s)."""
    x, y, w, h = box
    raw = sh("ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-i", src, "-t", f"{b - a:.3f}", "-vf", f"fps={FPS},crop={w}:{h}:{x}:{y},scale=24:18:flags=area",
             "-f", "rawvideo", "-pix_fmt", "rgb24", "-").stdout
    small = np.frombuffer(raw, np.uint8).reshape(-1, 18, 24, 3).astype(float)
    n = round((b - a) * FPS)
    small = np.concatenate([small, np.repeat(small[-1:], max(0, n - len(small)), 0)])[:n]
    cand = small[::6]
    ref = cand[int(np.argmin([np.median(np.abs(small - c).mean((1, 2, 3))) for c in cand]))]
    m = np.abs(small - ref).mean((1, 2, 3)) < 30
    hold = round(0.6 * FPS)
    for val in (False, True):  # widen short off-runs, then drop short on-runs
        i = 0
        while i < n:
            j = i
            while j < n and m[j] == m[i]:
                j += 1
            if m[i] == val and j - i < hold:
                if val is False:
                    m[max(0, i - (hold - (j - i)) // 2):i + hold] = False
                elif i > 0 and j < n:
                    m[i:j] = False
            i = j
    return m


def stream_frames(src, a, b, box, size):
    """Yield one PIL frame per output frame, straight from the recording (no big arrays in memory)."""
    x, y, w, h = box
    n, sz = round((b - a) * FPS), size[0] * size[1] * 3
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-i", src, "-t", f"{b - a + 0.3:.3f}", "-vf",
                          f"fps={FPS},crop={w}:{h}:{x}:{y},scale={size[0]}:{size[1]}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    last = None
    for _ in range(n):
        buf = p.stdout.read(sz)
        if len(buf) == sz:
            last = Image.frombuffer("RGB", size, buf)
        yield last
    p.stdout.close(); p.kill(); p.wait()


# ---------- end-of-speech gate: "Are you cutting off at the end before they're done speaking?" ----------
def last_words(wav, t0, t1):
    """Words in the last stretch of the rendered track, from a local whisper if one is installed (mlx_whisper, faster_whisper or whisper); None if none is."""
    seg = Path(tempfile.mkdtemp()) / "end.wav"
    sh("ffmpeg", "-v", "error", "-y", "-ss", f"{max(t0, 0):.3f}", "-t", f"{t1 - max(t0, 0):.3f}", "-i", wav, "-vn", "-ac", "1", "-ar", SR, seg)
    try:
        import mlx_whisper
        r = mlx_whisper.transcribe(str(seg), path_or_hf_repo="mlx-community/whisper-large-v3-turbo", word_timestamps=True, condition_on_previous_text=False)
        return [w["word"] for s in r["segments"] for w in s.get("words", [])]
    except ImportError:
        pass
    try:
        from faster_whisper import WhisperModel
        segs, _ = WhisperModel("small", compute_type="int8").transcribe(str(seg), word_timestamps=True)
        return [w.word for s in segs for w in s.words]
    except ImportError:
        pass
    try:
        import whisper
        r = whisper.load_model("small").transcribe(str(seg), word_timestamps=True)
        return [w["word"] for s in r["segments"] for w in s["words"]]
    except ImportError:
        return None


def end_gate(wav, speech_end, fade, last_word, src=None, cut=None):
    """Hard gate, run on the finished audio before any video is encoded. PASS needs: (a) the last 150 ms before the fade is room tone
    (>=30 dB under the speech), (b) the speech has decayed at the cut (last 30 ms >=12 dB under it) and is not rising into a next word,
    (c) a transcript of the last ~3 s ends on the full intended last word (whisper if installed; otherwise the energy checks plus the Gong
    transcript's last word are all there is, and the line says so). Returns (ok, line)."""
    _, d = read_db(wav, max(0, speech_end - 3.0), fade)
    d = d[::2]  # 10 ms
    k = round(min(3.0, speech_end) / 0.01)
    w90 = float(np.percentile(d[:k], 90))
    tail = float(d[-15:].mean())
    dec = w90 - float(d[max(0, k - 3):k].mean())
    rise = float(d[max(0, k - 3):k].mean()) - float(d[max(0, k - 9):max(0, k - 3)].mean())
    why = []
    if w90 - tail < 30: why.append(f"the last 150 ms before the fade is {tail:.0f} dB, the speech is {w90:.0f} dB (not room tone)")
    if dec < 12: why.append(f"the speech is still {w90 - dec:.0f} dB at the cut ({dec:.0f} dB decay, need 12)")
    if rise > 6 and dec < 16: why.append(f"a new sound is starting at the cut (+{rise:.0f} dB in the last 30 ms)")
    want, got, note = re.sub(r"[^a-z0-9]", "", last_word.lower()), None, ""
    ws = last_words(wav, speech_end - 3.0, min(fade, speech_end + 0.8))
    if ws is None:
        note = " (no local whisper: transcript check skipped, energy checks only; pip install mlx-whisper or faster-whisper)"
    elif not ws or not re.sub(r"[^a-z0-9]", "", ws[-1].lower()) or not (want == (got := re.sub(r"[^a-z0-9]", "", ws[-1].lower())) or want.endswith(got)):
        why.append(f"the last transcribed word is '{re.sub(r'[^a-z0-9]', '', ws[-1].lower()) if ws else ''}', the quote ends '{want}'")
    line = (f"End check: last word '{want}' completes at {speech_end:.2f}s, fade at {fade:.2f}s, tail room tone {tail:.0f} dB (speech {w90:.0f} dB) -> "
            + ("PASS" + note if not why else "FAIL: " + "; ".join(why)))
    print(line, flush=True)
    return not why, line


# ---------- render ----------
def build_audio(src, parts, wav, dur):
    f, labels = [], ""
    for i, p in enumerate(parts):
        d = p["b"] - p["a"]
        f.append(f"[0:a]atrim=start={p['a']:.3f}:end={p['b']:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                 f"afade=t=in:d=0.02,afade=t=out:st={d - 0.04:.3f}:d=0.04[a{i}]")
        labels += f"[a{i}]"
    ms = round(dur * 1000)
    f.append(f"{labels}concat=n={len(parts)}:v=0:a=1,apad=pad_dur={END_SECS},highpass=f=80,afftdn=nf=-25,loudnorm=I=-14:TP=-1.5:LRA=11[v]")
    f.append(f"[1:a]aresample=48000,volume={STING_VOL},adelay={ms}|{ms}[s]")  # sting SFX from the end card's first frame, after loudnorm
    f.append("[v][s]amix=inputs=2:duration=first:normalize=0[o]")
    sh("ffmpeg", "-v", "error", "-y", "-i", src, "-i", HERE / "sting-sfx.wav", "-filter_complex", ";".join(f), "-map", "[o]", "-ar", 48000, wav)


def levels(wav, n):
    raw = sh("ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", 16000, "-f", "s16le", "-").stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32)
    hop = SR // FPS
    r = np.sqrt((x[: len(x) // hop * hop].reshape(-1, hop) ** 2).mean(1))
    r = r[:n]
    return r / (np.percentile(r, 95) + 1e-6)


def check_head(head, words):
    norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
    h = [norm(w) for w in head.replace("[", "").replace("]", "").split()]
    toks = [norm(w[2]) for w in words]
    if not any(toks[i:i + len(h)] == h for i in range(len(toks) - len(h) + 1)):
        raise SystemExit(f'FAIL: the headline "{head}" must be words said in the clip, in order, with nothing added or changed.')


def render(spec_path):
    spec = json.load(open(spec_path))
    src = spec["src"] = str(Path(spec["src"]).expanduser())
    out = Path(spec["out"]).expanduser()
    parts, dur, floor = plan(spec)
    words = [w for p in parts for w in p["words"]]
    check_head(spec["head"], words)
    chunks = chunks_for(words)
    for c in chunks:  # every caption pill must fit the panel width
        if pill(c)[0] > L["panel"][2]:
            raise SystemExit(f"FAIL: caption too wide for the frame: {' '.join(w[2] for w in c)}")
    px, py, pw = L["panel"]
    ph = round(pw * 9 / 16)
    name_y = py + ph + L["cap_gap"] * 2 + L["cap_size"] * 1.25 + 28
    if name_y + L["name_size"] * 2.4 > BOUNDS[3]:
        raise SystemExit("FAIL: layout runs below the safe area")
    print(f"cut {len(parts)} part(s), {dur:.1f}s of speech, room tone after last word {parts[-1]['room']:.2f}s, floor {floor:.0f} dB")
    if not 12 <= dur <= 32:
        print(f"WARN: clip is {dur:.1f}s; aim for 15-30 s")
    tmp = Path(tempfile.mkdtemp(prefix="gong-promo-"))
    wav = tmp / "a.wav"
    build_audio(src, parts, wav, dur)
    last = re.sub(r"[^A-Za-z0-9' ]", "", spec["sentences"][-1][2]).split()[-1]
    ok, _ = end_gate(wav, dur - parts[-1]["room"], dur, last)  # the word ends `room` seconds before the end card
    if not ok:
        raise SystemExit("END CHECK FAILED, no file written. Move the out point to the measured end of the last word (energy decay), never the transcript end-time.")
    lv_all = levels(wav, round(dur * FPS))
    # per-frame source of the speaker tile
    seq = []
    for p in parts:
        n = round((p["b"] - p["a"]) * FPS)
        if spec.get("face"):
            box = tile_box(spec["face"])
            m = live_mask(src, p["a"], p["b"], box)
            seq.append((stream_frames(src, p["a"], p["b"], box, (pw, ph)), m))
        else:
            seq.append((iter([None] * n), np.zeros(n, bool)))
    on = np.concatenate([m for _, m in seq])
    if spec.get("face"):
        print(f"speaker on camera for {on.mean() * 100:.0f}% of the clip; their name tile covers the rest")
    out.parent.mkdir(parents=True, exist_ok=True)
    total = round((dur + END_SECS) * FPS)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wav),
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)],
                           stdin=subprocess.PIPE)
    tile = name_tile(pw, ph, spec["person"])
    sting, last, pi, fi, held = None, None, 0, 0, None
    for i in range(total):
        t = i / FPS
        if t >= dur:
            sting = sting or Sting()
            frame = sting.frame(t - dur)
            k = (t - dur) / 0.4
            if k < 1 and last is not None:
                frame = Image.blend(last, frame, ease(k))
            enc.stdin.write(frame.tobytes())
            continue
        while pi + 1 < len(parts) and t >= parts[pi + 1]["t"] - 1e-9:
            pi, fi = pi + 1, 0
        gen, m = seq[pi]
        raw = next(gen, None)  # a part can be one frame short of the timeline: hold its last frame
        if raw is None:
            raw = held
        held = raw
        live = raw if (raw is not None and m[min(fi, len(m) - 1)]) else None
        fi += 1
        glow = 1.0 - ease(min(max((t - 2.4) / 0.6, 0), 1))
        im = headline(spec["head"], round(glow * 20) / 20)
        shadow_card(im, (px, py, pw, ph))
        k = min(int(t * FPS), len(lv_all) - 1)
        lv = max(float(lv_all[max(0, k - j)]) * 0.78 ** j for j in range(6))
        ring, mg = wave_ring(pw, ph, lv)
        im.alpha_composite(ring, (px - mg, py - mg))
        im.paste((live if live is not None else tile).convert("RGBA"), (px, py), rounded_mask((pw, ph), 24))
        chip(im, px + 16, py + 16, max(16, round(pw * 0.022)))
        captions(im, py + ph + L["cap_gap"], chunks, t)
        name_card(im, name_y, spec["person"], spec["org"])
        frame = im.convert("RGB")
        last = frame
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("FAIL: ffmpeg encode failed")
    if sting:
        sting.close()
    print(f"wrote {out} ({dur + END_SECS:.1f}s). Run: promo.py qa {out}")


# ---------- QA ----------
def qa(path, sheet=None):
    path = str(Path(path).expanduser())
    pr = json.loads(sh("ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,codec_type:format=duration", "-of", "json", path).stdout)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    dur = float(pr["format"]["duration"])
    bad = []
    if (v["width"], v["height"], v["codec_name"]) != (W, H, "h264"):
        bad.append(f"expected 1080x1920 h264, got {v['width']}x{v['height']} {v['codec_name']}")
    if not 17 <= dur <= 38:
        bad.append(f"length {dur:.1f}s (speech 15-30 s + {END_SECS} s end card)")
    # the room tone before the end card must be quiet next to the voice, or the last word was clipped
    cut = dur - END_SECS
    _, db = read_db(path, 0, cut + 0.5)
    tail = db[int((cut - 0.35) / 0.005): int((cut - 0.05) / 0.005)]
    loud = float(np.percentile(db[: int(cut / 0.005)], 95))
    print(f"audio: voice ~{loud:.0f} dB, the 0.3 s before the end card peaks at {tail.max():.0f} dB")
    if tail.max() > loud - 15:
        bad.append("voice is still sounding right before the end card: the last word may be clipped")
    if sheet:
        d = Path(tempfile.mkdtemp())
        sh_ = Image.new("RGB", (270 * 5, 480 * 2), CREAM)
        for i in range(10):  # 9 frames across the clip plus the last frame
            sh("ffmpeg", "-v", "error", "-y", "-ss", f"{(i + 0.5) * dur / 10 if i < 9 else dur - 0.1:.2f}", "-i", path, "-frames:v", "1", "-vf", "scale=270:480", d / f"{i}.jpg")
            sh_.paste(Image.open(d / f"{i}.jpg"), ((i % 5) * 270, (i // 5) * 480))
        sh_.save(sheet, quality=88)
        print(f"contact sheet: {sheet} (open it: headline highlight, gold-ringed window, caption pill, name and org right, last frame = logo end card)")
    for b in bad:
        print("FAIL:", b)
    print("QA " + ("FAILED" if bad else "passed (automatic checks; still look at the sheet)"))
    return 1 if bad else 0


def check():
    ok = True
    for tool in ("ffmpeg", "ffprobe"):
        if subprocess.run(["which", tool], capture_output=True).returncode:
            print(f"missing {tool}: install with  brew install ffmpeg  (no Homebrew? https://brew.sh)"); ok = False
    if ok and b"libvpx-vp9" not in subprocess.run(["ffmpeg", "-decoders"], capture_output=True).stdout:
        print("this ffmpeg can't decode the logo animation: brew reinstall ffmpeg"); ok = False
    print("deps ok" if ok else "")
    return 0 if ok else 1


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "check": sys.exit(check())
    elif c == "render" and len(sys.argv) > 2: render(sys.argv[2])
    elif c == "qa" and len(sys.argv) > 2: sys.exit(qa(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None))
    else: print(__doc__); sys.exit(2)
