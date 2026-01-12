"""Image generation tool using Gemini API."""
import re, os
from langchain_core.tools import tool
from google import genai
from google.genai import types


_client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )




def _sanitize_filename(filename: str) -> str:
    """Sanitize filename to be filesystem-safe."""
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename).replace(' ', '_')
    sanitized = re.sub(r'_+', '_', sanitized)
    if not sanitized.lower().endswith('.png'):
        sanitized += '.png'
    return sanitized.lower()[:200]




@tool
def generate_image(prompt: str, filename: str = "output.png") -> str:
    """Generates an image from a prompt using Gemini."""
    response = _client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt],
        config=types.GenerateContentConfig(top_p=0.95, temperature=0, seed=42),
    )
    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            safe_name = _sanitize_filename(filename)
            image.save(safe_name)
            return f"Image saved: {safe_name}"
    return "Image generation failed."
