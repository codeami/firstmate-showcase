#!/usr/bin/env python3
"""Build one map page for this site: python3 -I maps/_shared/build.py <map.json> <out.html>
Follows super-board's build_skillmap.py (see NOTICE). Renders map.json through the vendored sdlc layout, swaps the
super-board site nav for a link bar for this site, reads the site's day/night choice, and adds status badges and a key.
meta.marks maps a node id to space-separated tokens: planned, unproven, added, owner, evidence. meta.key lists the key chips to show.
Stdlib only."""
import html, json, re, sys
from pathlib import Path

SH = Path(__file__).resolve().parent
src, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(SH))
import layout_sdlc

E = html.escape
data = json.loads(src.read_text(encoding="utf-8"))
meta = data["meta"]
m = layout_sdlc.build(data, src.parent)
rd = lambda f: (SH / f).read_text(encoding="utf-8")

NW, BADGE = layout_sdlc.NW, {"planned": ("PLANNED", 52), "unproven": ("NOT PROVEN", 66), "added": ("OWNER'S OWN", 70)}
CLS = {"planned": "pln", "owner": "own", "evidence": "evd"}


def mark_nodes(svg):
    for sid, toks in meta.get("marks", {}).items():
        toks = toks.split()
        pat = re.compile(r'<g class="nd (st-\w+)"( data-id="%s" .*?)</g>' % re.escape(E(sid)), re.S)
        mt = pat.search(svg)
        if not mt:
            sys.exit("map.json marks an id that is not a node: " + sid)
        body = mt.group(2)
        x, y = re.search(r'<rect x="(-?\d+)" y="(-?\d+)"', body).groups()
        badges = ""
        for t in toks:
            if t in BADGE:
                label, w = BADGE[t]
                badges += (f'<rect class="bdg bdg-{t}" x="{int(x)+8}" y="{int(y)-7}" width="{w}" height="13" rx="6.5"/>'
                           f'<text class="bdt" x="{int(x)+8+w/2}" y="{int(y)+3}" text-anchor="middle">{label}</text>')
        cls = " ".join([mt.group(1)] + [CLS[t] for t in toks if t in CLS])
        svg = svg[:mt.start()] + f'<g class="nd {cls}"{body}{badges}</g>' + svg[mt.end():]
    return svg


KEYS = {
    "owner": ("own", "Owner decides", "Nothing moves on until the owner says so."),
    "evidence": ("evd", "Evidence, derived", "Read from git, the forge or the files. Not taken from the worker's word."),
    "planned": ("pln", "Planned", "Written down. Not built."),
    "unproven": ("unp", "Not proven", "Designed or installed. No run has proved it."),
    "added": ("add", "Owner's own", "An addition in the owner's private fork. Not upstream."),
}
key = "".join(f'<span class="ky {KEYS[k][0]}" title="{E(KEYS[k][2])}"><i></i>{KEYS[k][1]}</span>' for k in meta.get("key", []))
legend = f'<div class="sm-key" aria-label="Key">{key}</div>' if key else ""

here = out.name
LINKS = [("../index.html", "Story"), ("../overview.html", "Six lanes"), ("skills.html", "Skill map"), ("flow.html", "Harness flow")]
CUR = ' aria-current="page"'
links = "".join(f'<a class="lk" href="{h}"{CUR if h == here else ""}><span class="tl">{t}</span></a>' for h, t in LINKS)
NAV = ('<header class="top wide"><div class="in">'
       '<a class="logo" href="../index.html"><svg viewBox="0 0 96 96" aria-hidden="true"><rect x="4" y="4" width="88" height="88" rx="20" fill="#191816" stroke="#36332f" stroke-width="2"/>'
       '<rect x="16" y="18" width="16" height="60" rx="4" fill="#fff" fill-opacity=".1"/><rect x="40" y="18" width="16" height="60" rx="4" fill="#fff" fill-opacity=".1"/><rect x="64" y="18" width="16" height="60" rx="4" fill="#fff" fill-opacity=".1"/>'
       '<rect x="19" y="22" width="10" height="9" rx="2" fill="#e07b6a"/><rect x="43" y="22" width="10" height="9" rx="2" fill="#8cc594"/><rect x="67" y="22" width="10" height="9" rx="2" fill="#b4a6e6"/></svg><span class="lt">Six-Lane Agent Setup</span></a>'
       '<span class="sp"></span>' + links +
       '<button class="btn" id="sbtt" type="button" aria-label="Toggle light or dark theme"><svg class="ni" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg><span class="nl">Theme</span></button>'
       '</div></header>')

EXTRA_CSS = r'''
.top .tl{white-space:nowrap}.top .lk[aria-current="page"]{background:var(--bg2);font-weight:600}
@media (max-width:640px){.top .in{flex-wrap:wrap;gap:4px 8px}.top .sp{display:none}}
.nd.own rect{stroke:var(--accent);stroke-width:3}.nd.evd rect{fill:color-mix(in srgb,var(--ok) 12%,var(--bg))}
.nd.pln rect{stroke-dasharray:5 4}.nd.pln .nn,.nd.pln .nt{opacity:.75}
.bdg{stroke:none!important}.bdg-planned{fill:var(--muted)!important}.bdg-unproven{fill:var(--st-plan)!important}.bdg-added{fill:var(--accent)!important}
.bdt{fill:var(--bg);font:800 7.5px var(--sans);letter-spacing:.05em}
.sm-key{display:flex;flex-wrap:wrap;gap:8px 16px;padding:10px 4px 2px;font-size:13px;color:var(--muted)}
.ky{display:inline-flex;align-items:center;gap:6px}.ky i{width:16px;height:12px;border-radius:3px;border:1.4px solid var(--muted);display:inline-block}
.ky.own i{border:3px solid var(--accent)}.ky.evd i{background:color-mix(in srgb,var(--ok) 25%,var(--bg))}.ky.pln i{border-style:dashed}
.ky.unp i{background:var(--st-plan);border-color:var(--st-plan)}.ky.add i{background:var(--accent);border-color:var(--accent)}
'''

# The "Also on the map" band head opens "stage:anytime", which stageModel() cannot name. Give it a dialog of its own.
ANY_JS = ("\n;(function(){var m0=SMPAGE.model;SMPAGE.model=function(id){if(id==='stage:anytime'){return {accent:'st-anytime calm',title:PACK.L.anytime,"
          "tags:[[PACK.L.anytime.toUpperCase(),1]],blocks:[{type:'note',v:PACK.L.anyNote},{label:'Groups here',key:'how',type:'chips',"
          "v:Object.keys(PACK.any).map(function(g){return 'any:'+g})}]}}return m0(id)}})();\n")

shell_js = rd("shell.js")
if "'sb-theme'" not in shell_js:
    sys.exit("shell.js no longer holds the sb-theme key; update build.py")
shell_js = shell_js.replace("'sb-theme'", "'theme'")  # share the site's day/night choice

foot = m["footer"]
foot = (foot + " · " if foot else "") + 'Map shell: <a href="https://github.com/EricTechPro/super-board" target="_blank" rel="noopener">super-board</a> by EricTechPro (MIT) · <a href="_shared/NOTICE">notice</a> · <a href="../index.html">Back to the site</a>'

t = rd("shell.html").replace("Best-practice order", E(meta.get("orderTitle", "Stages in order")))
for k, v in {"%%TITLE%%": E(m["title"]), "%%PLOGO%%": "", "%%FAV%%": "", "%%VERSION%%": E(m["version"]), "%%SUBTITLE%%": m["subtitle"], "%%NAV%%": NAV,
             "%%FILTER%%": "", "%%TOOLS%%": "", "%%SVG%%": mark_nodes(m["svg"]), "%%LEGEND%%": legend, "%%ORDER%%": "".join(
                 f'<div class="step {c}"><i>{E(n)}</i><span><b>{E(tt)}</b><small>{E(s)}</small></span></div>' for n, tt, s, c in m["order"]),
             "%%FOOTER%%": foot, "%%SHELLCSS%%": rd("shell.css") + "\n:root{--mapw:%dpx}" % m["mapw"], "%%SMCSS%%": rd("skillmap.css"),
             "%%PAGECSS%%": m["css"] + EXTRA_CSS, "%%SMJS%%": rd("skillmap.js"), "%%PAGEJS%%": m["js"] + ANY_JS, "%%SHELLJS%%": shell_js, "%%CANVASJS%%": rd("canvas.js")}.items():
    t = t.replace(k, v)
out.write_text(t, encoding="utf-8")
print(out, len(t))
