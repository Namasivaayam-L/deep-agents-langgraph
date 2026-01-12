"""Configuration for BA Deep Agent V2."""
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


# Paths
PROJECT_ROOT = Path(__file__).parent
SKILLS_DIR = PROJECT_ROOT / "skills"


# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Models
MODEL_GROQ_COMPOUND = "meta-llama/llama-4-scout-17b-16e-instruct"
DEFAULT_MODEL = MODEL_GROQ_COMPOUND
