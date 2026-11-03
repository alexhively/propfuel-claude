#!/usr/bin/env python3
"""gong-promo: cut one client moment from a Gong recording into a 1080x1920 promo clip, and QA it.

  promo.py check                      ffmpeg / ffprobe / Pillow / numpy present?
  promo.py render spec.json           -> spec["out"] (mp4, H.264 + AAC, clip + approved logo sting end card)
  promo.py qa clip.mp4 [sheet.jpg]    size, codec, length, audio-tail and contact-sheet checks (exit 1 on failure)

spec.json: {"src": "call.mp4", "out": "clip.mp4", "person": "Kate Elliott", "org": "Elevate", "role": "optional title",
            "highlight": "pretty much doubled", "face": [x, y, w, h] or omitted (name tile instead of footage),
            "sentences": [[start_s, end_s, "verbatim text"], ...]}   # the client's consecutive Gong sentences
Rules it enforces: the cut starts on the quietest 10 ms before the first word; it ends on the MEASURED end of the last word
(audio energy, not the transcript) plus real room tone; pauses over 0.7 s between sentences are cut to a short breath;
captions are exactly the spoken text; every text box stays inside the 9:16 safe box (x 100-880, y 290-1340).
Caption timing inside a sentence is estimated (Gong gives sentence times, not word times): check the sheet.
"""
import json, re, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent / "assets"
W, H, FPS = 1080, 1920, 30
SAFE = (100, 290, 880, 1340)  # x0, y0, x1, y1 (vertical-safe-zones skill)
CX = 490  # centre of the safe box: the right side of the frame is covered by the platform buttons
CREAM, CHAR, MID, GOLD, STEEL, WHITE = (244, 241, 234), (47, 47, 47), (110, 110, 110), (251, 192, 45), (74, 127, 165), (255, 255, 255)
SR = 16000
GAP_MAX, GAP_KEEP = 0.7, 0.3  # pauses between sentences longer than this are cut to this much room tone
ROOM_END = 0.5  # room tone kept after the last word (the last 0.25 s of it fades out)
QUIET_DB = 12  # "quiet" = within this many dB of the call's room-tone floor


def sh(*a, **k):
    return subprocess.run([str(x) for x in a], check=True, capture_output=True, **k)


def font(weight, size):
    f = ImageFont.truetype(str(HERE / "DMSans-Variable.ttf"), size)
    f.set_variation_by_name(weight)
    return f


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
    """(end, room_s): end of the last word measured from audio, plus ROOM_END of room tone. Raises if the speaker runs on."""
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


def onset(src, a, floor):
    """First voiced moment at/after a (30 ms above the floor)."""
    t0, db = read_db(src, a, a + 1.5)
    v = db > floor + QUIET_DB
    i = next((i for i in range(len(db) - 6) if v[i:i + 6].all()), 0)
    return t0 + i * 0.005


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
        a, b = snap_in(src, g[0][0]), None
        last = gi == len(groups) - 1
        end, room, decay = room_tail(src, g[-1][1], floor)
        if not last:  # inner cut: keep only a short breath after the word
            end = min(end, decay + GAP_KEEP)
        words = []
        starts = [onset(src, g[0][0] - 0.05, floor)] + [max(s[0], a) for s in g[1:]]
        for k, s in enumerate(g):
            t0 = max(starts[k], a)
            t1 = min(s[1], decay) if k == len(g) - 1 else s[1]
            toks = brand(s[2]).split()
            wt = np.array([len(w) + 2 for w in toks], float)
            edges = t0 + (t1 - t0) * np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
            words += [(edges[i] - a + t_clip, edges[i + 1] - a + t_clip, w) for i, w in enumerate(toks)]
        parts.append(dict(a=a, b=end, t=t_clip, words=words, room=room))
        t_clip += end - a
    return parts, t_clip, floor


def brand(t):
    return re.sub(r"\bprop ?fuel\b", "PropFuel", t.replace("…", "").replace("  ", " "), flags=re.I)


# ---------- drawing ----------
def wrap(d, words, f, maxw):
    lines, cur = [], []
    for w in words:
        if cur and d.textlength(" ".join(x for x, _ in cur + [(w[0], 0)]), font=f) > maxw:
            lines.append(cur); cur = []
        cur.append(w)
    return lines + [cur]


def chunks(words, maxn=5, maxdur=2.4):
    out, cur = [], []
    for w in words:
        if cur and not (cur[-1][3] and w[3]) and (len(cur) >= maxn or w[1] - cur[0][0] > maxdur or cur[-1][2][-1] in ".?!"):
            out.append(cur); cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    k = 0
    while k < len(out):  # never one word alone
        if len(out[k]) == 1 and len(out) > 1:
            if k + 1 < len(out): out[k + 1] = out[k] + out[k + 1]; del out[k]; continue
            out[k - 1] += out[k]; del out[k]; continue
        k += 1
    return out


class Canvas:
    def __init__(self, spec):
        self.spec, self.boxes = spec, []
        base = Image.new("RGB", (W, H), CREAM)
        logo = Image.open(HERE / "propfuel-logo.png").convert("RGBA")
        lh = 64
        logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
        base.paste(logo, (CX - logo.width // 2, 300), logo)
        d = ImageDraw.Draw(base)
        nf, rf = font("Bold", 40), font("Medium", 30)
        sub = " · ".join(x for x in (spec.get("role"), spec["org"]) if x)
        self.text(d, CX, 1236, spec["person"], nf, CHAR)
        self.text(d, CX, 1288, sub, rf, MID)
        self.base, self.px, self.py = base, 100, 400
        self.pw = 780
        f = spec.get("face")
        self.ph = min(round(self.pw * f[3] / f[2]), 520) if f else 420
        self.cy = self.py + self.ph // 2

    def text(self, d, cx, y, s, f, fill):
        d.text((cx, y), s, font=f, fill=fill, anchor="mt")
        b = d.textbbox((cx, y), s, font=f, anchor="mt")
        self.boxes.append(b)

    def panel(self, im, face_frame, level):
        if face_frame is not None:
            im.paste(face_frame, (self.px, self.py))
            return
        d = ImageDraw.Draw(im, "RGBA")
        cx, r0 = CX, 110
        for i in range(2):  # audio-led rings: they swell with the voice
            r = r0 * (1.35 + 0.3 * i) + r0 * 0.4 * level * (1 + 0.2 * i)
            d.ellipse([cx - r, self.cy - r, cx + r, self.cy + r], outline=(GOLD if i == 0 else STEEL) + (round(70 + 170 * level),), width=round(3 + 7 * level))
        r = r0 * (1 + 0.1 * level)
        d.ellipse([cx - r, self.cy - r, cx + r, self.cy + r], fill=STEEL)
        ini = "".join(p[0] for p in self.spec["person"].split()[:2])
        d.text((cx, self.cy), ini, font=font("Bold", 96), fill=WHITE, anchor="mm")

    def caption(self, chunk):
        """RGBA layer with the chunk centred in y 880-1200; the highlight phrase gets a gold bar behind it."""
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        f = font("Bold", 58)
        lines = wrap(d, [(c[2], c[3]) for c in chunk], f, SAFE[2] - SAFE[0])
        lh, y = 76, 1040 - 76 * len(lines) / 2
        for ln in lines:
            sp = d.textlength(" ", font=f)
            tw = sum(d.textlength(w, font=f) for w, _ in ln) + sp * (len(ln) - 1)
            x = CX - tw / 2
            for w, hi in ln:
                wl = d.textlength(w, font=f)
                if hi:
                    d.rounded_rectangle([x - 8, y + 6, x + wl + 8, y + lh - 6], 10, fill=GOLD + (255,))
                d.text((x, y + 56), w, font=f, fill=CHAR, anchor="ls")  # one shared baseline (per-word top anchors drift)
                self.boxes.append((x, y, x + wl, y + lh))
                x += wl + sp
            y += lh
        return lay

    def assert_safe(self):
        x0, y0, x1, y1 = SAFE
        bad = [b for b in self.boxes if b[0] < x0 or b[2] > x1 or b[1] < y0 or b[3] > y1]
        if bad:
            raise SystemExit(f"FAIL: text outside the 9:16 safe box {SAFE}: {bad[:2]}")


# ---------- render ----------
def build_audio(spec, parts, wav, total):
    f, labels = [], ""
    for i, p in enumerate(parts):
        d = p["b"] - p["a"]
        f.append(f"[0:a]atrim=start={p['a']:.3f}:end={p['b']:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
                 f"afade=t=in:d=0.012,afade=t=out:st={d - 0.012:.3f}:d=0.012[a{i}]")
        labels += f"[a{i}]"
    f.append(f"{labels}concat=n={len(parts)}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=9,afade=t=out:st={total - 0.25:.3f}:d=0.25,"
             f"atrim=end={total:.3f},aformat=channel_layouts=stereo[o]")
    sh("ffmpeg", "-v", "error", "-y", "-i", spec["src"], "-filter_complex", ";".join(f), "-map", "[o]", "-ar", 48000, wav)


def levels(wav, n):
    raw = sh("ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", 16000, "-f", "s16le", "-").stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32)
    hop = SR // FPS
    r = np.sqrt((x[: len(x) // hop * hop].reshape(-1, hop) ** 2).mean(1)) if len(x) >= hop else np.zeros(1)
    r = np.convolve(r, np.ones(3) / 3, mode="same")
    r = np.clip(r / (np.percentile(r, 95) + 1), 0, 1)
    return np.concatenate([r, np.zeros(max(0, n - len(r)))])[:n]


def live_mask(arr, hold=round(0.6 * FPS)):
    """True while the speaker is the face in the tile. Gong switches the tile to whoever makes a sound, so staff faces
    appear under client words: those frames get the name tile instead. Reference = the most typical frame of the clip."""
    small = arr[:, ::arr.shape[1] // 18, ::arr.shape[2] // 24][:, :18, :24].astype(float)
    cand = small[::6]
    ref = cand[int(np.argmin([np.median(np.abs(small - c).mean((1, 2, 3))) for c in cand]))]
    m = np.abs(small - ref).mean((1, 2, 3)) < 30
    for val in (False, True):  # widen short off-runs, then drop short on-runs
        i = 0
        while i < len(m):
            j = i
            while j < len(m) and m[j] == m[i]:
                j += 1
            if m[i] == val and j - i < hold:
                if val is False:
                    m[max(0, i - (hold - (j - i)) // 2):i + hold] = False
                elif i > 0 and j < len(m):
                    m[i:j] = False
            i = j
    return m


def face_frames(spec, parts, C):
    """Per output frame: a PIL image of the speaker, or None (use the name tile)."""
    f = spec.get("face")
    if not f:
        return None
    x, y, w, h = f
    arrs = []
    for p in parts:
        n = round((p["b"] - p["a"]) * FPS)
        raw = sh("ffmpeg", "-v", "error", "-ss", f"{p['a']:.3f}", "-i", spec["src"], "-t", f"{p['b'] - p['a']:.3f}", "-vf",
                 f"fps={FPS},crop={w}:{h}:{x}:{y},scale={C.pw}:{C.ph}:force_original_aspect_ratio=increase,crop={C.pw}:{C.ph}",
                 "-f", "rawvideo", "-pix_fmt", "rgb24", "-").stdout
        fs = np.frombuffer(raw, np.uint8).reshape(-1, C.ph, C.pw, 3)
        arrs += [fs[min(i, len(fs) - 1)] for i in range(n)]
    arr = np.stack(arrs)
    m = live_mask(arr)
    print(f"speaker on camera for {m.mean() * 100:.0f}% of the clip; the name tile covers the rest")
    return [Image.fromarray(a) if ok else None for a, ok in zip(arr, m)]


def mark_highlight(words, phrase):
    """(t0, t1, word) -> (t0, t1, word, in_highlight). The phrase must appear whole, in order; else it is an error."""
    norm = lambda s: re.sub(r"\W", "", s.lower())
    hl = [norm(x) for x in brand(phrase).split()]
    on = [False] * len(words)
    toks = [norm(w[2]) for w in words]
    for i in range(len(toks) - len(hl) + 1) if hl else []:
        if toks[i:i + len(hl)] == hl:
            on[i:i + len(hl)] = [True] * len(hl)
    if hl and not any(on):
        raise SystemExit(f'FAIL: highlight "{phrase}" is not in the spoken text, word for word.')
    return [w + (o,) for w, o in zip(words, on)]


def render(spec_path):
    spec = json.load(open(spec_path))
    spec["src"] = str(Path(spec["src"]).expanduser())
    out = Path(spec["out"]).expanduser()
    parts, total, floor = plan(spec)
    words = [w for p in parts for w in p["words"]]
    words = mark_highlight(words, spec.get("highlight", ""))
    print(f"cut {len(parts)} part(s), {total:.1f}s of speech, room tone after last word {parts[-1]['room']:.2f}s, floor {floor:.0f} dB")
    if not 12 <= total <= 32:
        print(f"WARN: clip is {total:.1f}s; aim for 15-30 s")
    C = Canvas(spec)
    cks = chunks(words)
    layers = [C.caption(c) for c in cks]
    C.assert_safe()
    n = round(total * FPS)
    tmp = Path(tempfile.mkdtemp(prefix="gong-promo-"))
    wav = tmp / "a.wav"
    build_audio(spec, parts, wav, total)
    lv, faces = levels(wav, n), face_frames(spec, parts, C)
    clip = tmp / "clip.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wav),
                          "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(clip)], stdin=subprocess.PIPE)
    k = 0
    for i in range(n):
        t = i / FPS
        while k + 1 < len(cks) and t >= cks[k + 1][0][0] - 0.05:
            k += 1
        im = C.base.copy()
        C.panel(im, faces[i] if faces else None, float(lv[i]))
        if t >= cks[0][0][0] - 0.05 and t < cks[k][-1][1] + 0.5:  # a caption stays until the next one; none over the final room tone
            im.paste(layers[k], (0, 0), layers[k])
        p.stdin.write(im.tobytes())
    p.stdin.close()
    if p.wait():
        raise SystemExit("FAIL: ffmpeg encode failed")
    sh("ffmpeg", "-v", "error", "-y", "-i", clip, "-i", HERE / "end-card-9x16.mp4", "-filter_complex",
       "[1:v]fps=30,format=yuv420p[ev];[1:a]aresample=48000,aformat=channel_layouts=stereo[ea];[0:v][0:a][ev][ea]concat=n=2:v=1:a=1[v][a]",
       "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)
    json.dump(dict(out=str(out), speech_s=round(total, 2), clip_s=round(total + 4.45, 2), room_s=parts[-1]["room"], parts=[(round(p["a"], 2), round(p["b"], 2)) for p in parts]), open(tmp / "plan.json", "w"))
    print(f"wrote {out} ({total + 4.45:.1f}s). Run: promo.py qa {out}")


# ---------- QA ----------
def qa(path, sheet=None):
    path = str(Path(path).expanduser())
    pr = json.loads(sh("ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,codec_type:format=duration", "-of", "json", path).stdout)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    dur = float(pr["format"]["duration"])
    bad = []
    if (v["width"], v["height"], v["codec_name"]) != (W, H, "h264"):
        bad.append(f"expected 1080x1920 h264, got {v['width']}x{v['height']} {v['codec_name']}")
    if not 17 <= dur <= 36:
        bad.append(f"length {dur:.1f}s (speech 15-30 s + 4.45 s end card)")
    # audio tail: the 0.3 s of room tone before the end card must be quiet next to the voice, or the last word was clipped
    cut = dur - 4.45
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
        print(f"contact sheet: {sheet} (open it: captions readable and inside the safe zone, name right, last frame = logo end card)")
    for b in bad:
        print("FAIL:", b)
    print("QA " + ("FAILED" if bad else "passed (automatic checks; still look at the sheet)"))
    return 1 if bad else 0


def check():
    ok = True
    for tool in ("ffmpeg", "ffprobe"):
        if subprocess.run(["which", tool], capture_output=True).returncode:
            print(f"missing {tool}: install with  brew install ffmpeg  (no Homebrew? https://brew.sh)"); ok = False
    print("python deps ok" if ok else "")
    return 0 if ok else 1


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "check": sys.exit(check())
    elif c == "render" and len(sys.argv) > 2: render(sys.argv[2])
    elif c == "qa" and len(sys.argv) > 2: sys.exit(qa(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None))
    else: print(__doc__); sys.exit(2)
