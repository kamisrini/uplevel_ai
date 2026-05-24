#!/usr/bin/env python3

"""Generate a visual diagram for the LangGraph pipeline.

Usage:
  python scripts/visualize_graph.py
  python scripts/visualize_graph.py --out-dir docs/graphs --no-png
"""

from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _prefer_repo_venv_python() -> None:
    """Re-exec with .venv python for consistent runtime when available."""
    venv_python = REPO_ROOT / ".venv" / "bin" / "python"
    already_switched = os.environ.get("UPLEVEL_AI_VENV_REEXEC") == "1"
    if already_switched:
        return
    if not venv_python.exists():
        return
    if sys.executable == str(venv_python) and sys.version_info >= (3, 11):
        return

    env = os.environ.copy()
    env["UPLEVEL_AI_VENV_REEXEC"] = "1"
    os.execve(str(venv_python), [str(venv_python), *sys.argv], env)


def _ensure_pip() -> None:
    """Ensure pip exists for the current interpreter."""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)


def _install_runtime_dependencies() -> None:
    """Install project/runtime dependencies required to construct the graph."""
    required_modules = ["langgraph", "anthropic", "pydantic_settings"]
    missing = [name for name in required_modules if importlib.util.find_spec(name) is None]
    if not missing:
        return

    _ensure_pip()
    print(f"Missing dependencies: {', '.join(missing)}")
    print("Installing project dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "."], cwd=REPO_ROOT, check=True)
    except subprocess.CalledProcessError:
        # Fallback for environments where installing the local package is restricted.
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "langgraph>=0.2.0",
                "anthropic>=0.40.0",
                "pydantic-settings>=2.6.0",
            ],
            check=True,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize the LangGraph pipeline.")
    parser.add_argument(
        "--out-dir",
        default="artifacts/graph",
        help="Directory where output files are written.",
    )
    parser.add_argument(
        "--no-png",
        action="store_true",
        help="Skip PNG generation and only write Mermaid text.",
    )
    return parser.parse_args()


def main() -> int:
    _prefer_repo_venv_python()
    _install_runtime_dependencies()

    from src.agents.graph import build_graph

    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    app = build_graph()
    graph = app.get_graph()

    mermaid_text = graph.draw_mermaid()
    mermaid_path = out_dir / "graph.mmd"
    mermaid_path.write_text(mermaid_text, encoding="utf-8")
    print(f"Wrote Mermaid graph to {mermaid_path}")

    if args.no_png:
        return 0

    png_path = out_dir / "graph.png"
    try:
        png_bytes = graph.draw_mermaid_png()
        png_path.write_bytes(png_bytes)
        print(f"Wrote PNG graph to {png_path}")
    except Exception as exc:  # pragma: no cover
        print(f"PNG generation skipped: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
