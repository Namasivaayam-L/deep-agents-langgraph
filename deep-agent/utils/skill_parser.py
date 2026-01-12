"""Skill parser utilities."""
import re
import yaml
from typing import Any, Tuple


def _parse_frontmatter(content: str) -> Tuple[dict[str, Any], str]:
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
