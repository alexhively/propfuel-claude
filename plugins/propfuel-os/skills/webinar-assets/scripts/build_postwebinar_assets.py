#!/usr/bin/env python3
"""
build_postwebinar_assets.py — builds the 3 PropFuel post-webinar (replay) assets from the Python templates.

  YouTube thumbnail          1280x720   template_yt_thumbnail_1280x720.py
  Website (resources) banner 1200x400   template_website_banner_1200x400.py
  PropFuel platform banner   2400x600   template_propfuel_banner_2400x600.py

The templates are pure PIL scripts with a CONFIG block at the top. This wrapper rewrites only the
CONFIG lines (TITLE, DATE, SPEAKER, TITLE_FONT_SIZE, USE_BLUE_GRADIENT, BUTTON_TEXT, HEADER_TEXT,
OUTPUT_FILE), copies propfuel_logo.png next to the script (the templates read "propfuel_logo.png"
from the current directory), ensures DM Sans is at /root/.local/share/fonts/DMSans.ttf (hard-coded
in the templates), runs each template, and copies the JPGs to the output folder.

Title font sizes: the templates default to 84 (YT), 52 (website), 110 (platform). Short titles can go
up; long titles must come down. Pass --font-scale 0.9 (or any factor) to scale all three at once, or
--yt-size / --web-size / --platform-size to set each individually. Look at the output and re-run.

Examples:
  python3 build_postwebinar_assets.py --title "How to Win Back Lapsed Members" --date "July 9, 2026" \
      --speaker "Brittany Lancor" --slug win_back
  python3 build_postwebinar_assets.py --title "..." --date "..." --speaker "..." --membership-ai   # blue steel title on YT
"""
import argparse, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = {
    "yt": ("template_yt_thumbnail_1280x720.py", "yt_thumbnail_{slug}_1280x720.jpg", 84),
    "web": ("template_website_banner_1200x400.py", "website_banner_{slug}_1200x400.jpg", 52),
    "platform": ("template_propfuel_banner_2400x600.py", "propfuel_banner_{slug}_2400x600.jpg", 110),
}


def set_cfg(src, name, value):
    """Replace a top-of-file CONFIG assignment, preserving the trailing comment if any."""
    pat = re.compile(rf'^{name}\s*=\s*.*$', re.M)
    rep = f'{name} = {value!r}' if isinstance(value, str) else f'{name} = {value}'
    if not pat.search(src):
        raise SystemExit(f"CONFIG line {name} not found in template")
    return pat.sub(rep, src, count=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True)
    ap.add_argument("--date", required=True, help='long form, e.g. "July 9, 2026" (post-webinar uses full month names)')
    ap.add_argument("--speaker", default="Brittany Lancor")
    ap.add_argument("--membership-ai", action="store_true", help="blue steel gradient title on the YouTube thumbnail")
    ap.add_argument("--font-scale", type=float, default=1.0)
    ap.add_argument("--yt-size", type=int); ap.add_argument("--web-size", type=int); ap.add_argument("--platform-size", type=int)
    ap.add_argument("--yt-button", default="Watch Now")
    ap.add_argument("--web-button", default="Watch Now")
    ap.add_argument("--platform-button", default="Webinar Replay")
    ap.add_argument("--platform-header", default="WATCH THE RECORDING")
    ap.add_argument("--only", nargs="*", choices=list(TEMPLATES), default=list(TEMPLATES))
    ap.add_argument("--slug", default=None)
    ap.add_argument("--templates", default=os.path.join(HERE, "..", "templates"))
    ap.add_argument("--work", default="/home/claude/postwebinar" if os.path.isdir("/home/claude") else "./out/work")
    ap.add_argument("--out", default="/mnt/user-data/outputs" if os.path.isdir("/mnt/user-data/outputs") else "./out")
    a = ap.parse_args()
    if not a.slug:
        a.slug = re.sub(r"[^a-z0-9]+", "_", a.title.lower()).strip("_")[:40]
    tdir = os.path.abspath(a.templates)
    if not os.path.isdir(tdir) and os.path.isdir("/mnt/project"):
        tdir = "/mnt/project"
    a.work, a.out = os.path.abspath(a.work), os.path.abspath(a.out)
    os.makedirs(a.work, exist_ok=True); os.makedirs(a.out, exist_ok=True)

    # font (templates hard-code /root/.local/share/fonts/DMSans.ttf)
    subprocess.run(["bash", os.path.join(HERE, "install_dmsans.sh")], check=False)
    font = os.path.expanduser("~/.local/share/fonts/DMSans.ttf")
    if os.path.isdir("/root/.local/share/fonts") and not os.path.isfile("/root/.local/share/fonts/DMSans.ttf"):
        try: shutil.copy(font, "/root/.local/share/fonts/DMSans.ttf")
        except OSError: pass
    font = "/root/.local/share/fonts/DMSans.ttf" if os.path.isfile("/root/.local/share/fonts/DMSans.ttf") else font

    # logo (templates read ./propfuel_logo.png; they strip the near-white background themselves)
    logo = os.path.join(tdir, "propfuel_logo.png")
    if not os.path.isfile(logo):
        raise SystemExit("propfuel_logo.png not found next to the templates. Re-upload it; do not recreate the logo.")
    shutil.copy(logo, os.path.join(a.work, "propfuel_logo.png"))

    sizes = {"yt": a.yt_size, "web": a.web_size, "platform": a.platform_size}
    delivered = []
    for key in a.only:
        fname, outpat, default_size = TEMPLATES[key]
        src = open(os.path.join(tdir, fname), encoding="utf-8").read()
        out_name = outpat.format(slug=a.slug)
        size = sizes[key] or int(round(default_size * a.font_scale))
        src = set_cfg(src, "FONT_PATH", font)
        src = set_cfg(src, "TITLE", a.title)
        src = set_cfg(src, "TITLE_FONT_SIZE", size)
        src = set_cfg(src, "OUTPUT_FILE", out_name)
        if key in ("yt", "web"):
            src = set_cfg(src, "DATE", a.date)
            src = set_cfg(src, "SPEAKER", a.speaker)
        if key == "yt":
            src = set_cfg(src, "USE_BLUE_GRADIENT", bool(a.membership_ai))
            src = set_cfg(src, "BUTTON_TEXT", a.yt_button)
        if key == "web":
            src = set_cfg(src, "BUTTON_TEXT", a.web_button)
        if key == "platform":
            src = set_cfg(src, "BUTTON_TEXT", a.platform_button)
            src = set_cfg(src, "HEADER_TEXT", a.platform_header)
        work_py = os.path.join(a.work, f"run_{key}.py")
        open(work_py, "w", encoding="utf-8").write(src)
        print(f"[{key}] title size {size}px ->", end=" ", flush=True)
        subprocess.run([sys.executable, work_py], cwd=a.work, check=True)
        final = os.path.join(a.out, out_name)
        shutil.copy(os.path.join(a.work, out_name), final)
        delivered.append(final)
    print("\nDelivered:")
    for d in delivered:
        print("  " + d)


if __name__ == "__main__":
    main()
