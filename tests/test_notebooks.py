import ast
import json
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"

def test_all_notebooks_are_valid_and_have_separate_cells():
    files = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
    assert len(files) == 14
    for path in files:
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
        assert len(code_cells) >= 3
        for cell in code_cells:
            ast.parse(cell.source)

def test_notebooks_have_no_saved_execution_outputs():
    for path in NOTEBOOK_DIR.glob("*.ipynb"):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                assert cell["execution_count"] is None
                assert cell["outputs"] == []
