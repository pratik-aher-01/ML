# ML Practical Cloud

Machine Learning practical notebooks using the exact syllabus IDs. Every notebook contains executable Python code cells only.

## Practical URLs

- `/1` — Feature Engineering (Titanic)
- `/2a` — PCA (Iris)
- `/2b` — LDA (Iris)
- `/3` — Multiple Linear Regression (California Housing)
- `/4` — Polynomial Regression (California Housing)
- `/5a` — Ridge Regression (California Housing)
- `/5b` — Lasso Regression (California Housing)
- `/6` — Logistic Regression (Social Network Ads)
- `/7a` — SVM Linear Kernel (California Housing, linear SVR)
- `/7b` — SVM Nonlinear Kernel (California Housing, RBF SVR)
- `/8` — K-Means Clustering (Mall Customers)
- `/9` — DBSCAN Clustering (Make Moons)
- `/10` — Ensemble Learning / Random Forest (Wisconsin Breast Cancer)
- `/11` — Q-Learning (simulated Grid World; no external dataset supplied)

Hosted service: https://ml-practical-cloud.onrender.com

## Use in Jupyter

1. Download and extract the supplied practical datasets ZIP.
2. Keep the extracted dataset folders somewhere inside the directory from which Jupyter is running (or a subdirectory of it).
3. In a notebook, run the matching command, for example:

```python
!curl -L https://ml-practical-cloud.onrender.com/2a
```

The code searches recursively for the supplied CSV filename, so the original folder structure and filenames can remain unchanged. Run the returned code in Jupyter. Required libraries include pandas, numpy, matplotlib and scikit-learn.

## Browser and download endpoints

- `/` — practical index
- `/health` — health check
- `/practicals` — JSON list
- `/view/{id}` — browser viewer
- `/download/{id}` — original Jupyter notebook
- `/c/{id}` — raw Python code
- `/{id}` — short raw Python code URL

The notebooks execute in the user's Jupyter environment, not on Render.
