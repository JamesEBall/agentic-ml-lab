"""File I/O and agent communication utilities for the Agentic ML Research Lab."""

import os
from datetime import datetime


PROJECT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "project")


def ensure_project_dirs():
    """Create standard project subdirectories."""
    dirs = [
        "data", "configs", "results", "visualizations", "logs", "scripts",
        "visualizations/eda", "visualizations/training", "visualizations/analysis",
        "research",
    ]
    for d in dirs:
        os.makedirs(os.path.join(PROJECT_DIR, d), exist_ok=True)


def update_status(agent_name: str, status: str, summary: str, details: str = ""):
    """Append a status update to project/status.md.

    Args:
        agent_name: Name of the agent reporting.
        status: running | completed | blocked | failed
        summary: One-line summary.
        details: Optional additional details.
    """
    status_path = os.path.join(PROJECT_DIR, "status.md")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"\n## [{timestamp}] {agent_name}\n"
    entry += f"**Status:** {status}\n"
    entry += f"**Summary:** {summary}\n"
    if details:
        entry += f"**Details:** {details}\n"
    entry += "---\n"

    # Create file with header if it doesn't exist
    if not os.path.exists(status_path):
        with open(status_path, "w") as f:
            f.write("# Project Status Log\n\n")

    with open(status_path, "a") as f:
        f.write(entry)


def read_status() -> str:
    """Read the full status log."""
    status_path = os.path.join(PROJECT_DIR, "status.md")
    if not os.path.exists(status_path):
        return ""
    with open(status_path, "r") as f:
        return f.read()


def read_template(template_name: str) -> str:
    """Read a template file from templates/.

    Args:
        template_name: Name without path, e.g. "problem_spec.md"

    Returns:
        Template content as string.
    """
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    path = os.path.join(template_dir, template_name)
    with open(path, "r") as f:
        return f.read()


def write_project_file(relative_path: str, content: str):
    """Write a file to the project directory.

    Args:
        relative_path: Path relative to project/, e.g. "problem_spec.md"
        content: File content.
    """
    path = os.path.join(PROJECT_DIR, relative_path)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def read_project_file(relative_path: str) -> str:
    """Read a file from the project directory.

    Args:
        relative_path: Path relative to project/

    Returns:
        File content as string.
    """
    path = os.path.join(PROJECT_DIR, relative_path)
    with open(path, "r") as f:
        return f.read()


def list_project_files(subdirectory: str = "") -> list[str]:
    """List files in a project subdirectory.

    Args:
        subdirectory: Subdirectory relative to project/, e.g. "configs"

    Returns:
        List of filenames.
    """
    path = os.path.join(PROJECT_DIR, subdirectory)
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))


def list_configs() -> list[str]:
    """List YAML config files in project/configs/."""
    return [f for f in list_project_files("configs") if f.endswith((".yaml", ".yml"))]


def list_results() -> list[str]:
    """List result files in project/results/."""
    return list_project_files("results")
