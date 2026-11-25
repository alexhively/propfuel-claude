#!/usr/bin/env python3
"""Google Search Console for the seo skill. Stdlib only.

  python3 gsc.py auth                      one-time browser consent; saves ~/.config/propfuel/gsc.json (600)
  python3 gsc.py sites                     list properties this login can read
  python3 gsc.py query --site sc-domain:propfuel.com --start 2026-10-01 --end 2026-10-31 \
      [--dims query,page] [--limit 1000] [--contains "member"] > out.csv

OAuth client: any Desktop-type client JSON with client_id/client_secret. Default is the one in
~/.config/propfuel/google-ads-adc.json (PropFuel GCP project); override with --client <file>.
The Search Console API must be enabled in that client's GCP project.
"""
import argparse, csv, http.server, json, os, sys, urllib.parse, urllib.request, webbrowser

CFG = os.path.expanduser("~/.config/propfuel/gsc.json")
DEFAULT_CLIENT = os.path.expanduser("~/.config/propfuel/google-ads-adc.json")
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
API = "https://searchconsole.googleapis.com/webmasters/v3"


def post(url, data):
    return json.load(urllib.request.urlopen(url, urllib.parse.urlencode(data).encode()))


def auth(client_file):
    c = json.load(open(client_file))
    cid, secret = c["client_id"], c["client_secret"]
    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            got.update(urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query))
            self.send_response(200); self.end_headers()
            self.wfile.write(b"Search Console connected. You can close this tab.")
        def log_message(self, *a): pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    redirect = f"http://127.0.0.1:{srv.server_port}"
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cid, "redirect_uri": redirect, "response_type": "code", "scope": SCOPE,
        "access_type": "offline", "prompt": "consent"})
    print("Opening the Google consent page. If it does not open, visit:\n" + url, file=sys.stderr)
    webbrowser.open(url)
    while "code" not in got and "error" not in got:
        srv.handle_request()
    if "error" in got:
        sys.exit(f"consent failed: {got['error'][0]}")
    tok = post("https://oauth2.googleapis.com/token", {"code": got["code"][0], "client_id": cid,
               "client_secret": secret, "redirect_uri": redirect, "grant_type": "authorization_code"})
    fd = os.open(CFG, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump({"client_id": cid, "client_secret": secret, "refresh_token": tok["refresh_token"]}, f)
    print("saved", CFG, file=sys.stderr)


def call(path, body=None):
    c = json.load(open(CFG))
    access = post("https://oauth2.googleapis.com/token", {**c, "grant_type": "refresh_token"})["access_token"]
    req = urllib.request.Request(API + path, json.dumps(body).encode() if body else None,
                                 {"Authorization": "Bearer " + access, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


def rows_to_csv(rows, dims, out):
    w = csv.writer(out)
    w.writerow(dims + ["clicks", "impressions", "ctr", "position"])
    for r in rows:
        w.writerow(r["keys"] + [r["clicks"], r["impressions"], round(r["ctr"], 4), round(r["position"], 1)])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["auth", "sites", "query", "self-test"])
    p.add_argument("--client", default=DEFAULT_CLIENT)
    p.add_argument("--site"); p.add_argument("--start"); p.add_argument("--end")
    p.add_argument("--dims", default="query"); p.add_argument("--limit", type=int, default=1000)
    p.add_argument("--contains")
    a = p.parse_args()
    if a.cmd == "auth":
        auth(a.client)
    elif a.cmd == "sites":
        for s in call("/sites").get("siteEntry", []):
            print(s["siteUrl"], s["permissionLevel"])
    elif a.cmd == "query":
        dims = a.dims.split(",")
        body = {"startDate": a.start, "endDate": a.end, "dimensions": dims, "rowLimit": a.limit}
        if a.contains:
            body["dimensionFilterGroups"] = [{"filters": [{"dimension": dims[0], "operator": "contains", "expression": a.contains}]}]
        rows_to_csv(call(f"/sites/{urllib.parse.quote(a.site, safe='')}/searchAnalytics/query", body).get("rows", []), dims, sys.stdout)
    else:
        import io
        buf = io.StringIO()
        rows_to_csv([{"keys": ["member engagement software"], "clicks": 3, "impressions": 120, "ctr": 0.025, "position": 4.83}], ["query"], buf)
        assert buf.getvalue().splitlines()[1] == "member engagement software,3,120,0.025,4.8", buf.getvalue()
        print("self-test OK")


if __name__ == "__main__":
    main()
