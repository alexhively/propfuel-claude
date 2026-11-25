#!/usr/bin/env python3
"""Google Ads Keyword Planner volumes for the seo skill. Stdlib only.

  python3 kp.py "keyword one" "keyword two" > vols.csv
  python3 kp.py --file keywords.txt > vols.csv          one keyword per line
  python3 kp.py --ideas "seed keyword" > ideas.csv  related keyword ideas

Needs Basic API access on the Google Ads manager account (until approved the API returns
DEVELOPER_TOKEN_NOT_APPROVED). Credentials: <config dir>/google-ads.env and google-ads-adc.json,
where config dir = env SEO_CONFIG_DIR, default ~/.config/seo, falling back to ~/.config/propfuel
if it exists. US, English, Google Search. No keyword difficulty: judge from the SERP.
"""
import argparse, csv, json, os, sys, urllib.parse, urllib.request

def config_dir():
    d = os.environ.get("SEO_CONFIG_DIR")
    if d:
        return os.path.expanduser(d)
    legacy = os.path.expanduser("~/.config/propfuel")
    return legacy if os.path.isdir(legacy) else os.path.expanduser("~/.config/seo")


CFG = config_dir()
VERSION = "v23"  # bump when Google deprecates it (UNSUPPORTED_VERSION error)


def env():
    e = {}
    for line in open(f"{CFG}/google-ads.env"):
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            e[k] = v.strip().strip('"')
    return e


def token():
    d = json.load(open(f"{CFG}/google-ads-adc.json"))
    data = urllib.parse.urlencode({"client_id": d["client_id"], "client_secret": d["client_secret"],
                                   "refresh_token": d["refresh_token"], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data))["access_token"]


def call(method, body):
    e = env()
    cid = e["GOOGLE_ADS_CUSTOMER_ID"].replace("-", "")
    h = {"Authorization": "Bearer " + token(), "Content-Type": "application/json",
         "login-customer-id": e["GOOGLE_ADS_LOGIN_CUSTOMER_ID"].replace("-", ""),
         "x-goog-user-project": e.get("GOOGLE_CLOUD_PROJECT", "")}
    if e.get("GOOGLE_ADS_DEVELOPER_TOKEN"):
        h["developer-token"] = e["GOOGLE_ADS_DEVELOPER_TOKEN"]
    req = urllib.request.Request(f"https://googleads.googleapis.com/{VERSION}/customers/{cid}:{method}",
                                 json.dumps(body).encode(), h)
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as err:
        detail = json.load(err)["error"]
        codes = [x["errorCode"] for d in detail.get("details", []) for x in d.get("errors", [])]
        sys.exit(f"Google Ads API {err.code}: {codes or detail.get('message')}")


def row(text, m):
    bid = lambda k: round(int(m[k]) / 1e6, 2) if m.get(k) else ""
    return [text, m.get("avgMonthlySearches", 0), m.get("competition", ""), m.get("competitionIndex", ""),
            bid("lowTopOfPageBidMicros"), bid("highTopOfPageBidMicros")]


HEADER = ["keyword", "avg_monthly_searches", "competition", "competition_index", "cpc_low", "cpc_high"]
BASE = {"language": "languageConstants/1000", "geoTargetConstants": ["geoTargetConstants/2840"],
        "keywordPlanNetwork": "GOOGLE_SEARCH"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("keywords", nargs="*")
    p.add_argument("--file")
    p.add_argument("--ideas")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        r = row("example keyword", {"avgMonthlySearches": "70", "competition": "LOW", "competitionIndex": "12",
                                      "lowTopOfPageBidMicros": "2500000", "highTopOfPageBidMicros": "9120000"})
        assert r == ["example keyword", "70", "LOW", "12", 2.5, 9.12], r
        print("self-test OK"); return
    w = csv.writer(sys.stdout); w.writerow(HEADER)
    if a.ideas:
        res = call("generateKeywordIdeas", {**BASE, "keywordSeed": {"keywords": [a.ideas]}})
        for x in res.get("results", []):
            w.writerow(row(x["text"], x.get("keywordIdeaMetrics", {})))
        return
    kws = a.keywords + ([l.strip() for l in open(a.file) if l.strip()] if a.file else [])
    for i in range(0, len(kws), 1000):
        res = call("generateKeywordHistoricalMetrics", {**BASE, "keywords": kws[i:i + 1000]})
        for x in res.get("results", []):
            w.writerow(row(x["text"], x.get("keywordMetrics", {})))


if __name__ == "__main__":
    main()
