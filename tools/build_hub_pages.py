#!/usr/bin/env python3
"""Build CMU-style hub landing pages (docs/index.html) for the 5 projects that lack one.
Each page: hero + inlined curated SVG + abstract + honest-scope callout + real-vs-scaffold
table + a 'Validated output' evidence section + links (paper, HF demo, explainer, code).
Grounded in the explainers; evidence numbers are the live reproduced test counts."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
CUR = ROOT / "tools" / "curated_figs"

CSS = """
:root{--bg:#fbfcfe;--panel:#fff;--ink:#16202c;--mut:#5b6776;--line:#e6eaf0;--acc:#2257d6;--acc2:#0e9f6e;--warn:#b45309;--chip:#eef2f9;--code:#f3f5f9}
@media(prefers-color-scheme:dark){:root{--bg:#0e1116;--panel:#161b22;--ink:#e7ecf3;--mut:#9aa6b4;--line:#252c37;--acc:#6ea8fe;--acc2:#54d6a0;--warn:#ffb454;--chip:#1b212b;--code:#11151b}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Noto Sans',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.65;font-size:16px}
h1,h2,h3{font-family:Montserrat,system-ui,sans-serif}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:980px;margin:0 auto;padding:0 22px}
header.hero{padding:54px 0 26px;text-align:center;border-bottom:1px solid var(--line)}
.kept{font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--mut);font-weight:700}
h1.title{font-size:38px;line-height:1.12;margin:14px 0 6px;font-weight:800}
.subtitle{font-size:18px;color:var(--mut);max-width:780px;margin:0 auto 8px}
.authors{margin:14px 0 4px;font-size:16px}.aff{color:var(--mut);font-size:14px}
.links{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:20px 0 4px}
.btn{display:inline-flex;align-items:center;gap:7px;background:var(--ink);color:var(--bg);padding:8px 15px;border-radius:999px;font-weight:600;font-size:14px}
.btn.go{background:var(--acc);color:#fff}.btn.alt{background:transparent;color:var(--ink);border:1px solid var(--line)}
.btn:hover{text-decoration:none;opacity:.92}
.pills{display:flex;gap:7px;justify-content:center;flex-wrap:wrap;margin:16px 0 0}
.pill{background:var(--chip);color:var(--mut);border:1px solid var(--line);border-radius:999px;padding:3px 11px;font-size:12.5px;font-weight:600}
section{padding:30px 0;border-bottom:1px solid var(--line)}
h2{font-size:24px;margin:0 0 12px}h3{font-size:17px;margin:18px 0 6px}
p{margin:10px 0}.lead{font-size:17px}
.fig{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin:14px 0}
.figcap{color:var(--mut);font-size:13.5px;margin-top:8px;text-align:center}
.callout{border-left:4px solid var(--acc2);background:var(--panel);border-radius:0 10px 10px 0;padding:14px 16px;margin:14px 0}
.callout.warn{border-left-color:var(--warn)}.callout b{font-family:Montserrat}
table{width:100%;border-collapse:collapse;margin:12px 0;font-size:14.5px}
th,td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
th{background:var(--chip);font-family:Montserrat;font-size:13px}
.ok{color:var(--acc2);font-weight:700}.scaf{color:var(--warn);font-weight:700}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13.5px;background:var(--code);padding:1px 6px;border-radius:5px}
ul{margin:8px 0;padding-left:22px}li{margin:5px 0}
footer{padding:26px 0 50px;color:var(--mut);font-size:13.5px;text-align:center}
@media(max-width:740px){h1.title{font-size:30px}}
"""

# per-project content (grounded in the public explainers + live reproduced test counts)
P = {
 "sat-splat-distort": dict(
  title="Sat-Splat-Distort", kept="Distortion-Aware 3D Vision",
  sub="Make 3D Gaussian Splatting work for non-pinhole cameras (satellite, pushbroom, fisheye, 360) by replacing the one wrong matrix in the standard rasterizer with an exact, per-camera, closed-form Jacobian, plus a small learned grid that mops up residual lens noise.",
  pills=["4 closed-form camera Jacobians","Autograd-validated","Learned distortion grid","20/20 tests pass"],
  abstract="Standard 3D Gaussian Splatting assumes a pinhole camera, so it breaks on the cameras that matter for Earth observation. Sat-Splat-Distort derives the exact projection Jacobian in closed form for four non-pinhole camera models and validates each numerically against <code>torch.autograd</code>, then adds a learned distortion-prior grid for residual lens noise.",
  scope="The genuine, tested contribution is the <b>four closed-form camera Jacobians</b> (each validated against autograd) and the <b>learned distortion-prior grid</b> module. The full GPU 3DGS fit uses a forked CUDA rasterizer that is loaded lazily and <b>stubbed for CPU smoke</b>; the README PSNR numbers (e.g. 24.2 on DFC2019) are <b>leaderboard targets, not reproduced</b>.",
  rows=[("4 camera project + analytic Jacobian","ok","Real, pure PyTorch, differentiable"),
        ("Analytic-vs-autograd validation","ok","Real, passing (part of 20/20 tests)"),
        ("DistortionPriorGrid module","ok","Real, CPU-runnable forward"),
        ("CUDA rasterizer fork","scaf","Forked, lazy-loaded, stubbed for CPU"),
        ("Trained checkpoints, PSNR 24.2","scaf","Target, not reproduced")],
  evidence="<b>20/20 tests pass</b> (run live). <b>Reproduced number:</b> the analytic camera Jacobians match <code>torch.autograd</code> to <b>~1e-5 relative error</b> (equirectangular ~1.8e-6, fisheye ~1.0e-5), the closed-form correctness claim is reproduced, not asserted. Full output in <a href=\"docs/EVIDENCE.md\">docs/EVIDENCE.md</a>."),
 "physflow-earth": dict(
  title="PhysFlow-Earth", kept="Physics-Constrained Generative Super-Resolution",
  sub="Super-resolve satellite imagery and climate fields with a generative model (rectified flow + a Diffusion Transformer), with a physics penalty so the sharp output it invents still obeys conservation laws (precipitation mass, divergence-free wind, spectral band ratios) instead of hallucinating impossible textures.",
  pills=["Rectified flow + DiT","Physics residual operators","20/20 tests pass","CV repackaging of published diffusion work"],
  abstract="Generative super-resolution can invent sharp but physically impossible detail. PhysFlow-Earth adds physics residual operators (mass conservation, divergence-free flow, spectral band ratios) to a rectified-flow + Diffusion-Transformer backbone, so the upsampled field stays physically consistent. The method is the CV-vocabulary form of the author's published conditional-diffusion line (Kriging-informed downscaling, PC-RF).",
  scope="The <b>physics residual operators, the rectified-flow training step, and the DiT backbone are real and tested</b>. The <b>trained checkpoints and the benchmark numbers</b> (e.g. PSNR 28.6 beating EDiffSR on WorldStrat) are <b>scaffold / targets</b>, and the 4-step consistency-distillation speedup is an aspirational README claim.",
  rows=[("Physics operators + residual heads","ok","Real, exactness tests pass"),
        ("RectifiedFlow hybrid training step","ok","Real, runs with backward"),
        ("DiTVelocity (DiT + codebook cross-attn)","ok","Real module, forward verified"),
        ("Trained Sentinel-2 / ERA5 checkpoints","scaf","Scaffold"),
        ("PSNR 28.6 beating EDiffSR","scaf","Target, not reproduced")],
  evidence="<b>20/20 tests pass</b> (run live). <b>Reproduced number:</b> the horizontal-divergence operator returns <b>max|div| = 0.0 (exact)</b> on a divergence-free field, so the conservation residual is correct, and the rectified-flow step runs with a backward pass. Full output in <a href=\"docs/EVIDENCE.md\">docs/EVIDENCE.md</a>."),
 "trajprompt": dict(
  title="TrajPrompt", kept="Trajectory-Text Retrieval",
  sub="Type a plain-English question (\"ships drifting suspiciously near pipelines last March\") and get matching ship trajectories on a map, by training a CLIP-style model that aligns AIS trajectories with text, then confirming candidates with TGARD rendezvous detection and a SAM 2 look at the imagery.",
  pills=["Trajectory-text CLIP (InfoNCE)","TGARD rendezvous","18/18 tests pass","SAM 2 confirm (stub)"],
  abstract="TrajPrompt aligns AIS trajectories with natural-language text in a shared embedding space (a CLIP-style contrastive encoder), so a plain-English query retrieves matching trajectories. Candidates are confirmed with the author's TGARD group-rendezvous detector and, in the production path, a SAM 2 look at the Sentinel-2 chip.",
  scope="Real and tested: the <b>trajectory-CLIP encoder</b> with its InfoNCE contrastive loss, and the <b>TGARD group-rendezvous algorithm</b> with pairwise haversine. <b>Stubbed:</b> the SAM 2 / Sentinel-2 chip puller (returns zeros). <b>Scaffold:</b> the trained traj-CLIP checkpoint and the AIS-text pairs dataset.",
  rows=[("TrajCLIPEncoder + InfoNCE loss","ok","Real, tested"),
        ("TGARD find_rendezvous + haversine","ok","Real, tested"),
        ("Sam2ChipPipeline (Sentinel-2 + SAM 2)","scaf","Stub (returns zeros)"),
        ("Trained traj-CLIP checkpoint","scaf","Scaffold"),
        ("AIS-text pairs dataset","scaf","Scaffold")],
  evidence="<b>18/18 tests pass</b> (run live): the contrastive encoder's forward + InfoNCE loss, and TGARD rendezvous (skips short gaps, flags infeasible ones). <b>Reproduced number:</b> <code>haversine_pairwise</code> returns <b>111,195 m for 1 degree</b> of latitude (matches the geodesic reference), the distance backbone behind rendezvous detection. Full output in <a href=\"docs/EVIDENCE.md\">docs/EVIDENCE.md</a>."),
 "pin-service": dict(
  title="Pin-Service", kept="Production Serving Path",
  sub="The production serving path for choosing where a vehicle should actually stop: candidate generation, hard-constraint filtering, ML scoring, congestion-aware re-ranking, and load shedding, behind a gRPC API with full observability.",
  pills=["gRPC serving pipeline","Constraint filtering","Congestion-aware re-rank","Unit + load tests"],
  abstract="Choosing a stop (pickup/drop-off or delivery) is a systems problem, not a lookup: the stop must be on a drivable lane, legal to stop at, walkable to the door, and globally coordinated so demand spikes do not converge on one curb. Pin-Service is a tested reference implementation of that serving path, candidate generation, constraint filtering, ML scoring, congestion-aware re-ranking, and load shedding, behind a gRPC API.",
  scope="This is a clean, <b>tested reference implementation</b> of the canonical serving path (unit tests for each stage + a Locust load test). The <b>engineering pattern is real and runnable</b>; the ML scorer is a gradient-boosted regressor trained on a <b>synthetic</b> satisfaction label and the map / supply signals are fixtures, so the model and data are <b>illustrative</b>.",
  rows=[("Candidate gen, constraint filter, scoring, re-rank, load shed","ok","Real, tested per stage"),
        ("gRPC API + observability","ok","Real"),
        ("Locust load test","ok","Real, runnable"),
        ("ML scorer (GBDT)","scaf","Trained on a synthetic label, illustrative"),
        ("HD-map + supply signals","scaf","Fixtures / stubs")],
  evidence="A tested reference serving implementation (~1,100 LOC; unit tests per stage + a Locust load test). The serving <b>pattern</b> is reproduced and runnable; the scorer model and map/supply data are illustrative. See <a href=\"docs/EVIDENCE.md\">docs/EVIDENCE.md</a>."),
 "pi-grpo": dict(
  title="Pi-GRPO", kept="Physics-Informed RL Post-Training",
  sub="Physics-informed reinforcement-learning post-training for trajectory generation that treats hard physical constraints as a reward floor, so a policy optimized with PPO, DPO, or GRPO improves task quality without learning to produce physically impossible trajectories.",
  pills=["PPO / DPO / GRPO","Physics reward floor","GRPO normalization finding"],
  abstract="RL post-training (PPO, DPO, GRPO) can reward-hack into physically impossible outputs. Pi-GRPO makes the physics a hard reward floor: the reward is a hybrid of the task reward and a term that heavily penalizes kinematic-constraint violations, shared unchanged across all three optimizers by construction. A workshop paper built on this reward was submitted and rejected; the follow-up audit found that GRPO's own group-relative advantage normalization can silently defeat the floor.",
  scope="The GRPO training loop and the hybrid physics reward are <b>real and run</b>. PPO and DPO are implemented but were <b>never trained</b>, so no result exists for either. The workshop paper's reward-hacking probe was reviewed and rejected as a synthetic construction rather than a trained-model test, and the reviewer was right. The follow-up audit found something more useful: GRPO z-scores each sampled completion against its own group before computing a gradient, so a constraint-violating completion can receive a <b>positive</b> training signal whenever it merely beats its sampled peers, independent of penalty size. Verified with a reproducible script (85.6% of random violator-containing groups reinforce a violator).",
  rows=[("GRPO loop + physics reward","ok","Real, runnable"),
        ("Physics-floor reward (kinematic penalty)","ok","Real"),
        ("GRPO group-normalization failure mode","ok","Real, measured, reproducible (run_groupnorm.py)"),
        ("Matched-budget violation-rate comparison","scaf","Not done; the paper's own comparison was confounded and withdrawn"),
        ("DPO / PPO training results","scaf","Implemented, never trained; no result exists"),
        ("Large-scale benchmark vs RLHF baselines","scaf","Next step, not done")],
  evidence="The GRPO loop and the physics-floor reward are runnable. The workshop submission was rejected on a valid objection (the probe was synthetic, not a trained-model test), and the follow-up audit turned up a real, verified finding instead: GRPO's own group normalization can hand a constraint-violating completion a positive advantage regardless of penalty magnitude. That result, not a violation-rate percentage, is the current headline. See the explainer and paper.")
}

HF = "https://huggingface.co/spaces/Arun0808/{s}"
PAPER = "https://arunshar.com/projects/{s}/"
EXPL = "https://arunshar.com/projects/{s}/explained.html"
CODE = "https://github.com/arunshar/{s}"

def page(slug, m):
    svg = (CUR / f"{slug}.svg").read_text() if (CUR / f"{slug}.svg").exists() else ""
    pills = "".join(f'<span class="pill">{p}</span>' for p in m["pills"])
    rows = "".join(f"<tr><td>{a}</td><td><span class=\"{c}\">{ {'ok':'Real','scaf':'Scaffold/Target'}[c] }</span> &middot; {d}</td></tr>" for a,c,d in m["rows"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{m['title']}: {m['sub'][:80]}...</title>
<meta name="description" content="{m['sub']}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Noto+Sans:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header class="hero"><div class="wrap">
  <div class="kept">{m['kept']}</div>
  <h1 class="title">{m['title']}</h1>
  <div class="subtitle">{m['sub']}</div>
  <div class="authors">Arun Sharma</div><div class="aff">University of Minnesota &middot; research-engineering project</div>
  <div class="links">
    <a class="btn go" href="{PAPER.format(s=slug)}">Full paper</a>
    <a class="btn alt" href="{HF.format(s=slug)}">Live demo (Space)</a>
    <a class="btn alt" href="{EXPL.format(s=slug)}">Deep explainer</a>
    <a class="btn alt" href="{CODE.format(s=slug)}">Code</a>
  </div>
  <div class="pills">{pills}</div>
</div></header>
<section><div class="wrap"><h2>Abstract</h2><p class="lead">{m['abstract']}</p>
  <div class="callout warn"><b>Honest scope.</b> {m['scope']}</div></div></section>
<section><div class="wrap"><h2>Architecture</h2><div class="fig">{svg}<div class="figcap">Green = real and tested; dashed amber = stub or target (off-the-shelf or roadmap).</div></div></div></section>
<section><div class="wrap"><h2>What is real vs scaffold</h2><table><thead><tr><th>Component</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section><div class="wrap"><h2>Validated output</h2><div class="callout">{m['evidence']}</div>
  <p class="lead">You can open the <a href="{HF.format(s=slug)}">live demo</a> to run it, read the <a href="{PAPER.format(s=slug)}">full paper</a>, or go deep in the <a href="{EXPL.format(s=slug)}">explainer</a>.</p></div></section>
<footer><div class="wrap">Research-engineering project. Honest scope stated above; reproduced results are in docs/EVIDENCE.md, leaderboard numbers are targets.
  <br>Built by Arun Sharma &middot; <a href="{PAPER.format(s=slug)}">paper</a> &middot; <a href="{CODE.format(s=slug)}">code</a> &middot; <a href="{HF.format(s=slug)}">demo</a> &middot; <a href="{EXPL.format(s=slug)}">explainer</a></div></footer>
</body></html>"""

for slug, m in P.items():
    d = ROOT / slug / "docs"; d.mkdir(parents=True, exist_ok=True)
    html = page(slug, m).replace('href="docs/EVIDENCE.md"',
                                 f'href="https://github.com/arunshar/{slug}/blob/main/docs/EVIDENCE.md"')
    (d / "index.html").write_text(html)
    (d / ".nojekyll").write_text("")
    print(f"OK {slug} -> docs/index.html ({len((d/'index.html').read_text())} bytes)")
