#!/usr/bin/env python3
"""
render_html_to_jpg.py — the one rendering routine every PropFuel HTML asset uses.

Pipeline (this exact recipe is what produced every approved pre-webinar banner):
  1. Load the HTML via file:// in headless Chromium (Playwright)
  2. Screenshot at device_scale_factor=2 (so a 1280x400 banner is captured at 2560x800)
  3. Downsample with PIL LANCZOS back to the exact target size
  4. Save as JPEG, quality=100, subsampling=0 (no chroma subsampling, keeps text crisp)

Why 2x then downsample: rendering at 1x produced visibly soft text on download (flagged
July 2026). Why downsample at all: Zoom rejects banners above 1280x1280, so the Zoom banner
MUST be delivered at exactly 1280x400, not the 2560x800 capture.

Usage:
  python3 render_html_to_jpg.py <input.html> <output.jpg> <width> <height>
  (also importable: render(html_path, out_path, w, h))
"""
import sys, os
from playwright.sync_api import sync_playwright
from PIL import Image


def render(html_path, out_path, width, height, scale=2, settle_ms=1500, return_metrics=False):
    html_path = os.path.abspath(html_path)
    tmp_png = out_path + ".2x.png"
    metrics = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height},
                                device_scale_factor=scale)
        page.goto("file://" + html_path)
        page.wait_for_timeout(settle_ms)  # let the local @font-face / fontconfig font settle
        if return_metrics:
            metrics = page.evaluate("""() => {
                const q = s => document.querySelector(s);
                const r = el => el ? el.getBoundingClientRect() : null;
                // Range-based right edge is the honest measure of where the TEXT ends
                // (the element box can be wider than the text it holds).
                const textRight = el => { if(!el) return null; const rg=document.createRange();
                    rg.selectNodeContents(el); return rg.getBoundingClientRect().right; };
                const h = q('.headline'), d = q('.divider'), sub = q('.subtitle');
                return {
                  headline_box: r(h), headline_text_right: textRight(h),
                  headline_font: h ? getComputedStyle(h).fontFamily : null,
                  headline_lines: h ? Math.round(h.getBoundingClientRect().height /
                                     parseFloat(getComputedStyle(h).lineHeight)) : null,
                  divider_box: r(d), subtitle_box: r(sub)
                };
            }""")
        page.screenshot(path=tmp_png)
        browser.close()
    im = Image.open(tmp_png).convert("RGB")
    if im.size != (width, height):
        im = im.resize((width, height), Image.LANCZOS)
    im.save(out_path, "JPEG", quality=100, subsampling=0)
    os.remove(tmp_png)
    return metrics if return_metrics else out_path


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__); sys.exit(1)
    html, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    m = render(html, out, w, h, return_metrics=True)
    print(f"wrote {out} ({w}x{h}); headline font = {m.get('headline_font')}; "
          f"lines = {m.get('headline_lines')}; text right = {m.get('headline_text_right')}")
