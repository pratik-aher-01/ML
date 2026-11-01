from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI(title="ML Practical Cloud", description="Jupyter-native ML practical notebooks", version="1.0.0")
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
    links = "".join(
        f'<li><b>{title}</b> — <a href="/t/{pid}">Download notebook</a> (<code>/t/{pid}</code>)</li>'
        for pid, (title, _) in PRACTICALS.items()
    )
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>ML Practical Cloud</title><style>body{{font:16px system-ui;max-width:850px;margin:48px auto;padding:0 20px;color:#172033}}li{{padding:10px 0;border-bottom:1px solid #e5e7eb}}a{{color:#2563eb}}code{{background:#f1f5f9;padding:3px 6px;border-radius:5px}}</style>
    </head><body><h1>ML Practical Cloud</h1><p>Download real Jupyter notebooks and execute cells locally in Anaconda.</p>
    <p><a href="/practicals">JSON API</a> · <a href="/docs">API docs</a> · <a href="/health">Health</a></p><ol>{links}</ol></body></html>"""

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ML Practical Cloud"}

@app.get("/practicals")
def list_practicals():
    return [{"id": pid, "title": title, "endpoint": f"/t/{pid}", "filename": filename}
            for pid, (title, filename) in PRACTICALS.items()]

@app.get("/t/{practical_id}")
def get_practical(practical_id: int):
    practical = PRACTICALS.get(practical_id)
    if practical is None:
        raise HTTPException(status_code=404, detail="Practical not found")
    path = NOTEBOOK_DIR / practical[1]
    if not path.is_file():
        raise HTTPException(status_code=500, detail="Notebook file is missing")
    return FileResponse(path, media_type="application/x-ipynb+json", filename=path.name)
