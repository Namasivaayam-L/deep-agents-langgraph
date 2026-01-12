"""HTML UI generation tool using Gemini API."""
import re, os
from langchain_core.tools import tool
from google import genai
from google.genai import types


_client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )


_HTML_PROMPT_TEMPLATE = """Generate a modern, responsive HTML page with inline CSS.
Tech: Semantic HTML5, CSS3, no external libraries.
Design: Clean, professional, accessible, with hover states.


Screen to generate:
{screen_description}


Output ONLY the complete HTML code, nothing else."""




def _sanitize_filename(filename: str) -> str:
    """Sanitize filename to be filesystem-safe."""
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename).replace(' ', '_')
    sanitized = re.sub(r'_+', '_', sanitized)
    if not sanitized.lower().endswith('.html'):
        sanitized += '.html'
    return sanitized.lower()[:200]




@tool
def generate_html(screen_description: str, filename: str = "output.html") -> str:
    """Generates HTML/CSS code for a UI screen."""
    response = _client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[_HTML_PROMPT_TEMPLATE.format(screen_description=screen_description)],
        config=types.GenerateContentConfig(temperature=0.7),
    )
    html_content = response.text
    safe_name = _sanitize_filename(filename)
    with open(safe_name, "w", encoding="utf-8") as f:
        f.write(html_content)
    return f"HTML saved: {safe_name}"
