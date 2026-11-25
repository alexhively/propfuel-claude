#!/usr/bin/env python3
"""Raw-HTML SEO crawl (no JS). Usage:
  python3 -I crawl_check.py https://example.com/sitemap.xml [--limit 20] [--out crawl.csv]
  python3 -I crawl_check.py --self-test
What it sees is what GPTBot/ClaudeBot/PerplexityBot see: server HTML only.
shortcut: sequential fetch, no robots.txt or rate handling; fine for ~300 URLs, add threads if slower."""
import csv, json, re, sys, argparse, urllib.request, urllib.parse
from html.parser import HTMLParser

COLS = ["url", "status", "title", "title_len", "meta_description", "meta_len", "canonical",
        "robots_meta", "h1_count", "h1_text", "jsonld_types", "word_count", "internal_links_out"]
UA = {"User-Agent": "Mozilla/5.0 (compatible; SEOCheck/1.0)"}


class Page(HTMLParser):
    def __init__(self, host=""):
        super().__init__(convert_charrefs=True)
        self.host, self.title, self.desc, self.canon, self.robots = host, "", "", "", ""
        self.h1, self.ld, self.words, self.links = [], [], 0, 0
        self._tag, self._buf, self._skip, self._ld, self._body = None, "", 0, False, False

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag in ("script", "style", "noscript"):
            self._skip += 1
            self._ld = tag == "script" and a.get("type") == "application/ld+json"
            self._buf = ""
        elif tag in ("title", "h1"):
            self._tag, self._buf = tag, ""
        if tag == "body": self._body = True
        elif tag == "meta":
            n = (a.get("name") or "").lower()
            if n == "description": self.desc = a.get("content", "")
            if n == "robots": self.robots = a.get("content", "")
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower():
            self.canon = a.get("href", "")
        elif tag == "a":
            h = a.get("href") or ""
            if h and not h.startswith(("#", "mailto:", "tel:", "javascript:")):
                d = urllib.parse.urlparse(h).netloc
                if not d or d == self.host: self.links += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            if self._ld: self.ld.append(self._buf)
            self._skip, self._ld = max(0, self._skip - 1), False
        elif tag == self._tag:
            (self.h1.append(self._buf.strip()) if tag == "h1" else setattr(self, "title", self._buf.strip()))
            self._tag = None

    def handle_data(self, d):
        if self._skip: self._buf += d if self._ld else ""; return
        if self._tag: self._buf += d
        if self._body: self.words += len(d.split())


def types(blobs):
    out = []
    def walk(o):
        if isinstance(o, dict):
            t = o.get("@type")
            out.extend(t if isinstance(t, list) else [t] if t else [])
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    for b in blobs:
        try: walk(json.loads(b))
        except ValueError: out.append("INVALID_JSON")
    return sorted(set(out))


def analyze(url, status, html):
    p = Page(urllib.parse.urlparse(url).netloc)
    p.feed(html)
    return {"url": url, "status": status, "title": p.title, "title_len": len(p.title),
            "meta_description": p.desc, "meta_len": len(p.desc), "canonical": p.canon,
            "robots_meta": p.robots, "h1_count": len(p.h1), "h1_text": " | ".join(p.h1),
            "jsonld_types": ",".join(types(p.ld)), "word_count": p.words, "internal_links_out": p.links}


def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return "ERR " + type(e).__name__, ""


def sitemap_urls(url):
    _, xml = get(url)
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    if "<sitemapindex" in xml:
        return [u for s in locs for u in sitemap_urls(s)]
    return locs


def self_test():
    html = ('<html><head><title>Example Title</title><meta name="description" content="Desc here.">'
            '<link rel="canonical" href="https://x.com/a"><meta name="robots" content="noindex">'
            '<script type="application/ld+json">{"@graph":[{"@type":"WebPage"},{"@type":["FAQPage","Thing"]}]}</script>'
            '<script>var x="not counted words";</script></head><body><h1>Hello <b>World</b></h1><h1>Two</h1>'
            '<p>one two three</p><a href="/b">in</a><a href="https://x.com/c">in2</a><a href="https://o.com">out</a>'
            '<a href="#t">frag</a></body></html>')
    r = analyze("https://x.com/a", 200, html)
    assert r["title"] == "Example Title" and r["title_len"] == 13
    assert r["meta_description"] == "Desc here." and r["canonical"] == "https://x.com/a"
    assert r["robots_meta"] == "noindex" and r["h1_count"] == 2 and r["h1_text"] == "Hello World | Two"
    assert r["jsonld_types"] == "FAQPage,Thing,WebPage", r["jsonld_types"]
    assert r["word_count"] == 10, r["word_count"]  # body text only, script/title excluded
    assert r["internal_links_out"] == 2
    assert analyze("https://x.com/", 200, "<p>hi</p>")["title"] == ""
    print("self-test OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sitemap", nargs="?")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default="-")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test: self_test(); sys.exit()
    if not a.sitemap: ap.error("sitemap URL required")
    urls = sitemap_urls(a.sitemap)
    if a.limit: urls = urls[:a.limit]
    f = sys.stdout if a.out == "-" else open(a.out, "w", newline="")
    w = csv.DictWriter(f, COLS); w.writeheader()
    for u in urls:
        s, h = get(u)
        w.writerow(analyze(u, s, h))
