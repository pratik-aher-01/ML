# ML Practical Cloud

A lightweight FastAPI service that serves all 14 Machine Learning practicals as readable browser pages with copyable code cells.

## One short URL per practical

After deployment, open:

- `https://YOUR-APP.onrender.com/1` — Feature Engineering
- `https://YOUR-APP.onrender.com/2` — PCA
- `https://YOUR-APP.onrender.com/3` — LDA
- `https://YOUR-APP.onrender.com/4` — Multiple Linear Regression
- `https://YOUR-APP.onrender.com/5` — Polynomial Regression
- `https://YOUR-APP.onrender.com/6` — Ridge Regression
- `https://YOUR-APP.onrender.com/7` — Lasso Regression
- `https://YOUR-APP.onrender.com/8` — Logistic Regression
- `https://YOUR-APP.onrender.com/9` — SVM Linear Kernel
- `https://YOUR-APP.onrender.com/10` — SVM Nonlinear Kernel
- `https://YOUR-APP.onrender.com/11` — K-Means
- `https://YOUR-APP.onrender.com/12` — DBSCAN
- `https://YOUR-APP.onrender.com/13` — Ensemble Learning
- `https://YOUR-APP.onrender.com/14` — Q-Learning

The practical page shows Markdown explanations and code cells directly in the browser. Use **Copy code** on any code cell. The optional **Download .ipynb** link preserves the original notebook.

## Deploy on Render

Render uses `render.yaml` in the repository root. Connect the GitHub repository as a Blueprint, or trigger a deploy for the existing service after pushing changes.

## Other endpoints

- `/` — practical index
- `/health` — health check
- `/practicals` — JSON list of all practicals
- `/download/{id}` — download the original notebook
- `/t/{id}` — compatibility URL for the browser practical page

## Local development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The hosted service displays and distributes notebooks; Python code executes in your local Jupyter/Python environment, not on Render.
