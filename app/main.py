from html import escape
import json
from pathlib import Path

import markdown
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse

app = FastAPI(
    title="ML Practical Cloud",
    description="Machine learning practicals using the exact numbering from the lab syllabus",
    version="2.3.0",
)
NOTEBOOK_DIR = Path(__file__).resolve().parent.parent / "notebooks"

# IDs intentionally match the practical labels in the supplied syllabus PDF.
PRACTICALS = {
    "1": ("Feature Engineering", "01_feature_engineering.ipynb"),
    "2a": ("Dimensionality Reduction — PCA", "02a_pca.ipynb"),
    "2b": ("Dimensionality Reduction — LDA", "02b_lda.ipynb"),
    "3": ("Multiple Linear Regression", "03_multiple_linear_regression.ipynb"),
    "4": ("Polynomial Regression", "04_polynomial_regression.ipynb"),
    "5a": ("Regularization Techniques — Ridge Regression", "05a_ridge_regression.ipynb"),
    "5b": ("Regularization Techniques — Lasso Regression", "05b_lasso_regression.ipynb"),
    "6": ("Logistic Regression", "06_logistic_regression.ipynb"),
    "7a": ("Support Vector Machine — Linear Kernel", "07a_svm_linear_kernel.ipynb"),
    "7b": ("Support Vector Machine — Nonlinear Kernel", "07b_svm_nonlinear_kernel.ipynb"),
    "8": ("K-Means Clustering", "08_kmeans_clustering.ipynb"),
    "9": ("DBSCAN Clustering", "09_dbscan_clustering.ipynb"),
    "10": ("Ensemble Learning", "10_ensemble_learning.ipynb"),
    "11": ("Reinforcement Learning — Q-Learning", "11_q_learning_grid_world.ipynb"),
}


def load_notebook(practical_code: str):
    practical = PRACTICALS.get(practical_code.lower())
    if practical is None:
        raise HTTPException(status_code=404, detail="Practical not found")
    path = NOTEBOOK_DIR / practical[1]
    if not path.is_file():
        raise HTTPException(status_code=500, detail="Notebook file is missing")
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise HTTPException(status_code=500, detail="Notebook could not be read")
    return practical, path, notebook


@app.get("/", response_class=HTMLResponse)
def home():
    items = "".join(
        f'<li><a href="/view/{code}"><strong>Practical {escape(code)} — {escape(title)}</strong>'
        f'<span>Open practical →</span></a></li>'
        for code, (title, _) in PRACTICALS.items()
    )
    return page("ML Practicals", f"""
      <header><p class="eyebrow">MACHINE LEARNING LAB</p><h1>Practical Library</h1>
      <p class="muted">Practical numbers follow the official lab syllabus.</p></header>
      <ol class="index">{items}</ol>
    """)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "ML Practical Cloud"}


@app.get("/practicals")
def list_practicals():
    return [
        {"id": code, "title": title, "url": f"/view/{code}", "code": f"/{code}",
         "download": f"/download/{code}"}
        for code, (title, _) in PRACTICALS.items()
    ]


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · ML Practicals</title>
<style>
:root{{--bg:#f6f7fb;--panel:#fff;--ink:#182033;--muted:#647084;--line:#e5e8ef;--accent:#3659d9;--code:#111827}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 system-ui,-apple-system,Segoe UI,sans-serif}}
main{{max-width:920px;margin:40px auto;padding:0 20px 64px}}header{{margin-bottom:28px}}h1{{font-size:clamp(28px,5vw,42px);line-height:1.15;margin:4px 0 10px}}.eyebrow{{font-size:12px;letter-spacing:.14em;font-weight:700;color:var(--accent)}}.muted{{color:var(--muted)}}
.index{{padding:0;list-style:none;display:grid;gap:10px}}.index li a{{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:16px 18px;background:var(--panel);border:1px solid var(--line);border-radius:12px;color:var(--ink);text-decoration:none}}.index li a span{{color:var(--accent);white-space:nowrap;font-size:14px}}
.top{{display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:24px}}a{{color:var(--accent)}}.cell{{background:var(--panel);border:1px solid var(--line);border-radius:12px;margin:16px 0;overflow:hidden}}.markdown{{padding:18px 22px}}.markdown pre{{overflow:auto;background:#f0f2f7;padding:12px;border-radius:8px}}.markdown code{{background:#eef0f5;padding:2px 5px;border-radius:4px}}.markdown pre code{{background:none;padding:0}}
.code-head{{display:flex;justify-content:space-between;align-items:center;padding:9px 14px;background:#202b3d;color:#dce5f5;font-size:12px}}button,.pill{{border:1px solid #526078;border-radius:7px;padding:6px 11px;background:#34435c;color:white;cursor:pointer;font:inherit;font-size:12px}}.code{{margin:0;padding:18px;overflow:auto;background:var(--code);color:#e5e7eb;font:13px/1.65 ui-monospace,SFMono-Regular,Consolas,monospace;tab-size:4;white-space:pre}}
footer{{margin-top:30px;color:var(--muted);font-size:13px}}@media(max-width:600px){{main{{margin:24px auto}}.index li a{{align-items:flex-start;flex-direction:column}}}}
</style></head><body><main>{body}</main>
<script>
function copyCell(button){{const code=button.closest('.cell').querySelector('pre.code').innerText;navigator.clipboard.writeText(code).then(()=>{{button.textContent='Copied!';setTimeout(()=>button.textContent='Copy code',1400)}}).catch(()=>{{button.textContent='Copy unavailable'}})}}
</script></body></html>"""


def render_notebook(practical_code: str) -> str:
    practical, _, notebook = load_notebook(practical_code)
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
    download = f'<a class="pill" href="/download/{practical_code}">Download .ipynb</a>'
    body = (
        f'<div class="top">{nav}{download}</div><header><p class="eyebrow">PRACTICAL {escape(practical_code)}</p>'
        f'<h1>{escape(title)}</h1><p class="muted">Complete practical with explanations and copyable code cells.</p></header>'
        + "".join(cells)
        + f'<footer>Jupyter shortcut: !curl -L https://ml-practical-cloud.onrender.com/{escape(practical_code)}</footer>'
    )
    return page(title, body)


def code_for_practical(practical_code: str) -> str:
    practical, _, notebook = load_notebook(practical_code)
    sections = [f"# Practical {practical_code} — {practical[0]}", "# Loaded directly from ML Practical Cloud"]
    code_number = 0
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        code_number += 1
        sections.append(f"# --- Code cell {code_number} ---\n{source.rstrip()}")
    return "\n\n".join(sections) + "\n"


@app.get("/c/{practical_code}", response_class=PlainTextResponse)
def jupyter_code(practical_code: str):
    return PlainTextResponse(
        code_for_practical(practical_code),
        media_type="text/x-python; charset=utf-8",
    )


@app.get("/download/{practical_code}")
def download_practical(practical_code: str):
    practical, path, _ = load_notebook(practical_code)
    return FileResponse(path, media_type="application/x-ipynb+json", filename=path.name)


@app.get("/view/{practical_code}", response_class=HTMLResponse)
def view_practical(practical_code: str):
    return HTMLResponse(render_notebook(practical_code))


# Preserve the previous /t/<id> viewer URLs.
@app.get("/t/{practical_code}", response_class=HTMLResponse)
def legacy_practical_url(practical_code: str):
    return HTMLResponse(render_notebook(practical_code))


# Short syllabus-based URLs return raw Python code for Jupyter curl.
@app.get("/{practical_code}", response_class=PlainTextResponse)
def practical_url(practical_code: str):
    return PlainTextResponse(
        code_for_practical(practical_code),
        media_type="text/x-python; charset=utf-8",
    )
