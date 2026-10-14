// propfuel-motion-ad: product-UI beats, recreated in code from the real PropFuel screens.
// Loaded by build.mjs (SCENES + CSS). Same contract as the beats there: each renderer returns { html, js },
// js runs with `tl` in scope, times are absolute seconds, static end-state HTML + tl.fromTo from-states,
// `immediateRender: false` on anything that starts after its element is first visible.
//
// Labels come from the real UI (AI Campaign Builder demo-call frames + the Membership AI page hero):
// "MEMBERSHIP AI · CAMPAIGN BUILDER", "Describe the campaign", "A sentence, or your whole plan — questions,
// workflows, timing", "Searching campaigns…", "Before I build the plan", "Here's the full plan", "Plan approval",
// "Does this plan look right? Any check-ins you'd like to adjust before I start building?", "Build it",
// "Let me change something", "Draft ready. Review and launch.", "Checked as it built",
// "Ask a question or change anything…", "The builder is working…". Every window that shows example data
// carries a "Sample" tag.

const esc = (s) =>
  String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const r2 = (n) => Math.round(n * 1000) / 1000;
const J = (v) => JSON.stringify(v);

const SPARK = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2c.6 4.8 2.9 7.4 8 8-5.1.6-7.4 3.2-8 8-.6-4.8-2.9-7.4-8-8 5.1-.6 7.4-3.2 8-8z" fill="currentColor"/></svg>`;
const UP = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const CHECK = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6 9 17l-5-5" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

// window chrome shared by every product beat
function win(id, kicker, title, tag, inner, extra = "") {
  return `<div class="win" id="${id}-win">
      <div class="win-bar"><div class="win-k"><i class="spk">${SPARK}</i>${esc(kicker)}</div>${
        title ? `<div class="win-t" id="${id}-title">${esc(title)}</div>` : ""
      }${tag ? `<em class="win-tag">${esc(tag)}</em>` : ""}</div>
      ${inner}${extra}
    </div>`;
}
const section = (id, sc, inner, cls = "") =>
  `<section id="${id}" class="clip scene ${cls}" data-start="${sc.start}" data-duration="${r2(sc.end - sc.start)}" data-track-index="1">${inner}</section>`;
// enter (skipped for a beat that opens the ad: frame 0 is the thumbnail) + exit
const enter = (id, s) =>
  s === 0 ? "" : `\n  tl.fromTo("#${id}-win", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, ${r2(s + 0.05)});`;
const exit = (id, sc) =>
  sc.hold ? "" : `\n  tl.to("#${id}-win", { opacity: 0, y: -36, duration: 0.3, ease: "power2.in" }, ${r2(sc.end - 0.32)});`;
const tap = (sel, t) =>
  `\n  tl.fromTo("${sel}", { scale: 0.2, opacity: 0.5 }, { scale: 2.4, opacity: 0, duration: 0.5, ease: "power2.out", immediateRender: false }, ${r2(t)});`;
// typewriter: deterministic (driven by the paused timeline, not a clock)
const typeJs = (elId, text, pre, t0, t1) => `
  (function(){ const el = document.getElementById("${elId}"); const T = ${J(text)}; const o = { n: ${pre} };
    tl.fromTo(o, { n: ${pre} }, { n: T.length, duration: ${r2(t1 - t0)}, ease: "none", immediateRender: false, onUpdate: () => { el.textContent = T.slice(0, Math.round(o.n)); } }, ${r2(t0)}); })();`;

// ---------- builder: the AI Campaign Builder, screen by screen ----------
// sc.screens[]: { kind: describe|thinking|clarify|plan|approve|ready, at, ... }. Each screen holds until the next.
function builderScreen(id, x, k) {
  const sid = `${id}-x${k}`;
  switch (x.kind) {
    case "describe": {
      const pre = x.pre || 0;
      return `<div class="bs bs-describe" id="${sid}">
        <div class="d-head"><i class="d-ico">${SPARK}</i><div><div class="d-h">Describe the campaign</div><div class="d-s">A sentence, or your whole plan — questions, workflows, timing</div></div></div>
        <div class="d-box"><p class="d-p"><span id="${sid}-t">${esc(x.text.slice(0, pre))}</span><i class="caret" id="${sid}-c"></i></p><i class="go d-go" id="${sid}-go">${UP}</i></div>
      </div>`;
    }
    case "thinking":
      return `<div class="bs" id="${sid}"><div class="feed">
        ${x.me ? `<p class="me">${esc(x.me)}</p>` : ""}
        <p class="st"><i class="st-dot" id="${sid}-d"></i>${esc(x.text || "Searching campaigns…")}</p>
      </div></div>`;
    case "clarify":
      return `<div class="bs" id="${sid}"><div class="feed"><div class="cardk">
        <b class="kk">Before I build the plan</b><p class="ck-p">A couple of quick things I need from you:</p>
        ${x.items.map((q, j) => `<div class="ck-q"><span>${esc(q[0])}</span><em class="ck-a" id="${sid}-a${j}">${esc(q[1])}</em></div>`).join("")}
      </div></div></div>`;
    case "plan":
      return `<div class="bs" id="${sid}"><div class="feed">
        <div class="pl-head"><b class="kk">Here's the full plan</b><p class="pl-n">${esc(x.name)}</p><p class="pl-m">${esc(x.meta)}</p></div>
        <div class="rows">${x.rows
          .map(
            (r, j) => `<div class="row" id="${sid}-r${j}"><b class="day">${esc(r.d)}</b><div class="row-b"><p class="row-q">${esc(r.q)}</p>${
              r.act ? `<small class="row-a">&rarr; ${esc(r.act)}</small>` : ""
            }${
              r.br
                ? `<div class="brs">${r.br.map((b) => `<span class="brc"><b>${esc(b[0])}</b><small>&rarr; ${esc(b[1])}</small></span>`).join("")}</div>`
                : ""
            }</div></div>`,
          )
          .join("")}</div>
      </div></div>`;
    case "approve":
      return `<div class="bs" id="${sid}"><div class="feed">
        ${x.name ? `<div><p class="pl-n">${esc(x.name)}</p><p class="pl-m">${esc(x.meta || "")}</p></div>` : ""}
        <div class="cardk ap">
          <b class="kk">Plan approval</b>
          <p class="ap-q">Does this plan look right? Any check-ins you'd like to adjust before I start building?</p>
          <div class="opt" id="${sid}-o0"><i class="radio"><i id="${sid}-dot"></i></i><div><b>Build it</b><small>Looks good — start creating the campaign.</small></div><span class="tap" id="${sid}-tap"></span></div>
          <div class="opt"><i class="radio"></i><div><b>Let me change something</b><small>I want to adjust the plan first.</small></div></div>
        </div>
      </div></div>`;
    case "ready":
      return `<div class="bs" id="${sid}"><div class="feed">
        ${x.name ? `<div><p class="pl-n">${esc(x.name)}</p><p class="pl-m">${esc(x.meta || "")}</p></div>` : ""}
        <div class="ready" id="${sid}-ok"><i class="ok-i">${CHECK}</i><div><b>${esc(x.text || "Draft ready. Review and launch.")}</b><small>${esc(x.sub || "Checked as it built")}</small></div></div>
        ${
          x.chips
            ? `<div class="chips-l">${esc(x.chipsLabel || "In the draft")}</div><div class="chips">${x.chips.map((c) => `<span class="chip">${esc(c)}</span>`).join("")}</div>`
            : ""
        }
      </div></div>`;
  }
  throw new Error(`unknown builder screen ${x.kind}`);
}

function builderJs(id, x, k, sc) {
  const sid = `${id}-x${k}`;
  let js = "";
  if (x.kind === "describe") {
    const t0 = x.typeAt ?? x.at + 0.2;
    const t1 = x.typeEnd ?? t0 + x.text.length * 0.024;
    js += typeJs(`${sid}-t`, x.text, x.pre || 0, t0, t1);
    js += `\n  tl.to("#${sid}-c", { opacity: 0, duration: 0.25, repeat: ${Math.max(1, Math.floor((t1 - x.at) / 0.25))}, yoyo: true, ease: "steps(1)" }, ${r2(x.at)});`;
    if (x.sendAt) {
      js += `\n  tl.set("#${sid}-c", { opacity: 0 }, ${r2(x.sendAt)});`;
      js += `\n  tl.to("#${sid}-go", { scale: 0.82, duration: 0.1, yoyo: true, repeat: 1 }, ${r2(x.sendAt)});`;
    }
  }
  if (x.kind === "thinking") {
    js += `\n  tl.to("#${sid}-d", { opacity: 0.25, scale: 0.7, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }, ${r2(x.at + 0.3)});`;
  }
  if (x.kind === "clarify") {
    x.items.forEach((_, j) => {
      js += `\n  tl.fromTo("#${sid}-a${j}", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, ${r2(x.answerAt[j])});`;
    });
  }
  if (x.kind === "plan") {
    const step = x.step || 0.4;
    x.rows.forEach((r, j) => {
      const t = x.at + 0.45 + j * step + (j > 0 && x.rows[0].br ? x.rows[0].br.length * 0.1 : 0);
      js += `\n  tl.fromTo("#${sid}-r${j}", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(t)});`;
      if (r.br) js += `\n  tl.fromTo("#${sid}-r${j} .brc", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, stagger: 0.1, ease: "power2.out" }, ${r2(t + 0.25)});`;
    });
  }
  if (x.kind === "approve" && x.pickAt) {
    js += tap(`#${sid}-tap`, x.pickAt);
    js += `\n  tl.to("#${sid}-o0", { backgroundColor: "#EAF0F6", borderColor: "#3B6A8C", duration: 0.2 }, ${r2(x.pickAt + 0.05)});`;
    js += `\n  tl.fromTo("#${sid}-dot", { scale: 0 }, { scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }, ${r2(x.pickAt + 0.08)});`;
    js += `\n  tl.to("#${sid}-o0", { scale: 0.98, duration: 0.08, yoyo: true, repeat: 1 }, ${r2(x.pickAt)});`;
  }
  if (x.kind === "ready") {
    if (k > 0 || sc.start > 0)
      js += `\n  tl.fromTo("#${sid}-ok", { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, ${r2(x.at + 0.35)});`;
    if (x.chips)
      js += `\n  tl.fromTo("#${sid} .chip", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.25, stagger: 0.09, ease: "power2.out" }, ${r2(x.at + 0.7)});`;
  }
  return js;
}

function builder(sc, i) {
  const id = `s${i}`;
  const S = sc.screens;
  const opensWithDescribe = S[0].kind === "describe";
  const screens = S.map((x, k) => builderScreen(id, x, k)).join("");
  // describe is its own full panel (as in the product); every other screen sits above the input bar
  const inner = `<div class="win-main">
        <div class="win-body">${screens}</div>
        <div class="win-in"><span class="in-a" id="${id}-ina"${opensWithDescribe ? " data-layout-allow-occlusion" : ""}>Ask a question or change anything…</span><span class="in-b" id="${id}-inb"${opensWithDescribe ? " data-layout-allow-occlusion" : ""}>The builder is working…</span><i class="go">${UP}</i></div>
      </div>`;
  const html = section(id, sc, win(id, "Membership AI · Campaign Builder", sc.title, sc.tag ?? "Sample", inner));
  let js = enter(id, sc.start);
  // title: hidden while the describe panel is up (the product shows only the kicker there)
  if (opensWithDescribe && sc.title && S[1])
    js += `\n  tl.fromTo("#${id}-title", { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: true }, ${r2(S[1].at + 0.2)});`;
  // the describe panel covers the input bar; the bar only shows once the panel has gone (no text under a fading panel)
  if (opensWithDescribe && S[1])
    js += `\n  tl.fromTo("#${id} .win-in", { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: true }, ${r2(S[1].at + 0.22)});`;
  // non-first screens start hidden; hand-offs (the old screen is gone before the new one arrives)
  S.forEach((x, k) => {
    if (k === 0) return;
    js += `\n  tl.to("#${id}-x${k - 1}", { opacity: 0, y: -14, duration: 0.2, ease: "power2.in" }, ${r2(x.at)});`;
    js += `\n  tl.fromTo("#${id}-x${k}", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(x.at + 0.22)});`;
  });
  S.forEach((x, k) => (js += builderJs(id, x, k, sc)));
  // input bar: "The builder is working…" while it thinks and plans
  if (sc.working) {
    // hand-off, not a crossfade: one placeholder is gone before the other appears
    js += `\n  tl.fromTo("#${id}-ina", { opacity: 1 }, { opacity: 0, duration: 0.12, immediateRender: false }, ${r2(sc.working[0])});`;
    js += `\n  tl.fromTo("#${id}-inb", { opacity: 0 }, { opacity: 1, duration: 0.2 }, ${r2(sc.working[0] + 0.14)});`;
    js += `\n  tl.to("#${id}-inb", { opacity: 0, duration: 0.12 }, ${r2(sc.working[1])});`;
    js += `\n  tl.to("#${id}-ina", { opacity: 1, duration: 0.2 }, ${r2(sc.working[1] + 0.14)});`;
  }
  js += exit(id, sc);
  return { html, js };
}

// ---------- checklist: the manual setup list (before), optionally ticked off (after) ----------
function checklist(sc, i) {
  const id = `s${i}`;
  const n = sc.items.length;
  const inner = `<div class="cl">
      <div class="cl-head"><b>${esc(sc.heading)}</b><span class="cl-count"><span id="${id}-c0">${esc(sc.count0 || `0 of ${n} done`)}</span>${
        sc.doneAt ? `<span class="cl-done" id="${id}-c1">${esc(sc.count1 || "Drafted for you")}</span>` : ""
      }</span></div>
      ${sc.items.map((t, k) => `<div class="cl-i" id="${id}-i${k}"><i class="box"><i class="box-c">${CHECK}</i></i><span>${esc(t)}</span></div>`).join("")}
    </div>`;
  const html = section(id, sc, win(id, sc.kicker || "New campaign", sc.title, sc.tag ?? "", inner));
  let js = enter(id, sc.start);
  if (sc.stagger)
    js += `\n  tl.fromTo("#${id} .cl-i", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.28, stagger: 0.07, ease: "power2.out" }, ${r2(sc.start + 0.25)});`;
  if (sc.doneAt) {
    js += `\n  tl.fromTo("#${id} .box-c", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.22, stagger: 0.12, ease: "back.out(2.2)", immediateRender: true }, ${r2(sc.doneAt)});`;
    js += `\n  tl.to("#${id} .box", { backgroundColor: "#5C7A32", borderColor: "#5C7A32", duration: 0.15, stagger: 0.12 }, ${r2(sc.doneAt)});`;
    js += `\n  tl.to("#${id} .cl-i span", { color: "#6E6E6E", duration: 0.15, stagger: 0.12 }, ${r2(sc.doneAt)});`;
    const t = sc.doneAt + n * 0.12;
    js += `\n  tl.to("#${id}-c0", { opacity: 0, duration: 0.15 }, ${r2(t)});`;
    js += `\n  tl.fromTo("#${id}-c1", { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, ${r2(t + 0.15)});`;
  }
  js += exit(id, sc);
  return { html, js };
}

// ---------- drafts: several describe -> draft runs stacked (renewal / onboarding / win-back) ----------
function drafts(sc, i) {
  const id = `s${i}`;
  const cards = sc.items
    .map(
      (d, k) => `<div class="dr" id="${id}-d${k}">
        <div class="dr-me"><b>You</b><span id="${id}-d${k}-t">${esc(k === 0 && sc.start === 0 ? d.prompt.slice(0, d.pre || 0) : "")}</span></div>
        <div class="dr-out" id="${id}-d${k}-o"><div><p class="dr-n">${esc(d.name)}</p><p class="dr-m">${esc(d.meta)}</p></div><span class="dr-ok"><i>${CHECK}</i>Draft ready</span></div>
        <p class="st dr-st" id="${id}-d${k}-s"><i class="st-dot"></i>Searching campaigns…</p>
      </div>`,
    )
    .join("");
  const html = section(id, sc, win(id, "Membership AI · Campaign Builder", sc.title, sc.tag ?? "Sample", `<div class="drs">${cards}</div>`));
  let js = enter(id, sc.start);
  sc.items.forEach((d, k) => {
    const t = d.at;
    if (!(k === 0 && sc.start === 0 && t === 0))
      js += `\n  tl.fromTo("#${id}-d${k}", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(t)});`;
    const t0 = t + 0.15, t1 = d.typeEnd ?? t0 + d.prompt.length * 0.02;
    js += typeJs(`${id}-d${k}-t`, d.prompt, k === 0 && sc.start === 0 ? d.pre || 0 : 0, t0, t1);
    js += `\n  tl.fromTo("#${id}-d${k}-s", { opacity: 0 }, { opacity: 1, duration: 0.2 }, ${r2(t1 + 0.1)});`;
    js += `\n  tl.to("#${id}-d${k}-s", { opacity: 0, duration: 0.15 }, ${r2(d.readyAt - 0.18)});`;
    js += `\n  tl.fromTo("#${id}-d${k}-o", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(d.readyAt)});`;
    js += `\n  tl.fromTo("#${id}-d${k} .dr-ok", { scale: 0.6 }, { scale: 1, duration: 0.35, ease: "back.out(2.4)", immediateRender: false }, ${r2(d.readyAt + 0.15)});`;
  });
  js += exit(id, sc);
  return { html, js };
}

// ---------- guard: the draft-first guardrails on a campaign card ----------
function guard(sc, i) {
  const id = `s${i}`;
  const inner = `<div class="gd">
      <div class="gd-top"><div><p class="pl-n">${esc(sc.name)}</p><p class="pl-m">${esc(sc.meta || "")}</p></div><span class="pill">${esc(sc.status || "Draft")}</span></div>
      ${sc.rows.map((r, k) => `<div class="gd-r" id="${id}-r${k}"><i class="ok-i">${CHECK}</i><span>${esc(r.text)}</span></div>`).join("")}
      ${sc.launch ? `<div class="gd-l" id="${id}-l"><span class="gd-btn">${esc(sc.launch.button)}</span><span class="gd-lt">${esc(sc.launch.text)}</span></div>` : ""}
    </div>`;
  const html = section(id, sc, win(id, sc.kicker || "Membership AI · Campaign Builder", sc.title, sc.tag ?? "Sample", inner));
  let js = enter(id, sc.start);
  sc.rows.forEach((r, k) => {
    js += `\n  tl.fromTo("#${id}-r${k}", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.32, ease: "power3.out" }, ${r2(r.at)});`;
    js += `\n  tl.fromTo("#${id}-r${k} .ok-i", { scale: 0.3 }, { scale: 1, duration: 0.3, ease: "back.out(2.4)", immediateRender: false }, ${r2(r.at + 0.12)});`;
  });
  if (sc.launch)
    js += `\n  tl.fromTo("#${id}-l", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(sc.launch.at)});`;
  js += exit(id, sc);
  return { html, js };
}

// ---------- signals: the Signals list (from the Membership AI page, sample data) ----------
function signals(sc, i) {
  const id = `s${i}`;
  const inner = `<ul class="sig">${sc.items
    .map(
      (s, k) => `<li class="${s.tone || ""}" id="${id}-g${k}"><div><strong>${esc(s.title)}<span>${esc(s.tag)}</span></strong><small>${esc(s.sub)}</small></div></li>`,
    )
    .join("")}</ul>`;
  const html = section(id, sc, win(id, "Membership AI · Signals", sc.title, sc.tag ?? "Sample data", inner));
  let js = enter(id, sc.start);
  sc.items.forEach((s, k) => {
    if (s.at === 0 && sc.start === 0) return;
    js += `\n  tl.fromTo("#${id}-g${k}", { opacity: 0, y: 22, scale: 0.98 }, { opacity: 1, y: 0, scale: 1, duration: 0.38, ease: "power3.out" }, ${r2(s.at)});`;
  });
  if (sc.focus) {
    const f = sc.focus;
    js += `\n  tl.to("#${id} .sig li:not(#${id}-g${f.index})", { opacity: 0.4, duration: 0.3 }, ${r2(f.at)});`;
    js += `\n  tl.to("#${id}-g${f.index}", { scale: 1.03, boxShadow: "0 18px 40px -18px rgba(47,47,47,0.35)", duration: 0.35, ease: "power3.out" }, ${r2(f.at)});`;
  }
  js += exit(id, sc);
  return { html, js };
}

// ---------- segment: AI Segment Builder (prompt -> build plan -> ready to review) ----------
function segment(sc, i) {
  const id = `s${i}`;
  const inner = `<div class="seg">
      <div class="you">You</div>
      <div class="sg-p"><span id="${id}-t">${esc(sc.start === 0 ? sc.prompt.slice(0, sc.pre || 0) : "")}</span><i class="caret" id="${id}-c"></i></div>
      <div class="sg-plan" id="${id}-plan"><b class="kk">Build plan</b>${sc.plan.map((p) => `<div class="sg-r">${esc(p)}</div>`).join("")}</div>
      <div class="sg-res" id="${id}-res"><span>Segment ready to review</span><div class="sg-c"><b id="${id}-n">0</b><small>contacts</small></div></div>
    </div>`;
  const html = section(id, sc, win(id, "Membership AI · AI Segment Builder", sc.title || "New segment", sc.tag ?? "Sample data", inner));
  let js = enter(id, sc.start);
  js += typeJs(`${id}-t`, sc.prompt, sc.start === 0 ? sc.pre || 0 : 0, sc.typeAt, sc.typeEnd);
  js += `\n  tl.to("#${id}-c", { opacity: 0, duration: 0.25, repeat: ${Math.floor((sc.typeEnd - sc.start) / 0.25)}, yoyo: true, ease: "steps(1)" }, ${r2(sc.start)});`;
  js += `\n  tl.set("#${id}-c", { opacity: 0 }, ${r2(sc.typeEnd + 0.05)});`;
  js += `\n  tl.fromTo("#${id}-plan", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(sc.planAt)});`;
  js += `\n  tl.fromTo("#${id}-plan .sg-r", { opacity: 0, x: -16 }, { opacity: 1, x: 0, duration: 0.25, stagger: 0.18 }, ${r2(sc.planAt + 0.2)});`;
  js += `\n  tl.fromTo("#${id}-res", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(sc.resAt)});`;
  js += `
  (function(){ const n = document.getElementById("${id}-n"); const o = { v: 0 };
    tl.fromTo(o, { v: 0 }, { v: ${sc.count}, duration: 1.0, ease: "power2.out", immediateRender: false, onUpdate: () => { n.textContent = Math.round(o.v).toLocaleString("en-US"); } }, ${r2(sc.resAt + 0.1)}); })();`;
  js += exit(id, sc);
  return { html, js };
}

// ---------- profile: Org Profile, pre-filled from the website, then goals ----------
function profile(sc, i) {
  const id = `s${i}`;
  const inner = `<div class="op">
      <div class="op-src" id="${id}-src"><i class="spk">${SPARK}</i>${esc(sc.source || "Pre-filled from your website. Review and edit.")}</div>
      ${sc.fields.map((f, k) => `<div class="op-f" id="${id}-f${k}"><small>${esc(f[0])}</small><span id="${id}-v${k}">${esc(f[1])}</span></div>`).join("")}
      <div class="op-g" id="${id}-goals"><b class="kk">Goals</b>${sc.goals.map((g) => `<div class="op-gi"><i class="tgt"></i>${esc(g)}</div>`).join("")}</div>
    </div>`;
  const html = section(id, sc, win(id, "Membership AI · Org Profile", sc.title, sc.tag ?? "Sample", inner));
  let js = enter(id, sc.start);
  sc.fields.forEach((f, k) => {
    const t = sc.fillAt + k * (sc.fillStep || 0.45);
    js += `\n  tl.fromTo("#${id}-v${k}", { opacity: 0, x: -14 }, { opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }, ${r2(t)});`;
    js += `\n  tl.fromTo("#${id}-f${k}", { backgroundColor: "#EAF0F6" }, { backgroundColor: "#F8F6F1", duration: 0.6, immediateRender: false }, ${r2(t)});`;
  });
  js += `\n  tl.fromTo("#${id}-goals", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(sc.goalsAt)});`;
  js += `\n  tl.fromTo("#${id}-goals .op-gi", { opacity: 0, x: -14 }, { opacity: 1, x: 0, duration: 0.28, stagger: 0.2 }, ${r2(sc.goalsAt + 0.2)});`;
  js += exit(id, sc);
  return { html, js };
}

// ---------- home: Home page (Today's Briefing, Upcoming Sends, Your Initiatives) ----------
function home(sc, i) {
  const id = `s${i}`;
  const b = sc.briefing;
  const days = Array.from({ length: 14 }, (_, k) => {
    const s = sc.sends.find((x) => x.day === k);
    return `<div class="hd${s ? (s.draft ? " dr8" : " on") : ""}"><i></i></div>`;
  }).join("");
  const inner = `<div class="hm">
      <div class="hm-b" id="${id}-b">
        <b class="kk">Today's Briefing</b>
        <p class="hm-h">${esc(b.headline)}</p>
        <p class="hm-t">${esc(b.text)}</p>
        <div class="hm-acts">${b.actions.map((a, k) => `<span class="hm-act${k === 0 ? " pri" : ""}" id="${id}-a${k}">${esc(a)}${k === 0 ? `<span class="tap" id="${id}-tap"></span>` : ""}</span>`).join("")}</div>
      </div>
      <div class="hm-s" id="${id}-s"><b class="kk">Upcoming Sends · next 14 days</b><div class="hds">${days}</div>${
        sc.draftNote ? `<p class="hm-w"><i class="wdot"></i>${esc(sc.draftNote)}</p>` : ""
      }</div>
      <div class="hm-i" id="${id}-i"><b class="kk">Your Initiatives</b>${sc.initiatives.map((n) => `<div class="hm-ii"><i class="pin"></i>${esc(n)}</div>`).join("")}</div>
    </div>`;
  const html = section(id, sc, win(id, "PropFuel · Home", sc.title, sc.tag ?? "Sample data", inner));
  let js = enter(id, sc.start);
  if (sc.start > 0) js += `\n  tl.fromTo("#${id}-b", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.35 }, ${r2(sc.start + 0.3)});`;
  js += `\n  tl.fromTo("#${id}-s", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(sc.sendsAt)});`;
  js += `\n  tl.fromTo("#${id} .hd", { opacity: 0, scaleY: 0.3 }, { opacity: 1, scaleY: 1, duration: 0.2, stagger: 0.04 }, ${r2(sc.sendsAt + 0.15)});`;
  js += `\n  tl.fromTo("#${id}-i", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(sc.initAt)});`;
  if (sc.pickAt) {
    js += tap(`#${id}-tap`, sc.pickAt);
    js += `\n  tl.to("#${id}-a0", { scale: 0.95, duration: 0.08, yoyo: true, repeat: 1 }, ${r2(sc.pickAt)});`;
  }
  js += exit(id, sc);
  return { html, js };
}

// ---------- initiative: one goal, its campaigns and headline metrics ----------
function initiative(sc, i) {
  const id = `s${i}`;
  const inner = `<div class="in">
      <div class="in-top"><p class="pl-n">${esc(sc.name)}</p><p class="pl-m">Goal: ${esc(sc.goal)}</p></div>
      <div class="in-ms">${sc.metrics.map((m, k) => `<div class="in-m" id="${id}-m${k}"><b id="${id}-v${k}">${esc(m.v)}</b><small>${esc(m.k)}</small></div>`).join("")}</div>
      <div class="in-cs" id="${id}-cs"><b class="kk">Campaigns</b>${sc.campaigns.map((c) => `<div class="in-c"><span>${esc(c[0])}</span><em>${esc(c[1])}</em></div>`).join("")}</div>
    </div>`;
  const html = section(id, sc, win(id, "Membership AI · Initiatives", sc.title, sc.tag ?? "Sample data", inner));
  let js = enter(id, sc.start);
  js += `\n  tl.fromTo("#${id} .in-m", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.3, stagger: 0.12, ease: "power3.out" }, ${r2(sc.metricsAt)});`;
  js += `\n  tl.fromTo("#${id}-cs", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(sc.campaignsAt)});`;
  js += `\n  tl.fromTo("#${id} .in-c", { opacity: 0, x: -16 }, { opacity: 1, x: 0, duration: 0.25, stagger: 0.15 }, ${r2(sc.campaignsAt + 0.2)});`;
  js += exit(id, sc);
  return { html, js };
}

// ---------- headline: big type for bumpers (one gradient phrase) ----------
function headline(sc, i) {
  const id = `s${i}`;
  const html = section(
    id,
    sc,
    `<div class="hl" id="${id}-win">${sc.lines.map((l, k) => `<div class="hl-l${k === sc.gradient ? " g" : ""}">${esc(l)}</div>`).join("")}</div>`,
  );
  let js = "";
  sc.lines.forEach((_, k) => {
    if (sc.start === 0 && k === 0) return;
    js += `\n  tl.fromTo("#${id} .hl-l:nth-child(${k + 1})", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, ${r2(sc.start + 0.15 + k * 0.35)});`;
  });
  js += exit(id, sc);
  return { html, js };
}

// ---------- site: a Website Engagement draft previewed on a skeleton page (reuses the popup look) ----------
// For product ads only (sample answers, tagged "Draft preview · Sample"). Case-study ads use `popup`.
function site(sc, i) {
  const id = `s${i}`;
  const q = sc.question;
  const answers = q.answers
    .map(
      (a, k) =>
        `<div class="ans" id="${id}-a${k}"><span class="ans-dot"></span><span class="ans-t">${esc(a)}</span><span class="ans-check">&#10003;</span>${k === q.pick ? `<span class="tap" id="${id}-tap"></span>` : ""}</div>`,
    )
    .join("");
  const html = section(
    id,
    sc,
    `<div class="browser" id="${id}-win">
      <div class="br-bar"><i></i><i></i><i></i><span class="br-url">${esc(sc.site)}</span><em class="win-tag site-tag">${esc(sc.tag || "Draft preview · Sample")}</em></div>
      <div class="br-page">
        <div class="sk sk-h"></div><div class="sk"></div><div class="sk sk-s"></div>
        <div class="sk-grid"><div></div><div></div><div></div></div>
        <div class="pop" id="${id}-q"><div class="pop-text">${esc(q.text)}</div><div class="answers">${answers}</div>${
          q.result ? `<p class="site-res" id="${id}-res">&rarr; ${esc(q.result)}</p>` : ""
        }</div>
      </div>
    </div>`,
  );
  let js = enter(id, sc.start);
  js += `\n  tl.fromTo("#${id}-q", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.4)" }, ${r2(q.at)});`;
  js += `\n  tl.fromTo("#${id}-q .ans", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.3, stagger: 0.09, ease: "power2.out" }, ${r2(q.at + 0.3)});`;
  if (q.pick !== undefined) {
    js += tap(`#${id}-tap`, q.pickAt);
    js += `\n  tl.to("#${id}-a${q.pick}", { backgroundColor: "#2F2F2F", color: "#F4F1EA", borderColor: "#2F2F2F", duration: 0.2 }, ${r2(q.pickAt + 0.05)});`;
    js += `\n  tl.fromTo("#${id}-a${q.pick} .ans-check", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, ${r2(q.pickAt + 0.12)});`;
    if (q.result) js += `\n  tl.fromTo("#${id}-res", { opacity: 0, x: -12 }, { opacity: 1, x: 0, duration: 0.3 }, ${r2(q.pickAt + 0.4)});`;
  }
  js += exit(id, sc);
  return { html, js };
}

export const SCENES = { builder, checklist, drafts, guard, signals, segment, profile, home, initiative, headline, site };

export const CSS = `
      /* ---- product UI (scenes-product.mjs): windows recreated from the real PropFuel screens ---- */
      #root { --pu: calc(var(--u) * 1.12); --win: #FDFCF9; --wbg: #F8F6F1; --stx: #3B6A8C; --go: #46628F; --okx: #4F6B2A; }
      .win { position: relative; width: 100%; height: 100%; max-height: calc(var(--u) * 980px); display: flex; flex-direction: column;
        background: var(--win); border: 1px solid #DCD6CA; border-radius: calc(var(--u) * 30px); overflow: hidden;
        box-shadow: 0 2px 0 rgba(47,47,47,0.03), 0 30px 70px -30px rgba(90,70,40,0.35); }
      .win-bar { position: relative; flex: none; padding: calc(var(--u) * 26px) calc(var(--u) * 34px) calc(var(--u) * 20px); border-bottom: 1px solid var(--line); background: var(--win); }
      .win-k { display: flex; align-items: center; gap: 10px; font-size: calc(var(--pu) * 21px); font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--stx); }
      .spk { display: inline-block; width: calc(var(--u) * 22px); height: calc(var(--u) * 22px); color: var(--stx); }
      .spk svg, .d-ico svg, .go svg, .ok-i svg, .box-c svg, .dr-ok i svg { width: 100%; height: 100%; display: block; }
      .win-t { margin-top: calc(var(--u) * 6px); font-size: calc(var(--pu) * 33px); font-weight: 700; letter-spacing: -0.01em; }
      .win-tag { position: absolute; top: calc(var(--u) * 24px); right: calc(var(--u) * 28px); font-style: normal; font-size: calc(var(--pu) * 18px); font-weight: 700;
        letter-spacing: 0.08em; text-transform: uppercase; color: #5A5A5A; background: var(--deep); border-radius: 999px; padding: 4px 12px; }
      .win-main { position: relative; flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; background: var(--wbg); }
      .win-body { position: relative; flex: 1 1 auto; min-height: 0; }
      .bs { position: absolute; inset: 0; overflow: hidden; }
      .bs:not(:first-child) { opacity: 0; }
      .feed { display: flex; flex-direction: column; gap: calc(var(--u) * 16px); padding: calc(var(--u) * 22px) calc(var(--u) * 30px); }
      .win-in { position: relative; flex: none; display: flex; align-items: center; margin: 0 calc(var(--u) * 26px) calc(var(--u) * 24px); min-height: calc(var(--u) * 78px);
        padding: 0 calc(var(--u) * 12px) 0 calc(var(--u) * 24px); border: 2px solid #D9D6DE; border-radius: calc(var(--u) * 20px); background: var(--win);
        font-size: calc(var(--pu) * 25px); color: #6E6E6E; }
      .in-a, .in-b { position: absolute; left: calc(var(--u) * 24px); }
      .in-b { opacity: 0; }
      .go { margin-left: auto; flex: none; width: calc(var(--u) * 54px); height: calc(var(--u) * 54px); border-radius: 50%; background: var(--go); color: #F4F1EA; padding: calc(var(--u) * 12px); }
      /* describe panel */
      .bs-describe { position: absolute; inset: 0; z-index: 2; display: flex; flex-direction: column; background: var(--win); padding: calc(var(--u) * 26px) calc(var(--u) * 34px) calc(var(--u) * 30px); }
      .win-body .bs-describe { bottom: calc(var(--u) * -102px); }
      .d-head { display: flex; align-items: center; gap: calc(var(--u) * 20px); }
      .d-ico { flex: none; width: calc(var(--u) * 72px); height: calc(var(--u) * 72px); border-radius: calc(var(--u) * 16px); background: var(--go); color: #F4F1EA; padding: calc(var(--u) * 16px); }
      .d-h { font-size: calc(var(--pu) * 42px); font-weight: 750; letter-spacing: -0.015em; }
      .d-s { font-size: calc(var(--pu) * 23px); color: #6E6E6E; margin-top: 2px; }
      .d-box { position: relative; flex: 1 1 auto; margin-top: calc(var(--u) * 26px); border: 2px solid #D9D6DE; border-radius: calc(var(--u) * 22px); background: var(--win);
        padding: calc(var(--u) * 26px) calc(var(--u) * 28px); }
      .d-p { font-size: calc(var(--pu) * 36px); font-weight: 600; line-height: 1.38; color: var(--ch); }
      .caret { display: inline-block; width: 3px; height: 1.05em; margin-left: 3px; vertical-align: -0.15em; background: var(--ch); }
      .d-go { position: absolute; right: calc(var(--u) * 20px); bottom: calc(var(--u) * 20px); width: calc(var(--u) * 64px); height: calc(var(--u) * 64px); padding: calc(var(--u) * 15px); }
      /* chat feed pieces */
      .me { align-self: flex-end; max-width: 86%; background: var(--go); color: #F4F1EA; border-radius: 20px 20px 6px 20px; padding: calc(var(--u) * 18px) calc(var(--u) * 22px);
        font-size: calc(var(--pu) * 27px); font-weight: 600; line-height: 1.4; }
      .st { display: flex; align-items: center; gap: 12px; font-size: calc(var(--pu) * 27px); font-weight: 600; color: #6E6E6E; }
      .st-dot { width: calc(var(--u) * 14px); height: calc(var(--u) * 14px); border-radius: 50%; background: var(--stx); flex: none; }
      .kk { display: block; font-size: calc(var(--pu) * 20px); font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--stx); }
      .cardk { background: var(--win); border: 1.5px solid #D9D6DE; border-radius: calc(var(--u) * 20px); padding: calc(var(--u) * 22px) calc(var(--u) * 24px); }
      .ck-p { margin-top: 6px; font-size: calc(var(--pu) * 26px); font-weight: 600; }
      .ck-q { display: flex; justify-content: space-between; align-items: center; gap: 14px; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--line);
        font-size: calc(var(--pu) * 24px); color: #5A5A5A; line-height: 1.35; }
      .ck-a { flex: none; font-style: normal; font-weight: 700; font-size: calc(var(--pu) * 21px); color: var(--stx); background: #E4ECF3; border-radius: 999px; padding: 6px 14px; }
      .pl-n { font-size: calc(var(--pu) * 34px); font-weight: 750; letter-spacing: -0.01em; line-height: 1.2; margin-top: 4px; }
      .pl-m { font-size: calc(var(--pu) * 22px); font-weight: 600; color: #6E6E6E; margin-top: 4px; }
      .fmt-9x16 .pl-head .kk, .fmt-9x16 .pl-head .pl-m { display: none; }
      .rows { display: flex; flex-direction: column; }
      .row { display: grid; grid-template-columns: calc(var(--u) * 104px) 1fr; gap: calc(var(--u) * 18px); padding: calc(var(--u) * 16px) 0; border-bottom: 1px solid var(--line); }
      .day { font-size: calc(var(--pu) * 22px); font-weight: 750; text-align: center; padding: 6px 0; border-radius: 999px; background: var(--deep); color: var(--ch); height: fit-content; }
      .row-q { font-size: calc(var(--pu) * 27px); font-weight: 700; line-height: 1.3; }
      .row-a { display: block; font-size: calc(var(--pu) * 22px); font-weight: 600; color: var(--stx); margin-top: 4px; }
      .brs { display: grid; grid-template-columns: 1fr 1fr; gap: calc(var(--u) * 10px); margin-top: calc(var(--u) * 12px); }
      .brc { display: block; border: 1.5px solid #C9D7E3; background: var(--win); border-radius: calc(var(--u) * 14px); padding: calc(var(--u) * 9px) calc(var(--u) * 14px); line-height: 1.2; }
      .brc b { display: block; font-size: calc(var(--pu) * 22px); font-weight: 700; }
      .brc small { display: block; font-size: calc(var(--pu) * 19px); font-weight: 650; color: #B5441C; margin-top: 2px; }
      .ap-q { font-size: calc(var(--pu) * 27px); font-weight: 600; line-height: 1.35; margin-top: 8px; }
      .opt { position: relative; display: flex; align-items: center; gap: calc(var(--u) * 16px); margin-top: calc(var(--u) * 14px); padding: calc(var(--u) * 14px) calc(var(--u) * 18px);
        border: 2px solid #D9D6DE; border-radius: calc(var(--u) * 16px); background: var(--win); }
      .opt b { display: block; font-size: calc(var(--pu) * 27px); font-weight: 700; }
      .opt small { display: block; font-size: calc(var(--pu) * 21px); color: #6E6E6E; }
      .radio { flex: none; position: relative; width: calc(var(--u) * 26px); height: calc(var(--u) * 26px); border-radius: 50%; border: 2px solid #8A8A8A; }
      .radio > i { position: absolute; inset: 4px; border-radius: 50%; background: #3B6A8C; transform: scale(0); }
      .ready { display: flex; align-items: center; gap: calc(var(--u) * 18px); padding: calc(var(--u) * 22px) calc(var(--u) * 24px); border-radius: calc(var(--u) * 20px);
        background: #EBF0E1; border: 1.5px solid #C5D3AE; }
      .ok-i { flex: none; width: calc(var(--u) * 46px); height: calc(var(--u) * 46px); border-radius: 50%; background: #5C7A32; color: #F4F1EA; padding: calc(var(--u) * 10px); }
      .ready b { display: block; font-size: calc(var(--pu) * 31px); font-weight: 750; }
      .ready small { display: block; font-size: calc(var(--pu) * 22px); font-weight: 700; color: var(--okx); margin-top: 2px; }
      .chips-l { font-size: calc(var(--pu) * 20px); font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #6E6E6E; }
      .chips { display: flex; flex-wrap: wrap; gap: calc(var(--u) * 10px); margin-top: calc(var(--u) * -8px); }
      .chip { font-size: calc(var(--pu) * 24px); font-weight: 700; padding: calc(var(--u) * 10px) calc(var(--u) * 18px); border-radius: 999px; background: var(--win); border: 1.5px solid #D9D6DE; }
      /* checklist */
      .cl { flex: 1 1 auto; background: var(--wbg); padding: calc(var(--u) * 20px) calc(var(--u) * 34px); display: flex; flex-direction: column; }
      .cl-head { display: flex; justify-content: space-between; align-items: baseline; padding-bottom: calc(var(--u) * 10px); }
      .cl-head b { font-size: calc(var(--pu) * 28px); font-weight: 750; }
      .cl-count { position: relative; font-size: calc(var(--pu) * 23px); font-weight: 700; color: #B5441C; }
      .cl-done { position: absolute; right: 0; top: 0; white-space: nowrap; color: var(--okx); opacity: 0; }
      .cl-i { display: flex; align-items: center; gap: calc(var(--u) * 18px); padding: calc(var(--u) * 13px) 0; border-top: 1px solid var(--line); font-size: calc(var(--pu) * 29px); font-weight: 600; }
      .box { flex: none; width: calc(var(--u) * 34px); height: calc(var(--u) * 34px); border-radius: calc(var(--u) * 9px); border: 2.5px solid #A9A39A; background: var(--win); color: #F4F1EA; padding: 3px; }
      .box-c { display: block; width: 100%; height: 100%; opacity: 0; }
      /* drafts stack */
      .drs { flex: 1 1 auto; display: flex; flex-direction: column; gap: calc(var(--u) * 16px); padding: calc(var(--u) * 20px) calc(var(--u) * 26px); background: var(--wbg); }
      .dr { position: relative; flex: 1 1 0; display: flex; flex-direction: column; justify-content: space-between; background: var(--win); border: 1.5px solid #D9D6DE; border-radius: calc(var(--u) * 20px); padding: calc(var(--u) * 18px) calc(var(--u) * 22px); }
      .dr-me { font-size: calc(var(--pu) * 25px); font-weight: 600; line-height: 1.35; }
      .dr-me b { display: inline-block; margin-right: 10px; font-size: calc(var(--pu) * 18px); font-weight: 750; letter-spacing: 0.08em; text-transform: uppercase; color: #F4F1EA; background: var(--go); border-radius: 999px; padding: 3px 10px; vertical-align: 0.15em; }
      .dr-out { display: flex; align-items: flex-end; justify-content: space-between; gap: 14px; }
      .dr-n { font-size: calc(var(--pu) * 30px); font-weight: 750; letter-spacing: -0.01em; }
      .dr-m { font-size: calc(var(--pu) * 21px); font-weight: 600; color: #6E6E6E; margin-top: 2px; }
      .dr-ok { flex: none; display: inline-flex; align-items: center; gap: 8px; font-size: calc(var(--pu) * 22px); font-weight: 750; color: var(--okx); background: #EBF0E1; border: 1.5px solid #C5D3AE; border-radius: 999px; padding: 6px 14px; }
      .dr-ok i { display: inline-block; width: calc(var(--u) * 22px); height: calc(var(--u) * 22px); }
      .dr-st { position: absolute; left: calc(var(--u) * 22px); bottom: calc(var(--u) * 20px); opacity: 0; }
      /* guard */
      .gd { flex: 1 1 auto; display: flex; flex-direction: column; gap: calc(var(--u) * 14px); padding: calc(var(--u) * 24px) calc(var(--u) * 34px); background: var(--wbg); }
      .gd-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; padding-bottom: calc(var(--u) * 10px); border-bottom: 1px solid var(--line); }
      .pill { flex: none; font-size: calc(var(--pu) * 22px); font-weight: 750; letter-spacing: 0.06em; text-transform: uppercase; color: #8A4B12; background: #F8E6C9; border-radius: 999px; padding: 6px 16px; }
      .gd-r { display: flex; align-items: center; gap: calc(var(--u) * 18px); background: var(--win); border: 1.5px solid var(--line); border-radius: calc(var(--u) * 18px); padding: calc(var(--u) * 16px) calc(var(--u) * 20px); font-size: calc(var(--pu) * 29px); font-weight: 650; }
      .gd-l { display: flex; align-items: center; gap: 18px; margin-top: auto; }
      .gd-btn { font-size: calc(var(--pu) * 27px); font-weight: 750; color: var(--ch); border: 2.5px solid var(--ch); border-radius: calc(var(--u) * 14px); padding: calc(var(--u) * 10px) calc(var(--u) * 26px); }
      .gd-lt { font-size: calc(var(--pu) * 25px); font-weight: 650; color: #5A5A5A; }
      /* signals */
      .sig { flex: 1 1 auto; list-style: none; display: flex; flex-direction: column; gap: calc(var(--u) * 14px); padding: calc(var(--u) * 22px) calc(var(--u) * 26px); background: var(--wbg); }
      .sig li { display: grid; grid-template-columns: 6px 1fr; gap: calc(var(--u) * 18px); background: var(--win); border: 1.5px solid var(--line); border-radius: calc(var(--u) * 18px); padding: calc(var(--u) * 18px) calc(var(--u) * 22px) calc(var(--u) * 18px) 0; overflow: hidden; }
      .sig li::before { content: ""; background: var(--stx); border-radius: 0 4px 4px 0; }
      .sig li.r::before { background: #C0392B; } .sig li.g::before { background: #5C7A32; }
      .sig strong { display: flex; justify-content: space-between; gap: 12px; font-size: calc(var(--pu) * 28px); font-weight: 750; line-height: 1.25; }
      .sig strong span { flex: none; height: fit-content; font-size: calc(var(--pu) * 18px); font-weight: 750; letter-spacing: 0.08em; text-transform: uppercase; padding: 4px 12px; border-radius: 999px; background: #E4ECF3; color: var(--stx); }
      .sig li.r strong span { background: #F6E1DE; color: #A5301F; } .sig li.g strong span { background: #E6EDDA; color: var(--okx); }
      .sig small { display: block; font-size: calc(var(--pu) * 23px); color: #5A5A5A; margin-top: 6px; line-height: 1.4; }
      /* segment */
      .seg { flex: 1 1 auto; display: flex; flex-direction: column; gap: calc(var(--u) * 16px); padding: calc(var(--u) * 24px) calc(var(--u) * 34px); background: var(--wbg); }
      .you { font-size: calc(var(--pu) * 19px); font-weight: 750; letter-spacing: 0.1em; color: #6E6E6E; }
      .sg-p { min-height: calc(var(--u) * 128px); background: var(--win); border: 2px solid #D9D6DE; border-radius: calc(var(--u) * 18px); padding: calc(var(--u) * 18px) calc(var(--u) * 22px);
        font-size: calc(var(--pu) * 31px); font-weight: 650; line-height: 1.35; }
      .sg-plan { background: var(--win); border: 1.5px solid var(--line); border-radius: calc(var(--u) * 18px); padding: calc(var(--u) * 16px) calc(var(--u) * 22px); }
      .sg-r { font-size: calc(var(--pu) * 26px); font-weight: 600; padding: calc(var(--u) * 10px) 0 0 calc(var(--u) * 26px); position: relative; }
      .sg-r::before { content: ""; position: absolute; left: 0; top: calc(var(--u) * 22px); width: calc(var(--u) * 12px); height: calc(var(--u) * 12px); border-radius: 50%; background: var(--stx); }
      .sg-res { display: flex; justify-content: space-between; align-items: center; background: #EBF0E1; border: 1.5px solid #C5D3AE; border-radius: calc(var(--u) * 18px); padding: calc(var(--u) * 16px) calc(var(--u) * 22px); }
      .sg-res > span { font-size: calc(var(--pu) * 26px); font-weight: 750; color: var(--okx); }
      .sg-c b { font-size: calc(var(--pu) * 52px); font-weight: 800; letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
      .sg-c small { font-size: calc(var(--pu) * 22px); font-weight: 650; color: #5A5A5A; margin-left: 8px; }
      /* org profile */
      .op { flex: 1 1 auto; display: flex; flex-direction: column; gap: calc(var(--u) * 10px); padding: calc(var(--u) * 20px) calc(var(--u) * 34px); background: var(--wbg); }
      .op-src { display: flex; align-items: center; gap: 10px; font-size: calc(var(--pu) * 23px); font-weight: 700; color: var(--stx); padding-bottom: 4px; }
      .op-f { display: grid; grid-template-columns: calc(var(--u) * 230px) 1fr; align-items: center; gap: 14px; border-bottom: 1px solid var(--line); padding: calc(var(--u) * 12px) calc(var(--u) * 8px); border-radius: 10px; }
      .op-f small { font-size: calc(var(--pu) * 21px); font-weight: 700; color: #6E6E6E; }
      .op-f span { font-size: calc(var(--pu) * 26px); font-weight: 650; line-height: 1.3; }
      .op-g { margin-top: calc(var(--u) * 8px); background: var(--win); border: 1.5px solid var(--line); border-radius: calc(var(--u) * 18px); padding: calc(var(--u) * 16px) calc(var(--u) * 22px); }
      .op-gi { display: flex; align-items: center; gap: 14px; font-size: calc(var(--pu) * 26px); font-weight: 650; margin-top: calc(var(--u) * 10px); }
      .tgt { flex: none; width: calc(var(--u) * 20px); height: calc(var(--u) * 20px); border-radius: 50%; border: 4px solid #B5441C; }
      /* home */
      .hm { flex: 1 1 auto; display: flex; flex-direction: column; gap: calc(var(--u) * 14px); padding: calc(var(--u) * 20px) calc(var(--u) * 26px); background: var(--wbg); }
      .hm > div { background: var(--win); border: 1.5px solid var(--line); border-radius: calc(var(--u) * 18px); padding: calc(var(--u) * 16px) calc(var(--u) * 22px); }
      .hm-h { font-size: calc(var(--pu) * 30px); font-weight: 750; margin-top: 6px; line-height: 1.25; }
      .hm-t { font-size: calc(var(--pu) * 23px); font-weight: 550; color: #5A5A5A; margin-top: 6px; line-height: 1.4; }
      .hm-acts { display: flex; flex-wrap: wrap; gap: 12px; margin-top: calc(var(--u) * 14px); }
      .hm-act { position: relative; font-size: calc(var(--pu) * 23px); font-weight: 700; border: 2px solid #D9D6DE; border-radius: calc(var(--u) * 12px); padding: calc(var(--u) * 8px) calc(var(--u) * 16px); }
      .hm-act.pri { background: var(--go); border-color: var(--go); color: #F4F1EA; }
      .hds { display: grid; grid-template-columns: repeat(14, 1fr); gap: calc(var(--u) * 8px); margin-top: calc(var(--u) * 12px); }
      .hd { height: calc(var(--u) * 50px); border-radius: 8px; background: var(--deep); display: flex; align-items: flex-end; justify-content: center; padding-bottom: 6px; }
      .hd i { width: calc(var(--u) * 12px); height: calc(var(--u) * 12px); border-radius: 50%; background: transparent; }
      .hd.on i { background: var(--stx); } .hd.dr8 i { background: #C26A12; }
      .hm-w { display: flex; align-items: center; gap: 10px; font-size: calc(var(--pu) * 21px); font-weight: 650; color: #8A4B12; margin-top: 10px; }
      .wdot { width: calc(var(--u) * 12px); height: calc(var(--u) * 12px); border-radius: 50%; background: #C26A12; }
      .hm-ii { display: flex; align-items: center; gap: 12px; font-size: calc(var(--pu) * 25px); font-weight: 650; margin-top: calc(var(--u) * 10px); }
      .pin { width: calc(var(--u) * 12px); height: calc(var(--u) * 12px); border-radius: 3px; background: var(--ch); transform: rotate(45deg); }
      .fmt-9x16 .hm { gap: calc(var(--u) * 10px); padding: calc(var(--u) * 14px) calc(var(--u) * 22px); }
      .fmt-9x16 .hm > div { padding: calc(var(--u) * 12px) calc(var(--u) * 20px); }
      .fmt-9x16 .hd { height: calc(var(--u) * 36px); }
      /* initiative */
      .in { flex: 1 1 auto; display: flex; flex-direction: column; gap: calc(var(--u) * 16px); padding: calc(var(--u) * 22px) calc(var(--u) * 34px); background: var(--wbg); }
      .in-ms { display: grid; grid-template-columns: 1fr 1fr; gap: calc(var(--u) * 12px); }
      .in-m { background: var(--win); border: 1.5px solid var(--line); border-radius: calc(var(--u) * 16px); padding: calc(var(--u) * 14px) calc(var(--u) * 20px); }
      .in-m b { display: block; font-size: calc(var(--pu) * 44px); font-weight: 800; letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
      .in-m small { font-size: calc(var(--pu) * 21px); font-weight: 650; color: #5A5A5A; }
      .in-cs { background: var(--win); border: 1.5px solid var(--line); border-radius: calc(var(--u) * 16px); padding: calc(var(--u) * 14px) calc(var(--u) * 20px); }
      .in-c { display: flex; justify-content: space-between; gap: 12px; font-size: calc(var(--pu) * 25px); font-weight: 650; padding: calc(var(--u) * 10px) 0 0; }
      .in-c em { font-style: normal; font-size: calc(var(--pu) * 20px); font-weight: 750; color: var(--okx); background: #E6EDDA; border-radius: 999px; padding: 3px 12px; height: fit-content; }
      .site-tag { position: static; flex: none; margin-left: 12px; }
      .fmt-9x16 .cl-i { padding: calc(var(--u) * 9px) 0; }
      .site-res { margin-top: calc(var(--u) * 14px); font-size: calc(var(--pu) * 26px); font-weight: 750; color: var(--stx); }
      .cta-sub { margin-top: calc(var(--u) * 12px); }
      /* headline (bumpers) */
      .hl { width: 100%; }
      .hl-l { font-size: calc(var(--u) * 104px); font-weight: 800; line-height: 1.02; letter-spacing: -0.04em; }
      .hl-l.g { background: linear-gradient(to right, #F47C2C, #FBC02D); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; padding-bottom: 0.08em; }
`;
