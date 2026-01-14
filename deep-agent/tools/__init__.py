"""Tools for BA Deep Agent V2."""
import logging

# Configure logging
logger = logging.getLogger(__name__)

from .generate_pdf import generate_pdf
from .generate_docx import generate_docx
from .generate_csv import generate_csv
from .generate_image import generate_image
from .generate_html import generate_html

logger.debug("Imported all tool modules")

__all__ = [
    "generate_pdf",
    "generate_docx",
    "generate_csv",
    "generate_image",
    "generate_html",
]

# Tool registry for dynamic lookup by name
TOOL_REGISTRY = {
    "generate_pdf": generate_pdf,
    "generate_docx": generate_docx,
    "generate_csv": generate_csv,
    "generate_image": generate_image,
    "generate_html": generate_html,
}

logger.info(f"Tool registry initialized with {len(TOOL_REGISTRY)} tools")
