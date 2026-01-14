"""Skill parser utilities."""
import logging
import re
import yaml
from pathlib import Path
from typing import Any, Tuple

# Configure logging
logger = logging.getLogger(__name__)


def _parse_frontmatter(content: str, file_path: Path = None) -> Tuple[dict[str, Any], str, Path]:
    """Parse YAML frontmatter from markdown content.

    Args:
        content: Markdown content to parse
        file_path: Optional path to the file being parsed

    Returns:
        Tuple of (frontmatter_dict, body_content, file_path)
    """
    logger.debug(f"Parsing frontmatter from {file_path or 'unknown file'}")
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
            body = match.group(2).strip()
            logger.debug(f"Successfully parsed frontmatter with keys: {list(frontmatter.keys())}")
            return frontmatter, body, file_path
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in {file_path}: {e}")
            return {}, content.strip(), file_path

    logger.debug(f"No frontmatter found in {file_path or 'unknown file'}")
    return {}, content.strip(), file_path
