#!/usr/bin/env python3
"""Brand-rule lint for webinar copy. Usage: lint_copy.py [--allow-no-proof] file [file...]  (exit 1 on any hit).
Promo files (email, linkedin, slack, popup, ad in the file name) must carry a proof line; zoom/recording files are exempt."""
import re, sys

RULES = [
    (r"—|–", "em/en dash"),
    (r"8\.68", "retired 8.68% stat"),
    (r"\bagain\b|back by popular demand", "repeat language"),
    (r"Session \d+ of \d+", "session count"),
    (r"Mark your calendar", "retired phrase"),
    (r"FelineVMA", "FelineVMA must stay anonymous in outward copy"),
]

def lint(text):
    hits = [(m, why) for pat, why in RULES for m in [re.search(pat, text, re.I)] if m]
    out = [f"{why}: '{m.group(0)}'" for m, why in hits]
    for m in re.finditer(r"12\s?%", text):
        if "0.98" not in text[max(0, m.start() - 200): m.end() + 200]:
            out.append("12% stat without 'vs 0.98% for the average association' nearby")
    if re.search(r"\b\d+\+? associations", text) and not re.search(r"370\+ associations", text):
        out.append("association count must be '370+ associations'")
    return out

PROOF_URL = r"propfuel\.com/case-studies/[a-z0-9-]+"
PROMO = re.compile(r"email|linkedin|slack|popup|promo|(^|[_-])ads?([_.-]|$)", re.I)  # promo pieces must carry proof; zoom/recording must not

def proof_issue(name, text):
    """Alex, Oct 19 2026: every promo carries the premier case study proof from Webinar Proof Map.md."""
    base = name.rsplit("/", 1)[-1]
    if re.search(r"zoom|recording", base, re.I) or not PROMO.search(base):
        return None
    if not re.search(PROOF_URL, text):
        return "promo piece has no proof line: add the premier case study stat and its propfuel.com/case-studies/ link (Webinar Proof Map.md), or pass --allow-no-proof for a GAP row"
    return None

if __name__ == "__main__":
    args = sys.argv[1:]
    allow = "--allow-no-proof" in args
    files = [a for a in args if not a.startswith("--")]
    bad = 0
    for f in files:
        text = open(f, encoding="utf-8").read()
        hits = lint(text)
        if not allow and (h := proof_issue(f, text)):
            hits.append(h)
        for h in hits:
            print(f"{f}: {h}"); bad = 1
    print("FAIL" if bad else "OK")
    sys.exit(bad)
