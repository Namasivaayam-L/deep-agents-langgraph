"""Skill loader utilities."""
from pathlib import Path
from typing import Any, Dict, List

from config import SKILLS_DIR, DEFAULT_MODEL
from tools import TOOL_REGISTRY
from .skill_parser import _parse_frontmatter


def load_skill_subagents() -> List[Dict[str, Any]]:
    """Load all skill subagents from the skills directory.

    Reads prompt.md files from each skill folder, parses the frontmatter,
    and creates subagent dictionaries with the appropriate tools.

    Returns:
        List of subagent dictionaries
    """
    subagents = []

    if not SKILLS_DIR.exists():
        return subagents

    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith((".", "_")):
            prompt_file = skill_dir / "prompt.md"

            if not prompt_file.exists():
                continue

            content = prompt_file.read_text(encoding="utf-8")
            frontmatter, body = _parse_frontmatter(content)

            # Get skill metadata
            name = frontmatter.get("name", skill_dir.name)
            description = frontmatter.get("description", "No description available")
            tool_names = frontmatter.get("tools", [])

            # Map tool names to actual tool functions
            tools = []
            for tool_name in tool_names:
                if tool_name in TOOL_REGISTRY:
                    tools.append(TOOL_REGISTRY[tool_name])

            # Create subagent dict
            subagent = {
                "name": name,
                "description": description,
                "system_prompt": body,
                "tools": tools,
                # "model": DEFAULT_MODEL,
            }

            subagents.append(subagent)

    return subagents
