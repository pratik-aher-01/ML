from __future__ import annotations

import json
import re
from pathlib import Path

import requests
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.display import HTML, display

BASE_URL = "https://ml-practical-cloud.onrender.com"


@magics_class
class MLPracticalMagics(Magics):
    @line_magic
    def mlpractical(self, line: str):
        """Create a code-only notebook from the hosted practical. Usage: %mlpractical 4"""
        value = line.strip()
        if not re.fullmatch(r"\d{1,2}", value):
            print("Usage: %mlpractical 4   (choose a practical number from 1 to 14)")
            return

        practical_id = int(value)
        if not 1 <= practical_id <= 14:
            print("Practical number must be between 1 and 14.")
            return

        url = f"{BASE_URL}/download/{practical_id}"
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        source_nb = response.json()

        cells = []
        for cell in source_nb.get("cells", []):
            if cell.get("cell_type") != "code":
                continue
            source = cell.get("source", "")
            if isinstance(source, list):
                source = "".join(source)
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": source.splitlines(keepends=True),
            })

        if not cells:
            print("No code cells were found in this practical.")
            return

        notebook = {
            "cells": cells,
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {"name": "python"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }

        filename = f"Practical_{practical_id:02d}.ipynb"
        Path(filename).write_text(
            json.dumps(notebook, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
        display(HTML(
            f'<b>Created {filename}</b> with {len(cells)} separate code cells. '
            f'Open this file from Jupyter\'s file browser: '
            f'<code>{filename}</code>.'
        ))


def load_ipython_extension(ipython):
    ipython.register_magics(MLPracticalMagics)
