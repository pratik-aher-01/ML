# ML Practical Cloud

Jupyter-native ML practical library built from the provided Machine Learning practical statement. Every endpoint serves a real `.ipynb` file with separate Markdown and code cells. The API distributes files; all experiment code executes locally in your Anaconda environment.

## Deploy on Render

1. Push/confirm this repository on GitHub.
2. In Render choose **New → Blueprint** and connect this repository.
3. Render detects `render.yaml` and creates the web service.
4. Test `/health`, `/practicals`, and `/docs`.

## Use in Anaconda Jupyter Notebook

In a notebook cell, replace the base URL with the Render URL assigned to your service:

```python
!curl -L https://YOUR-APP.onrender.com/t/4 -o 03_multiple_linear_regression.ipynb
```

Refresh the Jupyter file browser and open the downloaded notebook. Execute code cells individually using **Shift + Enter**. Editing and Ctrl+Z undo/redo remain native Jupyter behavior.

## Endpoint map

| ID | Experiment |
|---:|---|
| 1 | Feature Engineering |
| 2 | PCA |
| 3 | LDA |
| 4 | Multiple Linear Regression |
| 5 | Polynomial Regression |
| 6 | Ridge Regression |
| 7 | Lasso Regression |
| 8 | Logistic Regression |
| 9 | SVM — Linear Kernel |
| 10 | SVM — Nonlinear Kernel |
| 11 | K-Means Clustering |
| 12 | DBSCAN Clustering |
| 13 | Ensemble Learning |
| 14 | Reinforcement Learning — Q-Learning |

The supplied statement contains 11 numbered headings with PCA/LDA, Ridge/Lasso, and Linear/Nonlinear SVM as separate subparts. They are exposed as 14 distinct notebooks/endpoints.

## API endpoints

- `GET /` — simple practical index page
- `GET /health` — health status
- `GET /practicals` — JSON list of notebooks
- `GET /t/{id}` — download notebook by ID

## Local notebook dependencies

The hosted API needs only FastAPI and Uvicorn. Your local Anaconda kernel needs the ML libraries used in the notebooks:

```bash
pip install numpy pandas matplotlib scikit-learn nbformat
```

Some examples fetch open datasets on first execution and require internet access.

## Local API development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Notes

- Render does not execute notebook code and does not need your ML libraries.
- Notebook code runs on your laptop, preserving local files and Jupyter's native editor.
- Notebooks are committed with empty outputs and unexecuted code cells.
