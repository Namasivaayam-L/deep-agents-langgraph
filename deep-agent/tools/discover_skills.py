"""Skills discovery tool - scans skills folder and returns available skills with metadata."""
import json
import re
from pathlib import Path
from typing import Any


import yaml
from langchain_core.tools import tool


from config import SKILLS_DIR




def _parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content.
    
    Returns:
        Tuple of (frontmatter_dict, body_content)
    """
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
            body = match.group(2).strip()
            return frontmatter, body
        except yaml.YAMLError:
            return {}, content.strip()
    
    return {}, content.strip()




def _load_skill(skill_dir: Path) -> dict[str, Any] | None:
    """Load a single skill from its directory."""
    prompt_file = skill_dir / "prompt.md"
    
    if not prompt_file.exists():
        return None
    
    content = prompt_file.read_text(encoding="utf-8")
    frontmatter, body = _parse_frontmatter(content)
    
    return {
        "name": frontmatter.get("name", skill_dir.name),
        "description": frontmatter.get("description", "No description available"),
        "tools": frontmatter.get("tools", []),
        "system_prompt": body,
        "path": str(skill_dir),
    }




@tool
def discover_skills() -> str:
    """Discovers all available skills from the skills folder.
    
    Scans the skills directory for subfolders containing prompt.md files.
    Each prompt.md can have YAML frontmatter with name, description, and tools.
    
    Returns:
        JSON string containing list of available skills with their metadata:
        - name: Skill identifier
        - description: What the skill does
        - tools: List of tool names the skill can use
        - system_prompt: The full prompt text for the skill
        - path: Filesystem path to the skill folder
    """
    skills = []
    
    if not SKILLS_DIR.exists():
        return json.dumps({"error": f"Skills directory not found: {SKILLS_DIR}", "skills": []})
    
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith((".", "_")):
            skill = _load_skill(skill_dir)
            if skill:
                skills.append(skill)
    
    return json.dumps({
        "skills_count": len(skills),
        "skills": skills,
    }, indent=2)
