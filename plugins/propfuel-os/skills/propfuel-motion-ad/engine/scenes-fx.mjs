// propfuel-motion-ad: effect beats built on vendored open-source libraries (engine/vendor/LICENSES.md).
// Loaded by build.mjs (SCENES + CSS + VENDOR). Same contract as the other beats: each renderer returns
// { html, js }, js runs with `tl` in scope, times are absolute seconds on the root timeline.
//
// HyperFrames determinism, per effect:
//  - Every effect is driven by a proxy tween on the one paused GSAP timeline (`ease: "none"`, onUpdate redraws),
//    so a seek to any time redraws that exact frame. No requestAnimationFrame, no clocks, no network.
//  - Setup that needs fonts or layout (measuring text, Pixi's async init) pushes a promise onto `__fx`; the
//    template registers window.__timelines["main"] only after every promise settles.
//  - Randomness is seeded: Matter.js runs a fixed 60 Hz step from fixed spawn points, Rough.js gets `seed`,
//    p5.brush gets brush.seed()/noiseSeed(), Pixi's GlitchFilter is reshuffled from a seeded PRNG per frame.
//
// Effects animate IN: none of them is a frame-0 thumbnail. Open the ad on a caption + a static beat, not on these.

const esc = (s) =>
  String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const r2 = (n) => Math.round(n * 1000) / 1000;
const J = (v) => JSON.stringify(v);

const section = (id, sc, inner, cls = "") =>
  `<section id="${id}" class="clip scene ${cls}" data-start="${sc.start}" data-duration="${r2(sc.end - sc.start)}" data-track-index="1">${inner}</section>`;
const exit = (sel, sc) =>
  sc.hold ? "" : `\n  tl.to("${sel}", { opacity: 0, y: -30, duration: 0.3, ease: "power2.in" }, ${r2(sc.end - 0.32)});`;
// one proxy tween across the whole beat: the frame is a pure function of local time
const drive = (s, e, fn) =>
  `tl.fromTo({ t: 0 }, { t: 0 }, { t: ${r2(e - s)}, duration: ${r2(e - s)}, ease: "none", immediateRender: false, onUpdate: function () { ${fn}(this.targets()[0].t); } }, ${r2(s)});`;

// ---------- stack: word cards fall, collide and stack (Matter.js) ----------
// sc.words[] (2-8 short words), sc.hero = index of the one gradient card, sc.title (optional line above),
// sc.dropAt (s after start, default 0.15), sc.gap (s between drops, default 0.16), sc.preDrop (n cards already
// resting at the beat's first frame: use it when the stack opens the ad, so frame 0 isn't an empty floor).
// The physics is simulated once on load at a fixed 60 Hz step and baked per frame; seeking reads the bake.
function stack(sc, i) {
  const id = `s${i}`;
  const words = sc.words || [];
  const cards = words
    .map((w, k) => `<div class="stk-card${k === sc.hero ? " stk-hero" : ""}" id="${id}-k${k}" data-layout-allow-overflow>${esc(w)}</div>`)
    .join("");
  const html = section(
    id,
    sc,
    `<div class="fx-stack" id="${id}-wrap">${sc.title ? `<div class="stk-title" id="${id}-title">${esc(sc.title)}</div>` : ""}<div class="stk-pit" id="${id}-pit">${cards}</div></div>`,
  );
  const s = sc.start;
  const dur = sc.end - sc.start;
  const js = `
  __fx.push(__fxFonts.then(() => {
    const pit = document.getElementById("${id}-pit");
    const W = pit.clientWidth, H = pit.clientHeight, FPS = 60, N = Math.ceil(${r2(dur)} * FPS) + 1;
    const PRE = ${sc.preDrop || 0}, WARM = PRE ? 2 * FPS : 0;
    const els = ${J(words)}.map((_, k) => document.getElementById("${id}-k" + k));
    const M = Matter, eng = M.Engine.create({ enableSleeping: false });
    eng.gravity.y = 1.6;
    const wall = { isStatic: true, friction: 0.9 };
    M.Composite.add(eng.world, [
      M.Bodies.rectangle(W / 2, H + 50, W * 3, 100, wall),
      M.Bodies.rectangle(-50, H / 2, 100, H * 6, wall),
      M.Bodies.rectangle(W + 50, H / 2, 100, H * 6, wall),
    ]);
    // fixed spawn plan: alternate sides of centre, seeded tilt; nothing depends on wall-clock or Math.random
    const h = (a) => { const v = Math.sin(a * 12.9898 + ${sc.seed || 7} * 78.233) * 43758.5453; return v - Math.floor(v); };
    const plan = els.map((el, k) => {
      const w = el.offsetWidth, hh = el.offsetHeight;
      const span = Math.max(0, W - w) / 2;
      const x = W / 2 + (k % 2 ? 1 : -1) * span * (0.15 + 0.6 * h(k + 1));
      // the first preDrop cards fall during an unrecorded 2 s warm-up, so they are already resting at frame 0
      const pre = k < PRE, at = pre ? Math.round(k * 0.18 * FPS) : WARM + Math.round((${sc.dropAt ?? 0.15} + (k - PRE) * ${sc.gap ?? 0.16}) * FPS);
      return { el, w, hh, x, y: -hh * 0.6, a: (h(k + 11) - 0.5) * 0.5, at, body: null };
    });
    const bake = plan.map(() => new Float32Array(N * 3));
    for (let g = 0; g < WARM + N; g++) {
      const f = g - WARM;
      for (const p of plan) if (g === p.at) {
        p.body = M.Bodies.rectangle(p.x, p.y, p.w, p.hh, { chamfer: { radius: Math.min(p.hh / 2, 22) }, angle: p.a, restitution: 0.18, friction: 0.7, frictionStatic: 1, density: 0.002 });
        // heavier rotational inertia: cards tip and settle instead of cartwheeling (no upside-down words)
        M.Body.setInertia(p.body, p.body.inertia * ${sc.inertia ?? 6});
        M.Composite.add(eng.world, p.body);
      }
      if (f >= 0) plan.forEach((p, k) => {
        const b = p.body, o = f * 3;
        bake[k][o] = b ? b.position.x : p.x; bake[k][o + 1] = b ? b.position.y : -p.hh * 2; bake[k][o + 2] = b ? b.angle : p.a;
      });
      M.Engine.update(eng, 1000 / FPS);
    }
    const draw = (t) => {
      const f = Math.max(0, Math.min(N - 1, Math.round(t * FPS)));
      plan.forEach((p, k) => {
        const o = f * 3;
        p.el.style.transform = "translate(" + (bake[k][o] - p.w / 2).toFixed(2) + "px," + (bake[k][o + 1] - p.hh / 2).toFixed(2) + "px) rotate(" + bake[k][o + 2].toFixed(4) + "rad)";
      });
    };
    draw(0);
    ${drive(s, sc.end, "draw")}
  }));${sc.title ? `\n  tl.fromTo("#${id}-title", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, ${r2(s + 0.05)});` : ""}${exit(`#${id}-wrap`, sc)}`;
  return { html, js };
}

// ---------- sketch: a hand-drawn mark around a number or word (Rough.js) ----------
// sc.value (the hero, e.g. "370+"), sc.label, sc.sub, sc.source, sc.mark: circle | underline | box | hatch,
// sc.seed (any integer; same seed = same strokes), sc.drawAt (s after start, default 0.45).
// The mark is the frame's one gradient element; the number stays charcoal.
function sketch(sc, i) {
  const id = `s${i}`;
  const html = section(
    id,
    sc,
    `<div class="fx-sketch" id="${id}-wrap">
      <svg class="sk-svg" id="${id}-svg" aria-hidden="true"></svg>
      <div class="sk-num" id="${id}-num">${esc(sc.value)}</div>
      ${sc.label ? `<div class="sk-label" id="${id}-label">${esc(sc.label)}</div>` : ""}
      ${sc.sub ? `<div class="stat-sub" id="${id}-sub">${esc(sc.sub)}</div>` : ""}
      ${sc.source ? `<div class="stat-src" id="${id}-src">${esc(sc.source)}</div>` : ""}
    </div>`,
    "fx",
  );
  const s = sc.start;
  const at = s + (sc.drawAt ?? 0.45);
  const js = `
  tl.fromTo("#${id}-num", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }, ${r2(s + 0.05)});${sc.label ? `
  tl.fromTo("#${id}-label", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.35 }, ${r2(s + 0.25)});` : ""}${sc.sub ? `
  tl.fromTo("#${id}-sub", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.35 }, ${r2(at + 0.6)});` : ""}${sc.source ? `
  tl.fromTo("#${id}-src", { opacity: 0 }, { opacity: 1, duration: 0.35 }, ${r2(at + 0.85)});` : ""}
  __fx.push(__fxFonts.then(() => {
    const svg = document.getElementById("${id}-svg"), wrap = document.getElementById("${id}-wrap"), num = document.getElementById("${id}-num");
    const W = wrap.clientWidth, H = wrap.clientHeight;
    svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.setAttribute("width", W); svg.setAttribute("height", H);
    // offsetLeft/Top: layout box, untouched by the entrance scale
    const bx = num.offsetLeft, by = num.offsetTop, bw = num.offsetWidth, bh = num.offsetHeight;
    const u = parseFloat(getComputedStyle(wrap).getPropertyValue("--u")) || 1;
    const NS = "http://www.w3.org/2000/svg";
    svg.innerHTML = '<defs><linearGradient id="${id}-g" gradientUnits="userSpaceOnUse" x1="' + bx + '" y1="0" x2="' + (bx + bw) + '" y2="0"><stop offset="0" stop-color="#F47C2C"/><stop offset="1" stop-color="#FBC02D"/></linearGradient></defs>';
    const gen = rough.generator();
    const o = { seed: ${sc.seed || 3}, roughness: 1.4, bowing: 1.2, strokeWidth: 7 * u, stroke: "#000", preserveVertices: true };
    const mark = ${J(sc.mark || "circle")};
    let d;
    if (mark === "underline") d = gen.curve([[bx - 10 * u, by + bh * 0.98], [bx + bw * 0.5, by + bh * 1.04], [bx + bw + 14 * u, by + bh * 0.96]], o);
    else if (mark === "box") d = gen.rectangle(bx - 26 * u, by - 10 * u, bw + 52 * u, bh + 20 * u, o);
    else if (mark === "hatch") d = gen.rectangle(bx - 22 * u, by + bh * 0.42, bw + 44 * u, bh * 0.5, Object.assign({}, o, { stroke: "none", fill: "#000", fillStyle: "hachure", hachureGap: 13 * u, hachureAngle: -38, fillWeight: 5 * u }));
    else d = gen.ellipse(bx + bw / 2, by + bh / 2, bw * 1.24 + 40 * u, bh * 1.32, o);
    const paths = gen.toPaths(d).map((p) => {
      const el = document.createElementNS(NS, "path");
      el.setAttribute("d", p.d); el.setAttribute("fill", "none"); el.setAttribute("stroke", "url(#${id}-g)");
      el.setAttribute("stroke-width", p.strokeWidth || 7 * u); el.setAttribute("stroke-linecap", "round"); el.setAttribute("stroke-linejoin", "round");
      svg.appendChild(el);
      const L = el.getTotalLength(); el.style.strokeDasharray = L + " " + L; el.style.strokeDashoffset = L;
      return { el, L };
    });
    // draw-on: the strokes follow each other like one hand going round twice
    const each = ${r2(sc.drawDur ?? 0.7)} / paths.length;
    paths.forEach((p, k) => tl.fromTo(p.el, { strokeDashoffset: p.L }, { strokeDashoffset: 0, duration: each, ease: "power1.inOut", immediateRender: false }, ${r2(at)} + k * each));
  }));${exit(`#${id}-wrap`, sc)}`;
  return { html, js };
}

// ---------- brush: a textured gradient brush swipe behind a word (p5.brush, standalone build, WebGL2) ----------
// sc.text (the headline), sc.mark (the word or phrase inside sc.text the swipe sits behind; default all),
// sc.brush (p5.brush preset: charcoal | crayon | marker | pastel | spray, default charcoal), sc.weight, sc.seed, sc.swipeAt.
// The stroke is painted ONCE on load into an OffscreenCanvas (seeded), copied into a 2D canvas and tinted with
// the brand gradient; the reveal is a GSAP clip-path wipe, so a seek never re-paints and the texture can't swim.
function brush(sc, i) {
  const id = `s${i}`;
  const mark = sc.mark || sc.text;
  const at = sc.text.indexOf(mark);
  const pre = at > -1 ? sc.text.slice(0, at) : "";
  const post = at > -1 ? sc.text.slice(at + mark.length) : "";
  const html = section(
    id,
    sc,
    `<div class="fx-brush" id="${id}-wrap"><div class="bh-t" id="${id}-t">${esc(pre)}<span class="bh-m" id="${id}-m"><canvas class="bh-c" id="${id}-c"></canvas><span class="bh-w">${esc(at > -1 ? mark : sc.text)}</span></span>${esc(post)}</div>${
      sc.sub ? `<div class="bh-sub" id="${id}-sub">${esc(sc.sub)}</div>` : ""
    }</div>`,
    "fx",
  );
  const s = sc.start;
  const sw = s + (sc.swipeAt ?? 0.35);
  const js = `
  tl.fromTo("#${id}-t", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, ${r2(s + 0.05)});
  tl.fromTo("#${id}-c", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: ${r2(sc.swipeDur ?? 0.55)}, ease: "power2.inOut", immediateRender: true }, ${r2(sw)});${
    sc.sub ? `\n  tl.fromTo("#${id}-sub", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.35 }, ${r2(sw + 0.5)});` : ""
  }
  __fx.push(__fxFonts.then(() => {
    const m = document.getElementById("${id}-m"), c = document.getElementById("${id}-c");
    const w = Math.round(m.offsetWidth * 1.2), h = Math.round(m.offsetHeight * 1.05);
    c.width = w; c.height = h;
    // one shared OffscreenCanvas for every brush beat on the page (p5.brush keeps one active target);
    // never call brush.scaleBrushes here: it multiplies on every call. Size comes from the weight instead.
    if (!window.__fxBrushTarget || window.__fxBrushTarget.width < w || window.__fxBrushTarget.height < h) { window.__fxBrushTarget = new OffscreenCanvas(w, h); brush.load(window.__fxBrushTarget); }
    const off = window.__fxBrushTarget, ow = off.width, oh = off.height;
    brush.seed(${sc.seed || 11}); brush.noiseSeed(${sc.seed || 11});
    brush.clear();
    brush.set(${J(sc.brush || "charcoal")}, "#2F2F2F", ${sc.weight ? r2(sc.weight) : "h / 8.5"});
    // origin is the target's centre; the swipe sits in its top-left w x h. Three overlapping passes, a hair
    // off level, like a real highlighter.
    const x0 = -ow / 2, y0 = -oh / 2, L = x0 + w * 0.05, R = x0 + w * 0.95, cy = y0 + h * 0.52;
    [-0.24, 0, 0.24].forEach((dy, k) => brush.line(L + k * 5, cy + dy * h + (k - 1) * 2, R - k * 7, cy + dy * h - 3 + k * 2));
    brush.render();
    const g = c.getContext("2d");
    g.drawImage(off, 0, 0, w, h, 0, 0, w, h);
    g.globalCompositeOperation = "source-in";
    const gr = g.createLinearGradient(0, 0, w, 0); gr.addColorStop(0, "#F47C2C"); gr.addColorStop(1, "#FBC02D");
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
  }));${exit(`#${id}-wrap`, sc)}`;
  return { html, js };
}

// ---------- filter: glow or glitch on one line of type (PixiJS v8 + pixi-filters, WebGL) ----------
// sc.text, sc.effect: glow | glitch, sc.sub, sc.peakAt (s after start, default 0.45), sc.seed.
// glow: a gold (#FBC02D) halo blooms and settles; it is the frame's accent, so no other gradient on screen.
// glitch: a short seeded slice-displacement burst that resolves to clean type by ~1s.
// If WebGL is unavailable the DOM fallback line shows instead (same words, a CSS gold text-shadow for glow).
function filter(sc, i) {
  const id = `s${i}`;
  const html = section(
    id,
    sc,
    `<div class="fx-filter" id="${id}-wrap"><canvas class="fl-c" id="${id}-c"></canvas><div class="fl-dom" id="${id}-dom">${esc(sc.text)}</div>${
      sc.sub ? `<div class="fl-sub" id="${id}-sub">${esc(sc.sub)}</div>` : ""
    }</div>`,
    "fx",
  );
  const s = sc.start;
  const eff = sc.effect || "glow";
  const peak = sc.peakAt ?? 0.45;
  const js = `
  tl.fromTo("#${id}-c, #${id}-dom", { opacity: 0 }, { opacity: 1, duration: 0.3 }, ${r2(s + 0.05)});${
    sc.sub ? `\n  tl.fromTo("#${id}-sub", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.35 }, ${r2(s + peak + 0.5)});` : ""
  }
  __fx.push(__fxFonts.then(async () => {
    const wrap = document.getElementById("${id}-wrap"), c = document.getElementById("${id}-c"), dom = document.getElementById("${id}-dom");
    const W = wrap.clientWidth, H = dom.offsetHeight + 120;
    try {
      const app = new PIXI.Application();
      await app.init({ canvas: c, width: W, height: H, backgroundAlpha: 0, antialias: true, autoStart: false, preference: "webgl", resolution: 1, autoDensity: false });
      app.ticker.stop();
      const cs = getComputedStyle(dom);
      const txt = new PIXI.Text({ text: ${J(sc.text)}, style: { fontFamily: "DM Sans", fontWeight: cs.fontWeight, fontSize: parseFloat(cs.fontSize), lineHeight: parseFloat(cs.lineHeight), letterSpacing: parseFloat(cs.letterSpacing) || 0, fill: "#2F2F2F", align: "center", wordWrap: true, wordWrapWidth: dom.clientWidth, padding: 40 } });
      txt.anchor.set(0.5); txt.x = W / 2; txt.y = H / 2; app.stage.addChild(txt);
      let draw;
      if (${J(eff)} === "glitch") {
        // GlitchFilter shuffles with Math.random: give it a seeded PRNG for each call, keyed to the frame
        const prng = (a) => () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
        const seeded = (seed, fn) => { const R = Math.random; Math.random = prng(seed); try { fn(); } finally { Math.random = R; } };
        let gf; seeded(${sc.seed || 5}, () => { gf = new PIXI.filters.GlitchFilter({ slices: 9, offset: 0, direction: 0, fillMode: 0, average: false, seed: 0 }); });
        txt.filters = [gf];
        draw = (t) => {
          const k = Math.round(t * 30), burst = t < ${r2(peak + 0.55)} ? Math.max(0, 1 - Math.abs(t - ${r2(peak)}) / 0.55) : 0;
          // outside the burst the filter is off, so the line settles to clean type (no residual slice shear)
          gf.enabled = burst > 0.15;
          if (gf.enabled) seeded(${sc.seed || 5} * 1000 + Math.floor(k / 2), () => { gf.offset = Math.round(70 * burst); gf.seed = (k % 7) / 7; gf.refresh(); });
          app.render();
        };
      } else {
        const gl = new PIXI.filters.GlowFilter({ distance: 28, outerStrength: 0, innerStrength: 0, color: 0xFBC02D, quality: 0.4 });
        txt.filters = [gl];
        draw = (t) => {
          const up = Math.min(1, t / ${r2(peak)}), settle = t > ${r2(peak)} ? Math.max(0, 1 - (t - ${r2(peak)}) / 0.6) : 0;
          gl.outerStrength = t <= ${r2(peak)} ? 4.2 * up * up : 1.6 + 2.6 * settle * settle;
          app.render();
        };
      }
      dom.style.visibility = "hidden";
      draw(0);
      ${drive(s, sc.end, "draw")}
    } catch (e) {
      console.error("filter beat: WebGL unavailable, DOM fallback", e);
      c.style.display = "none"; dom.classList.add("fl-fallback-${eff}");
    }
  }));${exit(`#${id}-wrap`, sc)}`;
  return { html, js };
}

// ---------- orb: an animated dotted orb for an AI-thinking / listening moment (thinking-orbs engine, MIT) ----------
// sc.state: listening | searching | working | solving | composing | shaping, sc.label, sc.sub,
// sc.density / sc.dot (multipliers over the upstream 64 px tuning; defaults 2.2 / 2.6 read well at video size).
// Dots are inked charcoal on cream (the engine's greyscale mapped to the brand ramp). Pure function of time.
function orb(sc, i) {
  const id = `s${i}`;
  const html = section(
    id,
    sc,
    `<div class="fx-orb" id="${id}-wrap"><canvas class="orb-c" id="${id}-c"></canvas>${sc.label ? `<div class="orb-l" id="${id}-l">${esc(sc.label)}</div>` : ""}${
      sc.sub ? `<div class="orb-s" id="${id}-sub">${esc(sc.sub)}</div>` : ""
    }</div>`,
    "fx",
  );
  const s = sc.start;
  const js = `
  (function(){
    const c = document.getElementById("${id}-c"), S = Math.round(c.clientWidth); c.width = S; c.height = S;
    const g = c.getContext("2d");
    const draw = (t) => { g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, S, S); ThinkingOrbs.draw(g, ${J(sc.state || "listening")}, S, t + 0.6, ${sc.density ?? 2.2}, ${sc.dot ?? 2.6}); };
    draw(0);
    ${drive(s, sc.end, "draw")}
  })();
  tl.fromTo("#${id}-c", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, ${r2(s + 0.05)});${
    sc.label ? `\n  tl.fromTo("#${id}-l", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, ${r2(s + 0.3)});` : ""
  }${sc.sub ? `\n  tl.fromTo("#${id}-sub", { opacity: 0 }, { opacity: 1, duration: 0.35 }, ${r2(s + 0.6)});` : ""}${exit(`#${id}-wrap`, sc)}`;
  return { html, js };
}

// ---------- words: kinetic headline on Anime.js v4 (optional; GSAP already covers this) ----------
// sc.text, sc.hero (a word index to fill with the gradient), sc.stagger (ms, default 70).
// Shows the seekable Anime.js pattern: autoplay false, registered on window.__hfAnime, which the HyperFrames
// animejs adapter seeks with the frame time in ms. Use it only when you need Anime.js-specific tools.
function words(sc, i) {
  const id = `s${i}`;
  const ws = sc.text.split(" ");
  const html = section(
    id,
    sc,
    `<div class="fx-words" id="${id}-wrap"><div class="wd-t">${ws
      .map((w, k) => `<span class="wd${k === sc.hero ? " wd-hero" : ""}">${esc(w)}</span>`)
      .join(" ")}</div></div>`,
    "fx",
  );
  const s = sc.start;
  const js = `
  (function(){
    const a = anime.createTimeline({ autoplay: false });
    a.add("#${id} .wd", { y: [60, 0], opacity: [0, 1], rotate: [6, 0], duration: 650, delay: anime.stagger(${sc.stagger ?? 70}), ease: "outExpo" }, ${Math.round((s + 0.05) * 1000)});
    __fxAnime(a);
  })();${exit(`#${id}-wrap`, sc)}`;
  return { html, js };
}

export const SCENES = { stack, sketch, brush, filter, orb, words };

// vendor files each beat needs (engine/vendor -> project assets/), in load order
export const VENDOR = {
  stack: ["matter.min.js"],
  sketch: ["rough.min.js"],
  brush: ["p5.brush.standalone.min.js"],
  filter: ["pixi.min.js", "pixi-filters.min.js"],
  orb: ["thinking-orbs.min.js"],
  words: ["anime.umd.min.js"],
};

export const CSS = `
      /* ---------- fx beats (scenes-fx.mjs) ---------- */
      .scene.fx { flex-direction: column; }
      .fx-stack { position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; }
      .stk-title { flex: 0 0 auto; font-size: calc(var(--u) * 52px); font-weight: 750; letter-spacing: -0.02em; line-height: 1.1; margin-bottom: calc(var(--u) * 20px); }
      .stk-pit { position: relative; flex: 1 1 auto; overflow: hidden; }
      .stk-card { position: absolute; left: 0; top: 0; display: block; white-space: nowrap; padding: calc(var(--u) * 22px) calc(var(--u) * 36px);
        border-radius: calc(var(--u) * 22px); background: var(--card); border: 2px solid var(--ch); color: var(--ch);
        font-size: calc(var(--u) * 46px); font-weight: 750; letter-spacing: -0.015em; line-height: 1; transform: translate(0px, -400px);
        box-shadow: 0 16px 30px -18px rgba(90,70,40,0.45); }
      .stk-card.stk-hero { background: linear-gradient(to right, #F47C2C, #FBC02D); border-color: transparent; }

      .fx-sketch { position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
      .sk-svg { position: absolute; left: 0; top: 0; pointer-events: none; overflow: visible; }
      .sk-num { position: relative; display: block; font-size: calc(var(--u) * 230px); font-weight: 800; line-height: 1; letter-spacing: -0.045em; padding: 0 calc(var(--u) * 10px); }
      .sk-label { position: relative; font-size: calc(var(--u) * 46px); font-weight: 700; margin-top: calc(var(--u) * 64px); }
      .fx-sketch .stat-sub, .fx-sketch .stat-src { position: relative; }

      .fx-brush { width: 100%; display: flex; flex-direction: column; align-items: flex-start; }
      .bh-t { font-size: calc(var(--u) * 92px); font-weight: 800; line-height: 1.08; letter-spacing: -0.035em; max-width: 11ch; }
      .layout-row .bh-t { max-width: 16ch; }
      .bh-m { position: relative; display: inline-block; white-space: nowrap; }
      .bh-w { position: relative; z-index: 1; }
      .bh-c { position: absolute; left: -10%; top: 2%; width: 120%; height: 105%; display: block; }
      .bh-sub { font-size: calc(var(--u) * 36px); font-weight: 600; color: var(--mg); margin-top: calc(var(--u) * 40px); }

      .fx-filter { position: relative; width: 100%; display: flex; flex-direction: column; align-items: center; text-align: center; }
      .fl-c { display: block; }
      .fl-dom { position: absolute; left: 0; right: 0; top: 60px; margin: 0 auto; max-width: 92%; font-size: calc(var(--u) * 96px); font-weight: 800; line-height: 1.06; letter-spacing: -0.03em; }
      .fl-dom.fl-fallback-glow, .fl-dom.fl-fallback-glitch { position: relative; top: 0; }
      .fl-dom.fl-fallback-glow { text-shadow: 0 0 calc(var(--u) * 26px) rgba(251,192,45,0.85); }
      .fl-sub { font-size: calc(var(--u) * 36px); font-weight: 600; color: var(--mg); margin-top: calc(var(--u) * 10px); }

      .fx-orb { width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
      .orb-c { display: block; width: min(calc(var(--u) * 560px), 62%); aspect-ratio: 1; }
      .layout-row .orb-c { width: min(560px, 70%); }
      .orb-l { font-size: calc(var(--u) * 62px); font-weight: 750; letter-spacing: -0.02em; margin-top: calc(var(--u) * 26px); }
      .orb-s { font-size: calc(var(--u) * 32px); font-weight: 600; color: var(--mg); margin-top: calc(var(--u) * 14px); }

      .fx-words { width: 100%; }
      .wd-t { font-size: calc(var(--u) * 96px); font-weight: 800; line-height: 1.06; letter-spacing: -0.035em; max-width: 11ch; }
      .layout-row .wd-t { max-width: 16ch; }
      .wd { display: inline-block; }
      .wd-hero { background: linear-gradient(to right, #F47C2C, #FBC02D); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
`;
