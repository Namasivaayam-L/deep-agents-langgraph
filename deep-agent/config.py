"""Configuration for BA Deep Agent V2."""
import logging
import os
from pathlib import Path
from dotenv import load_dotenv


# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()
logger.info("Loaded environment variables from .env")


# Paths
PROJECT_ROOT = Path(__file__).parent
SKILLS_DIR = PROJECT_ROOT / "skills"
logger.debug(f"Project root: {PROJECT_ROOT}")
logger.debug(f"Skills directory: {SKILLS_DIR}")


# Provider API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if OPENROUTER_API_KEY:
    logger.info("OpenRouter API key loaded from environment")
else:
    logger.warning("OPENROUTER_API_KEY not found in environment")
if GROQ_API_KEY:
    logger.info("Groq API key loaded from environment")
else:
    logger.debug("GROQ_API_KEY not found in environment")


# Models
# OpenRouter model: nvidia/nemotron-3-nano-30b-a3b:free
MODEL_OPENROUTER_NAME = "nvidia/nemotron-3-nano-30b-a3b:free"
MODEL_OPENROUTER_NAME = "xiaomi/mimo-v2-flash:free"
MODEL_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_GROQ_COMPOUND = "meta-llama/llama-4-scout-17b-16e-instruct"

# Default model configuration (change as needed)
DEFAULT_MODEL_NAME = MODEL_OPENROUTER_NAME
DEFAULT_MODEL_PROVIDER = "openai"
DEFAULT_MODEL_BASE_URL = MODEL_OPENROUTER_BASE_URL

logger.info(f"Default model configured: {DEFAULT_MODEL_NAME}")
logger.info(f"Model provider: {DEFAULT_MODEL_PROVIDER}")
logger.debug(f"Base URL: {DEFAULT_MODEL_BASE_URL}")
