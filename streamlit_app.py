"""Root launcher so `streamlit run streamlit_app.py` works from repo root.

This uses `runpy` instead of importing with `*` so Streamlit reruns execute
the target app script on every interaction.
"""

from __future__ import annotations

from pathlib import Path
import runpy


APP_FILE = Path(__file__).parent / "app" / "streamlit_app.py"
runpy.run_path(str(APP_FILE), run_name="__main__")
