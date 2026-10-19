#!/usr/bin/env python3
"""Brand-rule lint for webinar copy. Usage: lint_copy.py file [file...]  (exit 1 on any hit)."""
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

if __name__ == "__main__":
    bad = 0
    for f in sys.argv[1:]:
        for h in lint(open(f, encoding="utf-8").read()):
            print(f"{f}: {h}"); bad = 1
    print("FAIL" if bad else "OK")
    sys.exit(bad)
