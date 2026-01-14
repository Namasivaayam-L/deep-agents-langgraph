"""Skill loader utilities."""
import logging
from pathlib import Path
from typing import Any, Dict, List

# Configure logging
logger = logging.getLogger(__name__)

from config import SKILLS_DIR
from tools import TOOL_REGISTRY
from .skill_parser import _parse_frontmatter


def load_skill_subagents() -> List[Dict[str, Any]]:
    """Load all skill subagents from the skills directory.

    Reads prompt.md files from each skill folder, parses the frontmatter,
    and creates subagent dictionaries with the appropriate tools.

    Returns:
        List of subagent dictionaries
    """
    logger.info("Starting skill discovery...")
    subagents = []

    if not SKILLS_DIR.exists():
        logger.warning(f"Skills directory not found: {SKILLS_DIR}")
        return subagents

    logger.debug(f"Scanning skills directory: {SKILLS_DIR}")
    skill_dirs = [d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith((".", "_"))]
    logger.info(f"Found {len(skill_dirs)} skill directories")

    for skill_dir in skill_dirs:
        logger.debug(f"Loading skill: {skill_dir.name}")
        prompt_file = skill_dir / "SKILL.md"

        if not prompt_file.exists():
            logger.warning(f"prompt.md not found in {skill_dir.name}, skipping")
            continue

        content = prompt_file.read_text(encoding="utf-8")
        frontmatter, body, _ = _parse_frontmatter(content, prompt_file)

        # Get skill metadata
        name = frontmatter.get("name", skill_dir.name)
        description = frontmatter.get("description", "No description available")
        tool_names = frontmatter.get("tools", [])

        # Get the SKILL.md path for this skill
        skill_md_path = skill_dir / "SKILL.md"

        # Map tool names to actual tool functions
        tools = []
        for tool_name in tool_names:
            if tool_name in TOOL_REGISTRY:
                tools.append(TOOL_REGISTRY[tool_name])
                logger.debug(f"  Registered tool: {tool_name}")
            else:
                logger.warning(f"  Tool not found in registry: {tool_name}")

        # Create subagent dict
        subagent = {
            "name": name,
            "description": description,
            "skill_path": str(skill_md_path),  # Path to SKILL.md
            # "system_prompt": body,
            "tools": tools,
            # "model": DEFAULT_MODEL,
        }

        logger.info(f"Loaded skill '{name}' with {len(tools)} tools")
        subagents.append(subagent)

    logger.info(f"Skill discovery complete. Loaded {len(subagents)} skills")
    return subagents
