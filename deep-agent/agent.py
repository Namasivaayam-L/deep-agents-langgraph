"""Main agent for BA Deep Agent using skill-based subagents."""
import logging
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from os import getenv
from pathlib import Path
import os

# Configure logging
logger = logging.getLogger(__name__)

from config import (
    DEFAULT_MODEL_NAME,
    DEFAULT_MODEL_PROVIDER,
    DEFAULT_MODEL_BASE_URL,
    OPENROUTER_API_KEY,
)
from utils import load_skill_subagents

logger.info("Agent module initialized")

# Load skill subagents
logger.info("Loading skill subagents...")
skill_subagents = load_skill_subagents()
logger.info(f"Loaded {len(skill_subagents)} skills: {[s['name'] for s in skill_subagents]}")
from tools import (
    generate_pdf,
    generate_docx,
    generate_csv,
    generate_image,
    generate_html,
)

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", None)
os.environ["LANGSMITH_TRACING"] = "true"
logger.debug("LangSmith tracing enabled")

# Load root prompt from file
PROMPTS_DIR = Path(__file__).parent / "prompts"
ROOT_PROMPT_FILE = PROMPTS_DIR / "root.md"
logger.debug(f"Loading root prompt from: {ROOT_PROMPT_FILE}")
_ROOT_PROMPT = ROOT_PROMPT_FILE.read_text(encoding="utf-8")
logger.info("Root prompt loaded successfully")

# Ensure OpenRouter key is available to providers that read env
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY", OPENROUTER_API_KEY)

# Initialize OpenRouter chat model via langchain's init_chat_model
logger.info("Initializing OpenRouter chat model...")
logger.debug(f"Model: {DEFAULT_MODEL_NAME}, Provider: {DEFAULT_MODEL_PROVIDER}")
_model = init_chat_model(
    model=DEFAULT_MODEL_NAME,
    model_provider=DEFAULT_MODEL_PROVIDER,
    base_url=DEFAULT_MODEL_BASE_URL,
    api_key=getenv("OPENROUTER_API_KEY") or OPENROUTER_API_KEY,
)
logger.info("Chat model initialized successfully")

# Format skill list for the prompt
logger.debug("Formatting skill descriptions for prompt...")
skill_descriptions = []
for subagent in skill_subagents:
    skill_descriptions.append(
        f"- **{subagent['name']}**: {subagent['description']}\n"
        f"  Path: {subagent.get('skill_path', 'N/A')}"
    )

formatted_prompt = _ROOT_PROMPT.format(skill_list="\n".join(skill_descriptions))
logger.debug(f"Prompt formatted with {len(skill_descriptions)} skills")

# All tools available for the root agent
_all_tools = [
    generate_pdf,
    generate_docx,
    generate_csv,
    generate_image,
    generate_html,
]
logger.debug(f"Registered {len(_all_tools)} tools for root agent")

# Create the agent
logger.info("Creating deep agent...")
agent = create_deep_agent(
    model=_model,
    system_prompt=formatted_prompt,
    # subagents=skill_subagents,
    tools=_all_tools,
)
logger.info("Deep agent created successfully")

__all__ = ["agent"]
