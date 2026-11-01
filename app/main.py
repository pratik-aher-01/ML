from html import escape
import json
from pathlib import Path

import markdown
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI(
    title="ML Practical Cloud",
    description="Browser-readable machine learning practicals",
    version="2.0.0",
)
NOTEBOOK_DIR = Path(__file__).resolve().parent.parent / "notebooks"

PRACTICALS = {
    1: ("Feature Engineering", "01_feature_engineering.ipynb"),
    2: ("PCA — Dimensionality Reduction", "02a_pca.ipynb"),
    3: ("LDA — Dimensionality Reduction", "02b_lda.ipynb"),
    4: ("Multiple Linear Regression", "03_multiple_linear_regression.ipynb"),
    5: ("Polynomial Regression", "04_polynomial_regression.ipynb"),
    6: ("Ridge Regression", "05a_ridge_regression.ipynb"),
    7: ("Lasso Regression", "05b_lasso_regression.ipynb"),
    8: ("Logistic Regression", "06_logistic_regression.ipynb"),
    9: ("SVM — Linear Kernel", "07a_svm_linear_kernel.ipynb"),
    10: ("SVM — Nonlinear Kernel", "07b_svm_nonlinear_kernel.ipynb"),
    11: ("K-Means Clustering", "08_kmeans_clustering.ipynb"),
    12: ("DBSCAN Clustering", "09_dbscan_clustering.ipynb"),
    13: ("Ensemble Learning", "10_ensemble_learning.ipynb"),
    14: ("Reinforcement Learning — Q-Learning", "11_q_learning_grid_world.ipynb"),
}


@app.get("/", response_class=HTMLResponse)
def home():
    items = "".join(
        f'<li><a href="/{pid}"><strong>{escape(title)}</strong><span>Open practical →</span></a></li>'
        for pid, (title, _) in PRACTICALS.items()
    )
    return page("ML Practicals", f"""
      <header><p class="eyebrow">MACHINE LEARNING LAB</p><h1>Practical Library</h1>
      <p class="muted">Choose a practical to view its complete code and explanations.</p></header>
      <ol class="index">{items}</ol>
    """)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "ML Practical Cloud"}


@app.get("/practicals")
def list_practicals():
    return [
        {"id": pid, "title": title, "url": f"/{pid}", "download": f"/download/{pid}"}
        for pid, (title, _) in PRACTICALS.items()
    ]


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · ML Practicals</title>
<style>
:root{{--bg:#f6f7fb;--panel:#fff;--ink:#182033;--muted:#647084;--line:#e5e8ef;--accent:#3659d9;--code:#111827}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 system-ui,-apple-system,Segoe UI,sans-serif}}
main{{max-width:920px;margin:40px auto;padding:0 20px 64px}}header{{margin-bottom:28px}}h1{{font-size:clamp(28px,5vw,42px);line-height:1.15;margin:4px 0 10px}}h2{{margin-top:0}}.eyebrow{{font-size:12px;letter-spacing:.14em;font-weight:700;color:var(--accent)}}.muted,caption{{color:var(--muted)}}
.index{{padding:0;list-style:none;display:grid;gap:10px}}.index li a{{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:16px 18px;background:var(--panel);border:1px solid var(--line);border-radius:12px;color:var(--ink);text-decoration:none}}.index li a span{{color:var(--accent);white-space:nowrap;font-size:14px}}
.top{{display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:24px}}a{{color:var(--accent)}}.cell{{background:var(--panel);border:1px solid var(--line);border-radius:12px;margin:16px 0;overflow:hidden}}.markdown{{padding:18px 22px}}.markdown pre{{overflow:auto;background:#f0f2f7;padding:12px;border-radius:8px}}.markdown code{{background:#eef0f5;padding:2px 5px;border-radius:4px}}.markdown pre code{{background:none;padding:0}}
.code-head{{display:flex;justify-content:space-between;align-items:center;padding:9px 14px;background:#202b3d;color:#dce5f5;font-size:12px}}button,.pill{{border:1px solid #526078;border-radius:7px;padding:6px 11px;background:#34435c;color:white;cursor:pointer;font:inherit;font-size:12px}}.code{{margin:0;padding:18px;overflow:auto;background:var(--code);color:#e5e7eb;font:13px/1.65 ui-monospace,SFMono-Regular,Consolas,monospace;tab-size:4;white-space:pre}}
footer{{margin-top:30px;color:var(--muted);font-size:13px}}@media(max-width:600px){{main{{margin:24px auto}}.index li a{{align-items:flex-start;flex-direction:column}}}}
</style></head><body><main>{body}</main>
<script>
function copyCell(button){{const code=button.closest('.cell').querySelector('pre.code').innerText;navigator.clipboard.writeText(code).then(()=>{{button.textContent='Copied!';setTimeout(()=>button.textContent='Copy code',1400)}}).catch(()=>{{button.textContent='Copy unavailable'}})}}
</script></body></html>"""


def render_notebook(practical_id: int) -> str:
    practical = PRACTICALS.get(practical_id)
    if practical is None:
        raise HTTPException(status_code=404, detail="Practical not found")
    path = NOTEBOOK_DIR / practical[1]
    if not path.is_file():
        raise HTTPException(status_code=500, detail="Notebook file is missing")
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise HTTPException(status_code=500, detail="Notebook could not be read")

    cells = []
    code_number = 0
    for cell in notebook.get("cells", []):
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        if cell.get("cell_type") == "markdown":
            rendered = markdown.markdown(source, extensions=["fenced_code", "tables"])
            cells.append(f'<section class="cell markdown">{rendered}</section>')
        elif cell.get("cell_type") == "code":
            code_number += 1
            cells.append(
                f'<section class="cell"><div class="code-head"><span>CODE CELL {code_number}</span>'
                f'<button type="button" onclick="copyCell(this)">Copy code</button></div>'
                f'<pre class="code"><code>{escape(source)}</code></pre></section>'
            )

    title = practical[0]
    nav = '<a href="/">← All practicals</a>'
    download = f'<a class="pill" href="/download/{practical_id}">Download .ipynb</a>'
    body = (
        f'<div class="top">{nav}{download}</div><header><p class="eyebrow">PRACTICAL {practical_id:02d} / 14</p>'
        f'<h1>{escape(title)}</h1><p class="muted">Complete practical with explanations and copyable code cells.</p></header>'
        + "".join(cells)
        + '<footer>Code runs in your local Python or Jupyter environment. Use the copy buttons to reuse individual cells.</footer>'
    )
    return page(title, body)


@app.get("/download/{practical_id}")
def download_practical(practical_id: int):
    practical = PRACTICALS.get(practical_id)
    if practical is None:
        raise HTTPException(status_code=404, detail="Practical not found")
    path = NOTEBOOK_DIR / practical[1]
    if not path.is_file():
        raise HTTPException(status_code=500, detail="Notebook file is missing")
    return FileResponse(path, media_type="application/x-ipynb+json", filename=path.name)


@app.get("/t/{practical_id}", response_class=HTMLResponse)
def legacy_practical_url(practical_id: int):
    return HTMLResponse(render_notebook(practical_id))


@app.get("/{practical_id}", response_class=HTMLResponse)
def practical_url(practical_id: int):
    return HTMLResponse(render_notebook(practical_id))
