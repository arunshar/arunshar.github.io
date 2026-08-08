#!/usr/bin/env python3
"""Author GeoTrace-grade curated architecture SVGs for every project.

Matches the GeoTrace-Agent figure house style (tools/curated_figs/geotrace-agent.svg):
viewBox ~1120 wide, shared <style>/<defs>, a left-to-right labeled spine, optional
feeder boxes, a deterministic-kernel lane, and an honest amber band; honest coloring
green=real/tested, amber(dashed)=off-the-shelf/target. Self-contained (literal colors)
so each renders as an external <img> on the make4ht paper pages.

Writes tools/curated_figs/<slug>.svg for the 9 cv-portfolio projects + covid-mobility.
MBOR's hub SVG is written by the mbor block at the bottom into ~/code/mbor/docs/.
Grounded in each project's real pipeline / study guide / paper; no invented components.
"""
from pathlib import Path
import os

OUT = Path(__file__).resolve().parent / "curated_figs"
OUT.mkdir(parents=True, exist_ok=True)

# GeoTrace house style, self-contained (literal hex, no var() so it works as <img>)
STYLE = """<defs>
<marker id="ah" markerWidth="12" markerHeight="12" refX="9" refY="5" orient="auto"><path d="M0,0 L11,5 L0,10 z" fill="#202733"/></marker>
</defs>
<style>
svg text{font-family:'Noto Sans',system-ui,-apple-system,sans-serif;}
.box{fill:#fff;stroke:#aebbd0;stroke-width:1.5;}
.acc{fill:#eaf3fd;stroke:#1772d0;stroke-width:1.5;}
.grn{fill:#e6f7ed;stroke:#0f766e;stroke-width:1.5;}
.amb{fill:#fff6e6;stroke:#e7b66a;stroke-width:1.5;stroke-dasharray:6 4;}
.lane{fill:#f3f6fc;stroke:#aebbd0;stroke-width:1.5;}
.ttl{font-size:16px;font-weight:700;fill:#0e1117;font-family:'Montserrat','Noto Sans',sans-serif;}
.sub{font-size:12.5px;font-weight:500;fill:#1b2230;}
.ar{stroke:#202733;stroke-width:2.2;fill:none;marker-end:url(#ah);}
.lg{font-size:12px;}
</style>"""

W = 1120
MARGIN = 28


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def box(x, y, w, h, title, subs=None, cls="box"):
    subs = subs or []
    cx = x + w / 2
    out = [f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="11"/>']
    # vertically center title + subs
    n = 1 + len(subs)
    ty = y + h / 2 - (n - 1) * 9 + 5
    out.append(f'<text class="ttl" x="{cx:.0f}" y="{ty:.0f}" text-anchor="middle">{esc(title)}</text>')
    for i, s in enumerate(subs):
        out.append(f'<text class="sub" x="{cx:.0f}" y="{ty + 18 * (i + 1):.0f}" text-anchor="middle">{esc(s)}</text>')
    return "".join(out)


def harrow(x1, y, x2, label=None):
    s = f'<line class="ar" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>'
    if label:
        s += f'<text class="sub" x="{(x1 + x2) / 2:.0f}" y="{y - 9}" text-anchor="middle">{esc(label)}</text>'
    return s


def varrow(x, y1, y2):
    return f'<line class="ar" x1="{x}" y1="{y1}" x2="{x}" y2="{y2}"/>'


def spine(items, y=52, h=92, gap=44):
    """items: list of (title, [subs], cls). Auto-spaced across W. Returns (svg, centers)."""
    n = len(items)
    bw = (W - 2 * MARGIN - (n - 1) * gap) / n
    parts, centers = [], []
    x = MARGIN
    for i, (t, subs, cls) in enumerate(items):
        parts.append(box(x, y, bw, h, t, subs, cls))
        centers.append((x, x + bw, x + bw / 2))
        x += bw + gap
    for i in range(n - 1):
        parts.append(harrow(centers[i][1], y + h / 2, centers[i + 1][0]))
    return "".join(parts), centers, bw, y, h


def band(y, title, lines, h=84):
    cx = MARGIN + 20
    parts = [f'<rect x="{MARGIN}" y="{y}" width="{W - 2 * MARGIN}" height="{h}" rx="12" fill="#fff6e6" stroke="#e7b66a" stroke-width="1.5"/>']
    parts.append(f'<text x="{cx}" y="{y + 28}" style="font-size:15px;font-weight:700;fill:#0e1117;font-family:Montserrat,sans-serif">{esc(title)}</text>')
    for i, ln in enumerate(lines):
        parts.append(f'<text x="{cx}" y="{y + 50 + i * 20}" class="sub">{esc(ln)}</text>')
    return "".join(parts)


def legend(y):
    return (f'<text class="lg" x="{MARGIN}" y="{y}" fill="#0f766e">green = real and tested</text>'
            f'<text class="lg" x="{MARGIN + 200}" y="{y}" fill="#b45309">dashed amber = off-the-shelf / target</text>'
            f'<text class="lg" x="{MARGIN + 470}" y="{y}" fill="#1772d0">blue = learned / core method</text>')


def wrap(vh, body, label):
    return (f'<svg viewBox="0 0 {W} {vh}" width="100%" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{esc(label)}">{STYLE}{body}</svg>\n')


figs = {}

# ---- geosam-3d ----
b, c, bw, y, h = spine([
    ("Monocular video", ["single camera"], "box"),
    ("Depth Anything V2", ["metric depth priors", "(off-the-shelf)"], "amb"),
    ("3D Gaussian field", ["MonoGS reconstruction", "(off-the-shelf)"], "amb"),
    ("SAM 2 video masks", ["lift to per-Gaussian feats", "(off-the-shelf)"], "amb"),
    ("Promptable 3D mask", ["click-to-segment"], "box"),
], y=52)
body = b
body += varrow(c[2][2], y + h, 224)
body += box(MARGIN, 236, (W - 2 * MARGIN - 44) / 2, 84, "Gaussian feature head", ["InfoNCE, 32-d, trained"], "grn")
body += box(MARGIN + (W - 2 * MARGIN - 44) / 2 + 44, 236, (W - 2 * MARGIN - 44) / 2, 84, "Heat-method geodesic kernel", ["Varadhan distance, fixes occlusion leak"], "grn")
body += band(344, "Honest scope", [
    "Feature head + heat-geodesic kernel are real and verified (21 unit tests, synthetic-occlusion checks).",
    "MonoGS / Depth-Anything / SAM 2 are off-the-shelf front-ends; ScanNet / Replica benchmarks are the next step (target).",
])
body += legend(452)
figs["geosam-3d"] = wrap(470, body, "GeoSAM-3D architecture")

# ---- mapfix-spatial ----
b, c, bw, y, h = spine([
    ("Distorted coordinates", ["raw geo points"], "box"),
    ("Distortion detector", ["residual / outlier scan"], "box"),
    ("Deterministic correction engine", ["closed-form fit, exact"], "grn"),
    ("Clean map projection", ["rendered output"], "box"),
], y=52)
body = b
body += box(c[2][0], 196, bw, 76, "Optional model-backed analysis", ["LLM-assisted path"], "amb")
body += varrow(c[2][2], y + h, 196)
body += band(300, "Honest scope", [
    "The deterministic correction engine is real and tested; the model-backed analysis path is optional.",
    "Shipped as a live browser demo.",
])
body += legend(408)
figs["mapfix-spatial"] = wrap(426, body, "MapFix Spatial architecture")

# ---- sat-splat-distort ----
b, c, bw, y, h = spine([
    ("Non-pinhole cameras", ["RPC / pushbroom / fisheye / 360"], "box"),
    ("Distortion-aware projection", ["closed-form analytic Jacobians"], "grn"),
    ("3D Gaussian splatting", ["rasterizer"], "box"),
    ("Learned distortion prior", ["token grid (target)"], "amb"),
    ("Novel-view synthesis", ["rendered views"], "box"),
], y=52)
body = b
body += band(196, "Honest scope", [
    "Analytic Jacobians for all 4 camera models validated against torch.autograd to ~1e-5 relative error (20 tests).",
    "Learned distortion-prior token grid and the IEEE GRSS DFC2019 multi-view PSNR benchmark are the next step (target).",
])
body += legend(304)
figs["sat-splat-distort"] = wrap(322, body, "Sat-Splat-Distort architecture")

# ---- physflow-earth ----
b, c, bw, y, h = spine([
    ("Coarse input", ["Sentinel-2 / ERA5 / CHIRPS"], "box"),
    ("DiT backbone", ["denoiser"], "box"),
    ("Rectified flow + physics", ["mass / divergence / band-ratio operators"], "grn"),
    ("Super-resolved field", ["fine-scale output"], "box"),
    ("PSNR / SSIM eval", ["held-out split"], "amb"),
], y=52)
body = b
body += band(196, "Honest scope", [
    "Physics operators (mass, divergence, band-ratio) are exact and unit-tested (8 tests).",
    "Trained PSNR / SSIM on a held-out split is the next step (target); leaderboard numbers not claimed.",
])
body += legend(304)
figs["physflow-earth"] = wrap(322, body, "PhysFlow-Earth architecture")

# ---- trajprompt ----
b, c, bw, y, h = spine([
    ("AIS tracks + imagery", ["+ free-text query"], "box"),
    ("TrajCLIP encoder", ["trajectory-text contrastive"], "acc"),
    ("Open-vocabulary retrieval", ["top-k tracks"], "box"),
    ("TGARD + SAM 2", ["rendezvous + segmentation"], "grn"),
    ("Results", ["ranked matches"], "box"),
], y=52)
body = b
body += band(196, "Honest scope", [
    "TrajCLIP retrieval and TGARD rendezvous are exercised on a synthetic / open set (6 tests).",
    "A full open-vocabulary maritime benchmark is the next step (target).",
])
body += legend(304)
figs["trajprompt"] = wrap(322, body, "TrajPrompt architecture")

# ---- pin-service ----
b, c, bw, y, h = spine([
    ("Client request", ["gRPC (proto)"], "box"),
    ("PIN service", ["request handler"], "grn"),
    ("Placement pipeline", ["geocode + resolve"], "grn"),
    ("Response", ["resolved PIN"], "box"),
], y=52)
body = b
body += box(c[1][0], 196, c[2][1] - c[1][0], 76, "Load test (Locust) + observability", ["measured p50 / p95 latency"], "grn")
body += varrow((c[1][2] + c[2][2]) / 2, y + h, 196)
body += band(300, "Honest scope", [
    "The service and placement pipeline are real; p50 / p95 latency is measured under a real Locust load test.",
])
body += legend(390)
figs["pin-service"] = wrap(408, body, "PIN-Service architecture")

# ---- pi-grpo ----
feedw = (W - 2 * MARGIN - 3 * 30) / 4
fy = 48
body = ""
feeders = [
    ("Hard S-KBM penalty", ["unbounded violation", "(physics floor)"], "grn"),
    ("Soft envelope", ["95th-pct jerk / curvature"], "box"),
    ("Pi-DPM term", ["reconstruction likelihood"], "box"),
    ("Preference model", ["cross-encoder (optional)"], "amb"),
]
fx = MARGIN
fcenters = []
for t, subs, cls in feeders:
    body += box(fx, fy, feedw, 80, t, subs, cls)
    fcenters.append(fx + feedw / 2)
    fx += feedw + 30
# hybrid reward bus
busy = 168
body += f'<line x1="{fcenters[0]}" y1="128" x2="{fcenters[0]}" y2="{busy}" stroke="#202733" stroke-width="2.2"/>'
body += f'<line x1="{fcenters[-1]}" y1="128" x2="{fcenters[-1]}" y2="{busy}" stroke="#202733" stroke-width="2.2"/>'
body += f'<line x1="{fcenters[0]}" y1="{busy}" x2="{fcenters[-1]}" y2="{busy}" stroke="#202733" stroke-width="2.2"/>'
body += box(W / 2 - 150, 188, 300, 56, "Hybrid reward", [], "acc")
body += varrow(W / 2, busy, 188)
b2, c2, bw2, y2, h2 = spine([
    ("Preference triples", ["~11K from GeoTrace HITL"], "box"),
    ("PPO / DPO / GRPO", ["post-training"], "acc"),
    ("vLLM rollouts", ["content-addressed ckpts"], "box"),
    ("Physics-feasible policy", ["trajectory generation"], "grn"),
], y=276, h=84)
body += b2
body += band(384, "Quantitative result under revision", [
    "The workshop paper's two GRPO arms were not trained at a matched step budget, so the violation-rate",
    "comparison is being re-run. No figure is quoted here until it completes.",
])
body += legend(492)
figs["pi-grpo"] = wrap(510, body, "Pi-GRPO architecture")

# ---- covid-mobility ----
b, c, bw, y, h = spine([
    ("Aggregated mobility", ["mobile-device data"], "box"),
    ("Spatial-epidemiology", ["aggregation + privacy"], "box"),
    ("County-level analytics", ["policy vs mobility"], "grn"),
    ("Delivered to policymakers", ["MN Dept of Mgmt & Budget"], "box"),
], y=52)
body = b
body += band(196, "Impact", [
    "Measured how COVID-19 policies shifted mobility over aggregated mobile-device data; delivered county-level analytics.",
    "The work was cited in testimony to the Minnesota House Transportation Finance Committee.",
])
body += legend(304)
figs["covid-mobility"] = wrap(322, body, "COVID-mobility architecture")

# ---- darkvessel-stack ----
dfeedw = (W - 2 * MARGIN - 2 * 30) / 3
dbody = ""
dfeeders = [
    ("Sentinel-1 SAR", ["Lee speckle filter, ~96% var cut"], "grn"),
    ("Sentinel-2 optical", ["cloud mask"], "box"),
    ("AIS tracks", ["vessel reports"], "box"),
]
dfx = MARGIN
dfc = []
for t, subs, cls in dfeeders:
    dbody += box(dfx, 48, dfeedw, 80, t, subs, cls)
    dfc.append(dfx + dfeedw / 2)
    dfx += dfeedw + 30
dbusy = 168
dbody += f'<line x1="{dfc[0]}" y1="128" x2="{dfc[0]}" y2="{dbusy}" stroke="#202733" stroke-width="2.2"/>'
dbody += f'<line x1="{dfc[-1]}" y1="128" x2="{dfc[-1]}" y2="{dbusy}" stroke="#202733" stroke-width="2.2"/>'
dbody += f'<line x1="{dfc[0]}" y1="{dbusy}" x2="{dfc[-1]}" y2="{dbusy}" stroke="#202733" stroke-width="2.2"/>'
dbody += box(W / 2 - 200, 188, 400, 56, "Geo foundation backbone", ["Prithvi-2 / Clay / SatMAE++ (swappable)"], "amb")
dbody += varrow(W / 2, dbusy, 188)
db2, dc2, dbw2, dy2, dh2 = spine([
    ("DETR detection", ["bounding boxes"], "box"),
    ("SAM 2 segmentation", ["instance masks"], "box"),
    ("TGARD + Pi-DPM anomaly", ["rendezvous + spoof reasoning"], "grn"),
    ("Dark-vessel detections", ["ranked alerts"], "box"),
], y=276, h=84)
dbody += db2
dbody += varrow(W / 2, 244, 276)
dbody += band(384, "Honest scope", [
    "Lee speckle filter (~96% variance reduction), TGARD rendezvous, and the foundation-model adapter are verified (53 tests).",
    "Backbones are swappable off-the-shelf geospatial FMs; the xView3-SAR detection-AP benchmark is the next step (target).",
])
dbody += legend(492)
figs["darkvessel-stack"] = wrap(510, dbody, "DarkVesselNet architecture")

for slug, svg in figs.items():
    (OUT / f"{slug}.svg").write_text(svg)
    print(f"OK {slug}: {len(svg)} bytes")

# ---- mbor (written into the mbor repo hub dir) ----
b, c, bw, y, h = spine([
    ("Road network", ["DIMACS Bay Area, 321,270 nodes"], "box"),
    ("KaHIP min-cut partition", ["50 fragments"], "box"),
    ("Boundary multigraph", ["inter-fragment links"], "acc"),
    ("MEPFV precompute", ["FPPV + BPPV (rayon)"], "acc"),
    ("Online retrieval", ["per query"], "box"),
], y=52)
mbody = b
mw = (W - 2 * MARGIN - 44) / 3
mbody += box(MARGIN, 196, mw, 80, "Basic (Alg 3)", ["frontier merge"], "box")
mbody += box(MARGIN + mw + 22, 196, mw, 80, "Adv 2DCI (Alg 4)", ["cost-interval pruning"], "grn")
mbody += box(MARGIN + 2 * (mw + 22), 196, mw, 80, "Complete Pareto set", ["time vs energy routes"], "grn")
mbody += varrow(c[4][2], y + h, 196)
mbody += band(300, "Reproduced (Rust + Triton)", [
    "Full BAY (321,270 nodes): MBOR-Adv ~900x over exact bi-objective A*, exact Pareto sets (0 mismatches vs 3 baselines).",
    "Dense GPU sub-steps reach 96x and 1188x in Triton on an A100; avg 118.8 solutions/query (paper: 119).",
])
mbody += legend(408)
msvg = wrap(426, mbody, "MBOR architecture")
mbor_dir = Path(os.path.expanduser("~/code/mbor/docs"))
if mbor_dir.exists():
    (mbor_dir / "mbor-arch.svg").write_text(msvg)
    print(f"OK mbor: {len(msvg)} bytes -> ~/code/mbor/docs/mbor-arch.svg")
else:
    (OUT / "mbor.svg").write_text(msvg)
    print(f"OK mbor (fallback to curated_figs): {len(msvg)} bytes")
