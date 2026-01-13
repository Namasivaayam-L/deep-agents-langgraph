"""Main agent for BA Deep Agent using skill-based subagents."""
from deepagents import create_deep_agent
from langchain_groq import ChatGroq
import os

from config import DEFAULT_MODEL, GROQ_API_KEY
from utils import load_skill_subagents

# Load skill subagents
skill_subagents = load_skill_subagents()
from tools import (
    generate_pdf,
    generate_docx,
    generate_csv,
    generate_image,
    generate_html,
)

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", None)
os.environ["LANGSMITH_TRACING"] = "true"

_ROOT_PROMPT = """You are the root orchestrator for Business Analyst workflows using skill-based subagents.

## Your Role
You decompose complex tasks into subtasks and delegate them to specialized skill subagents that have the appropriate tools and expertise for each task.

## Workflow

### Step 1: Analyze Request
- Understand the user's request
- Break down the request into logical subtasks

### Step 2: Delegate to Subagents
- Delegate each subtask to the most appropriate skill subagent:

### Step 3: Execute and Coordinate
- Each subagent will handle their specific task with their assigned tools
- Coordinate between subagents when tasks depend on each other
- Keep the user informed of progress and results

Always be helpful, clear, and guide the user through the complete workflow.
"""

# Initialize Groq compound model
_model = ChatGroq(
    model=DEFAULT_MODEL,
    api_key=GROQ_API_KEY,
)

# Format skill list for the prompt
skill_descriptions = []
for subagent in skill_subagents:
    skill_descriptions.append(f"- `{subagent['name']}`: {subagent['description']}")

formatted_prompt = _ROOT_PROMPT.format(skill_list="\n".join(skill_descriptions))

# All tools available for the root agent
_all_tools = [
    generate_pdf,
    generate_docx,
    generate_csv,
    generate_image,
    generate_html,
]

# Create the agent
agent = create_deep_agent(
    model=_model,
    system_prompt=formatted_prompt,
    # subagents=skill_subagents,
    tools=_all_tools,
)

__all__ = ["agent"]
