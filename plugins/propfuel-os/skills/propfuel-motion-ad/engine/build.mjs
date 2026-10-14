#!/usr/bin/env node
// propfuel-motion-ad engine: spec.json -> one HyperFrames project per cut x format.
// Every frame is drawn by HTML/CSS/GSAP. No video model, no stock, no AI imagery.
//
//   node build.mjs <spec.json> <outDir> [--cuts 15s,6s] [--formats 9x16,4x5,1x1,16x9]
//   node build.mjs <spec.json> <outDir> --test <cut>:<sceneIndex>[@secondsIntoScene] [--formats 1x1]
//
// Writes <outDir>/src/<cut>-<format>/ (index.html + assets + package.json + hyperframes.json).
// --test builds a 1-second project (src/test-<cut>-s<i>-<format>/) holding only that beat, playing the second
// that starts <secondsIntoScene> (default 0.3) after the beat starts: the "test the hardest second first" step.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const HF_VERSION = "0.8.150";

const args = process.argv.slice(2);
if (args.length < 2) {
  console.error("usage: node build.mjs <spec.json> <outDir> [--cuts 15s] [--formats 9x16,4x5]");
  process.exit(1);
}
const [specPath, outDir] = args;
const flag = (name) => {
  const i = args.indexOf(name);
  return i > -1 ? args[i + 1].split(",") : null;
};
const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
const FORMATS = JSON.parse(fs.readFileSync(path.join(HERE, "formats.json"), "utf8"));
const cuts = flag("--cuts") || Object.keys(spec.cuts);
const formats = flag("--formats") || ["9x16", "4x5"];

const esc = (s) =>
  String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const r2 = (n) => Math.round(n * 1000) / 1000;

// ---------- scene renderers: each returns { html, js } ----------
// js runs with `tl` in scope. Times are absolute seconds on the root timeline.

function inbox(sc, i) {
  const id = `s${i}`;
  const e = sc.email;
  const q = sc.question;
  // q.answers are the real labels; q.skeleton: n draws n grey bars when the case study doesn't list them verbatim
  const answers = q
    ? (q.answers || Array.from({ length: q.skeleton || 3 }, () => null))
        .map(
          (a, k) =>
            `<div class="ans${a === null ? " ans-sk" : ""}" id="${id}-a${k}"><span class="ans-dot"></span>${a === null ? `<span class="sk-bar" style="width:${[62, 48, 70, 55][k % 4]}%"></span>` : `<span class="ans-t">${esc(a)}</span>`}<span class="ans-check">&#10003;</span>${k === q.pick ? `<span class="tap" id="${id}-tap"></span>` : ""}</div>`,
        )
        .join("")
    : "";
  const html = `
  <section id="${id}" class="clip scene" data-start="${sc.start}" data-duration="${r2(sc.end - sc.start)}" data-track-index="1">
    <div class="card" id="${id}-card">
      <div class="mail-head">
        <div class="avatar">M</div>
        <div class="mail-meta"><div class="mail-from">${esc(e.from)}</div><div class="mail-to">to me</div></div>
      </div>
      <div class="mail-subject">${esc(e.subject)}</div>
      <div class="swap">
      <div class="mail-body" id="${id}-body">
        <p class="mail-p">${esc(e.body)}</p>
        ${
          e.rows || e.receipt
            ? `<div class="receipt" id="${id}-receipt">${(e.rows || [])
                .map((r) => `<div class="rc-row"><span>${esc(r[0])}</span><b>${esc(r[1])}</b></div>`)
                .join("")}${e.receipt ? `<div class="rc-stamp"><span class="receipt-i">&#10003;</span>${esc(e.receipt)}</div>` : ""}</div>`
            : ""
        }
      </div>
      ${
        q
          ? `<div class="q" id="${id}-q">
        <div class="q-text">${q.text ? esc(q.text) : `<span class="sk-bar sk-q"></span><span class="sk-bar sk-q sk-q2"></span>`}</div>
        <div class="answers">${answers}</div>
      </div>`
          : ""
      }
      </div>
    </div>
  </section>`;
  const s = sc.start;
  // A scene that opens the ad (start 0) is already on screen at frame 0: that frame is the poster/thumbnail.
  let js =
    s === 0
      ? ""
      : `
  tl.fromTo("#${id}-card", { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, ${r2(s + 0.05)});
  tl.fromTo("#${id}-body .mail-p", { opacity: 0 }, { opacity: 1, duration: 0.35 }, ${r2(s + 0.3)});`;
  if (e.receipt) js += `
  tl.fromTo("#${id} .rc-stamp", { scale: 0.6, opacity: 0, rotation: -8 }, { scale: 1, opacity: 1, rotation: -3, duration: 0.4, ease: "back.out(2.2)" }, ${r2(s + 0.7)});`;
  if (q) {
    const pa = q.at;
    js += `
  // hand-off, not a crossfade: the body is gone before the question arrives (overlapping text reads as a glitch)
  tl.to("#${id}-body", { opacity: 0, y: -20, duration: 0.2, ease: "power2.in" }, ${r2(pa)});
  tl.fromTo("#${id}-q", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(pa + 0.22)});
  tl.fromTo("#${id}-q .ans", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.3, stagger: 0.09, ease: "power2.out" }, ${r2(pa + 0.45)});
  tl.fromTo("#${id}-tap", { scale: 0.2, opacity: 0.55 }, { scale: 2.4, opacity: 0, duration: 0.5, ease: "power2.out", immediateRender: false }, ${r2(q.pickAt)});
  tl.to("#${id}-a${q.pick}", { backgroundColor: "#2F2F2F", color: "#F4F1EA", borderColor: "#2F2F2F", duration: 0.2 }, ${r2(q.pickAt + 0.05)});
  tl.fromTo("#${id}-a${q.pick} .ans-check", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, ${r2(q.pickAt + 0.12)});
  tl.to("#${id}-a${q.pick}", { scale: 0.97, duration: 0.08, yoyo: true, repeat: 1 }, ${r2(q.pickAt)});`;
  }
  js += `
  tl.to("#${id}-card", { opacity: 0, y: -40, duration: 0.3, ease: "power2.in" }, ${r2(sc.end - 0.32)});`;
  return { html, js };
}

// Number formatting shared by the static HTML and the count-up, so both print the same string.
// `comma: true` adds thousands separators (18,438); `decimals` fixes the places (38.3).
const fmtNum = (v, decimals, comma) => {
  const s = v.toFixed(decimals || 0);
  if (!comma) return s;
  const [a, b] = s.split(".");
  return a.replace(/\B(?=(\d{3})+(?!\d))/g, ",") + (b ? "." + b : "");
};

function stat(sc, i) {
  const id = `s${i}`;
  // dots: percent of the 100-dot grid to fill; null/undefined hides the grid (for counts that aren't a share)
  const hasDots = sc.dots !== null && sc.dots !== undefined;
  const dots = hasDots ? Array.from({ length: 100 }, (_, k) => `<i class="dot${k < sc.dots ? " on" : ""}"></i>`).join("") : "";
  // A stat that opens the ad (start 0, a stat-first hook) is the thumbnail: it shows its final value at frame 0.
  const opens = sc.start === 0;
  const initial = opens ? fmtNum(sc.value, sc.decimals, sc.comma) : fmtNum(0, sc.decimals, sc.comma);
  const html = `
  <section id="${id}" class="clip scene stat" data-start="${sc.start}" data-duration="${r2(sc.end - sc.start)}" data-track-index="1">
    <div class="stat-wrap" id="${id}-wrap">
      <div class="stat-num${sc.size ? " " + esc(sc.size) : ""}">${sc.prefix ? `<span class="g">${esc(sc.prefix)}</span>` : ""}<span class="g" id="${id}-n">${initial}</span><span class="g">${esc(sc.suffix || "")}</span></div>
      <div class="stat-label">${esc(sc.label)}</div>
      ${hasDots ? `<div class="dots" id="${id}-dots">${dots}</div>` : ""}
      <div class="stat-sub" id="${id}-sub">${esc(sc.sub)}</div>
      <div class="stat-src" id="${id}-src">${esc(sc.source)}</div>
    </div>
  </section>`;
  const s = sc.start;
  const js = opens
    ? `
  tl.to("#${id}-wrap", { opacity: 0, y: -30, duration: 0.3, ease: "power2.in" }, ${r2(sc.end - 0.32)});`
    : `
  (function(){
    const n = document.getElementById("${id}-n"); const o = { v: 0 };
    const f = (v) => { const s = v.toFixed(${sc.decimals || 0}); ${sc.comma ? `const p = s.split("."); return p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, ",") + (p[1] ? "." + p[1] : "");` : "return s;"} };
    tl.fromTo("#${id} .stat-num", { scale: 0.86, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "power3.out" }, ${r2(s + 0.05)});
    tl.fromTo(o, { v: 0 }, { v: ${sc.value}, duration: 1.3, ease: "power2.out", onUpdate: () => { n.textContent = f(o.v); } }, ${r2(s + 0.1)});
    tl.fromTo("#${id} .stat-label", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.35 }, ${r2(s + 0.35)});
    ${hasDots ? `tl.fromTo("#${id} .dot", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.18, stagger: 0.008, ease: "power2.out" }, ${r2(s + 0.45)});` : ""}
    tl.fromTo("#${id}-sub", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.35 }, ${r2(s + 1.2)});
    tl.fromTo("#${id}-src", { opacity: 0 }, { opacity: 1, duration: 0.35 }, ${r2(s + 1.5)});
    tl.to("#${id}-wrap", { opacity: 0, y: -30, duration: 0.3, ease: "power2.in" }, ${r2(sc.end - 0.32)});
  })();`;
  return { html, js };
}

function quote(sc, i) {
  const id = `s${i}`;
  const html = `
  <section id="${id}" class="clip scene quote" data-start="${sc.start}" data-duration="${r2(sc.end - sc.start)}" data-track-index="1">
    <div class="quote-wrap" id="${id}-wrap">
      <div class="quote-mark">&ldquo;</div>
      <div class="quote-t">${esc(sc.text)}</div>
      <div class="quote-by"><b>${esc(sc.name)}</b>${esc(sc.role)}</div>
    </div>
  </section>`;
  const s = sc.start;
  const js = `
  tl.fromTo("#${id}-wrap", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, ${r2(s + 0.05)});
  tl.fromTo("#${id} .quote-by", { opacity: 0 }, { opacity: 1, duration: 0.35 }, ${r2(s + 0.6)});
  tl.to("#${id}-wrap", { opacity: 0, duration: 0.3 }, ${r2(sc.end - 0.32)});`;
  return { html, js };
}

function cta(sc, i, spec) {
  const id = `s${i}`;
  const c = spec.cta;
  const words = c.headline
    .split(" ")
    .map((w) => `<span class="w">${esc(w)}</span>`)
    .join(" ");
  const html = `
  <section id="${id}" class="clip scene cta full" data-start="${sc.start}" data-duration="${r2(sc.end - sc.start)}" data-track-index="2">
    <div class="cta-wrap">
      <img class="cta-logo" id="${id}-logo" src="assets/propfuel-logo.png" alt="PropFuel" />
      <div class="cta-h">${words}</div>
      <div class="btn" id="${id}-btn">${esc(c.button)} <span class="btn-arrow">&rarr;</span></div>
      <div class="cta-url" id="${id}-url">${esc(c.url)}</div>
      <div class="cta-tag" id="${id}-tag">${esc(c.tagline)}</div>${c.sub ? `
      <div class="cta-tag cta-sub" id="${id}-sub">${esc(c.sub)}</div>` : ""}
    </div>
  </section>`;
  const s = sc.start;
  const len = sc.end - sc.start;
  const pulses = [];
  for (let t = s + 2.2; t < sc.end - 0.8; t += 1.8) pulses.push(r2(t));
  const js = `
  tl.fromTo("#${id}-logo", { scale: 0.8, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.6)" }, ${r2(s + 0.05)});
  tl.fromTo("#${id} .cta-h .w", { opacity: 0, y: 28 }, { opacity: 1, y: 0, duration: 0.4, stagger: 0.07, ease: "power3.out" }, ${r2(s + 0.3)});
  tl.fromTo("#${id}-btn", { opacity: 0, y: 20, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, ${r2(s + Math.min(0.75, len * 0.3))});
  tl.fromTo("#${id}-url", { opacity: 0 }, { opacity: 1, duration: 0.35 }, ${r2(s + Math.min(1.0, len * 0.35))});
  tl.fromTo("#${id}-tag", { opacity: 0 }, { opacity: 1, duration: 0.35 }, ${r2(s + Math.min(1.25, len * 0.4))});${c.sub ? `
  tl.fromTo("#${id}-sub", { opacity: 0 }, { opacity: 1, duration: 0.35 }, ${r2(s + Math.min(1.4, len * 0.45))});` : ""}
  ${pulses.map((t) => `tl.to("#${id}-btn", { scale: 1.045, duration: 0.22, yoyo: true, repeat: 1, ease: "sine.inOut" }, ${t});`).join("\n  ")}`;
  return { html, js };
}

// popup: a website (skeleton page in a browser frame, real domain in the URL bar) and the PropFuel
// Website Engagement pop-up that asks one question on it. `question.answers` are the real labels; when the
// case study doesn't list them verbatim, pass `question.skeleton: n` and n grey bars are drawn instead
// (never invent answer text). `question.pick` + `pickAt` tap one.
function popup(sc, i) {
  const id = `s${i}`;
  const q = sc.question;
  const labels = q.answers || Array.from({ length: q.skeleton || 3 }, () => null);
  const answers = labels
    .map(
      (a, k) =>
        `<div class="ans${a === null ? " ans-sk" : ""}" id="${id}-a${k}"><span class="ans-dot"></span>${a === null ? `<span class="sk-bar" style="width:${[62, 48, 70, 55][k % 4]}%"></span>` : `<span class="ans-t">${esc(a)}</span>`}<span class="ans-check">&#10003;</span>${k === q.pick ? `<span class="tap" id="${id}-tap"></span>` : ""}</div>`,
    )
    .join("");
  const html = `
  <section id="${id}" class="clip scene" data-start="${sc.start}" data-duration="${r2(sc.end - sc.start)}" data-track-index="1">
    <div class="browser" id="${id}-card">
      <div class="br-bar"><i></i><i></i><i></i><span class="br-url">${esc(sc.site)}</span></div>
      <div class="br-page">
        <div class="sk sk-h"></div><div class="sk"></div><div class="sk sk-s"></div>
        <div class="sk-grid"><div></div><div></div><div></div></div>
        <div class="sk"></div><div class="sk sk-s"></div>
        <div class="pop" id="${id}-q">
          <div class="pop-text">${esc(q.text)}</div>
          <div class="answers">${answers}</div>
        </div>
      </div>
    </div>
  </section>`;
  const s = sc.start;
  let js =
    s === 0
      ? ""
      : `
  tl.fromTo("#${id}-card", { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, ${r2(s + 0.05)});`;
  js += `
  tl.fromTo("#${id}-q", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.4)", immediateRender: ${s === 0 && q.at === 0 ? "false" : "true"} }, ${r2(q.at)});
  tl.fromTo("#${id}-q .ans", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.3, stagger: 0.09, ease: "power2.out" }, ${r2(q.at + 0.3)});`;
  if (q.pick !== undefined) {
    js += `
  tl.fromTo("#${id}-tap", { scale: 0.2, opacity: 0.55 }, { scale: 2.4, opacity: 0, duration: 0.5, ease: "power2.out", immediateRender: false }, ${r2(q.pickAt)});
  tl.to("#${id}-a${q.pick}", { backgroundColor: "#2F2F2F", color: "#F4F1EA", borderColor: "#2F2F2F", duration: 0.2 }, ${r2(q.pickAt + 0.05)});
  ${q.answers ? "" : `tl.to("#${id}-a${q.pick} .sk-bar", { backgroundColor: "#8A8A8A", duration: 0.2 }, ${r2(q.pickAt + 0.05)});`}
  tl.fromTo("#${id}-a${q.pick} .ans-check", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, ${r2(q.pickAt + 0.12)});
  tl.to("#${id}-a${q.pick}", { scale: 0.97, duration: 0.08, yoyo: true, repeat: 1 }, ${r2(q.pickAt)});`;
  }
  js += `
  tl.to("#${id}-card", { opacity: 0, y: -40, duration: 0.3, ease: "power2.in" }, ${r2(sc.end - 0.32)});`;
  return { html, js };
}

const SCENES = { inbox, stat, quote, cta, popup };
// Product-UI beats (AI Campaign Builder, Signals, segments, Home, Initiatives...) + their CSS: scenes-product.mjs
const PRODUCT = await import("./scenes-product.mjs");
Object.assign(SCENES, PRODUCT.SCENES);
// Effect beats on vendored open-source libraries (stack, sketch, brush, filter, orb, words) + CSS + vendor list
const FX = await import("./scenes-fx.mjs");
Object.assign(SCENES, FX.SCENES);
const vendorFor = (scenes) => [...new Set(scenes.flatMap((sc) => FX.VENDOR[sc.type] || []))];

function captionsHtml(caps) {
  return caps
    .map(
      (c, k) => `
    <div id="c${k}" class="clip cap" data-start="${c.start}" data-duration="${r2(c.end - c.start)}" data-track-index="3">
      <div class="cap-in" id="c${k}-in">${c.eyebrow ? `<div class="eyebrow">${esc(c.eyebrow)}</div>` : ""}<div class="cap-t">${esc(c.text)}</div></div>
    </div>`,
    )
    .join("");
}
function captionsJs(caps) {
  return caps
    .map(
      (c, k) => `
${c.start === 0 ? "" : `
  tl.fromTo("#c${k}-in", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(c.start + 0.05)});`}
  tl.to("#c${k}-in", { opacity: 0, y: -16, duration: 0.25, ease: "power2.in" }, ${r2(c.end - 0.27)});`,
    )
    .join("");
}

function page(cut, fmtKey, test) {
  const f = FORMATS[fmtKey];
  const C = test ? test.cut : spec.cuts[cut];
  const built = C.scenes.map((sc, i) => {
    if (!SCENES[sc.type]) throw new Error(`unknown scene type "${sc.type}"`);
    return SCENES[sc.type](sc, i, spec);
  });
  // test build: the beat's clip covers the whole 1s composition; its tweens keep their real times (see __fxT0)
  if (test) built[0].html = built[0].html.replace(/data-start="[^"]*" data-duration="[^"]*"/, `data-start="0" data-duration="${C.duration}"`);
  const ctaStart = (C.scenes.find((s) => s.type === "cta") || { start: C.duration }).start;
  const tpl = fs.readFileSync(path.join(HERE, "template.html"), "utf8");
  const vendor = vendorFor(C.scenes).map((v) => `\n    <script src="assets/${v}"></script>`).join("");
  return tpl
    .replace("</style>", () => PRODUCT.CSS + FX.CSS + "    </style>")
    .replace("{{VENDOR}}", () => vendor)
    .replace("{{T0}}", test ? r2(test.t0) : 0)
    .replaceAll("{{W}}", f.w)
    .replaceAll("{{H}}", f.h)
    .replaceAll("{{U}}", f.u)
    .replaceAll("{{FMT}}", fmtKey)
    .replaceAll("{{LAYOUT}}", f.layout)
    .replaceAll("{{SAFE_T}}", f.safe.top)
    .replaceAll("{{SAFE_B}}", f.safe.bottom)
    .replaceAll("{{SAFE_L}}", f.safe.left)
    .replaceAll("{{SAFE_R}}", f.safe.right)
    .replaceAll("{{DURATION}}", C.duration)
    .replaceAll("{{TITLE}}", esc(`${spec.slug} ${cut} ${fmtKey}`))
    .replace("{{BUG_DURATION}}", r2(ctaStart))
    .replace("{{CAPTIONS}}", () => captionsHtml(C.captions || []))
    .replace("{{SCENES}}", () => built.filter((b, i) => C.scenes[i].type !== "cta").map((b) => b.html).join(""))
    .replace("{{FULL}}", () => built.filter((b, i) => C.scenes[i].type === "cta").map((b) => b.html).join(""))
    .replace("{{TIMELINE}}", () => captionsJs(C.captions || []) + built.map((b) => b.js).join(""));
}

function copy(src, dst) {
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.copyFileSync(src, dst);
}

// --test <cut>:<i>[@s]: one beat, one second, no captions
const testArg = flag("--test");
const jobs = [];
if (testArg) {
  const m = testArg[0].match(/^([^:]+):(\d+)(?:@([\d.]+))?$/);
  if (!m || !spec.cuts[m[1]] || !spec.cuts[m[1]].scenes[+m[2]]) throw new Error(`--test wants <cut>:<sceneIndex>[@seconds], got "${testArg[0]}"`);
  const sc = spec.cuts[m[1]].scenes[+m[2]];
  const t0 = Math.min(sc.start + (m[3] !== undefined ? +m[3] : 0.3), sc.end - 1);
  const test = { t0: Math.max(t0, 0.001), cut: { duration: 1, captions: [], scenes: [sc] } };
  for (const fmt of flag("--formats") || ["1x1"]) jobs.push({ cut: m[1], fmt, test, name: `test-${m[1]}-s${m[2]}-${fmt}` });
} else {
  for (const cut of cuts) {
    if (!spec.cuts[cut]) throw new Error(`spec has no cut "${cut}"`);
    for (const fmt of formats) jobs.push({ cut, fmt, name: `${cut}-${fmt}` });
  }
}

for (const { cut, fmt, test, name } of jobs) {
  {
    if (!FORMATS[fmt]) throw new Error(`unknown format "${fmt}"`);
    const dir = path.join(outDir, "src", name);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, "index.html"), page(cut, fmt, test));
    for (const v of vendorFor((test ? test.cut : spec.cuts[cut]).scenes)) copy(path.join(HERE, "vendor", v), path.join(dir, "assets", v));
    copy(path.join(HERE, "assets/DMSans-Variable.ttf"), path.join(dir, "assets/DMSans-Variable.ttf"));
    copy(path.join(HERE, "assets/propfuel-logo.png"), path.join(dir, "assets/propfuel-logo.png"));
    copy(path.join(HERE, "vendor/gsap.min.js"), path.join(dir, "assets/gsap.min.js"));
    fs.writeFileSync(
      path.join(dir, "hyperframes.json"),
      JSON.stringify({ $schema: "https://hyperframes.heygen.com/schema/hyperframes.json", paths: { assets: "assets" } }, null, 2),
    );
    fs.writeFileSync(
      path.join(dir, "package.json"),
      JSON.stringify(
        {
          name: `${spec.slug}-${name}`,
          private: true,
          type: "module",
          scripts: {
            check: `npx --yes hyperframes@${HF_VERSION} check`,
            render: `npx --yes hyperframes@${HF_VERSION} render`,
          },
        },
        null,
        2,
      ),
    );
    console.log(`built ${dir}`);
  }
}
