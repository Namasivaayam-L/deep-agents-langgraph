# BA Deep Agent V2

A skill-based orchestration framework for Business Analyst workflows using LangChain and Deep Agents.

## Overview

The BA Deep Agent is a root orchestrator that decomposes complex business analysis tasks into subtasks and delegates them to specialized skill subagents. Each skill has dedicated tools and a specific prompt loaded from SKILL.md files.

## Architecture

```
deep-agent/
├── agent.py              # Main agent orchestrator
├── config.py             # Configuration and API keys
├── pyproject.toml        # Project metadata and dependencies
├── prompts/
│   └── root.md           # Root orchestrator prompt template
├── utils/
│   ├── skill_loader.py   # Loads skills from skills directory
│   └── skill_parser.py   # Parses YAML frontmatter from markdown
├── tools/
│   ├── generate_pdf.py
│   ├── generate_docx.py
│   ├── generate_csv.py
│   ├── generate_image.py
│   └── generate_html.py
└── skills/
    ├── architect/
    ├── brd_formatter/
    ├── requirement_collector/
    └── uiux_designer/
```

## Configuration

### Environment Variables

Required environment variables (set in `.env`):
```
OPENROUTER_API_KEY=your_openrouter_api_key
LANGSMITH_API_KEY=your_langsmith_api_key  # Optional
```

Optional OpenRouter headers for ranking:
```
YOUR_SITE_URL=https://your-site.com
YOUR_SITE_NAME=Your Site Name
```

### Model Configuration

Default model: **nvidia/nemotron-3-nano-30b-a3b:free** (via OpenRouter)

Edit [config.py](config.py) to change:
- `DEFAULT_MODEL_NAME` - Model identifier
- `DEFAULT_MODEL_PROVIDER` - Provider (e.g., "openai" for OpenRouter)
- `DEFAULT_MODEL_BASE_URL` - API endpoint

## How It Works

### 1. Initialization Flow

1. **[config.py](config.py)** loads environment variables and API keys
2. **[agent.py](agent.py)** initializes the model via `init_chat_model()`:
   - Uses OpenRouter as provider
   - Passes custom base URL and headers
   - Authenticates with OPENROUTER_API_KEY
3. **[utils/skill_loader.py](utils/skill_loader.py)** discovers available skills:
   - Scans `skills/` directory
   - Parses `prompt.md` files for skill metadata
   - Collects paths to `SKILL.md` files
   - Maps tool names to functions via `TOOL_REGISTRY`
4. **[prompts/root.md](prompts/root.md)** is loaded and populated with available skills list

### 2. Skill Definition

Each skill folder contains:
- **prompt.md** - YAML frontmatter with metadata:
  ```yaml
  ---
  name: Architect
  description: Designs technical architecture and system design
  tools:
    - generate_pdf
    - generate_docx
  ---
  System prompt content...
  ```
- **SKILL.md** - Detailed skill instructions and requirements

### 3. Request Handling

When a user makes a request:
1. Root agent analyzes the request
2. Breaks it into subtasks
3. Identifies the best-matching skill for each subtask
4. Loads the skill's detailed prompt from SKILL.md
5. Delegates to a subagent with skill-specific tools
6. Orchestrates execution and aggregates results

## Available Skills

Skills are dynamically loaded from the `skills/` directory. Current skills:
- **architect** - Technical architecture and system design
- **brd_formatter** - Business requirements document formatting
- **requirement_collector** - Requirements gathering and analysis
- **uiux_designer** - UI/UX design and specifications

## Available Tools

All subagents have access to output generation tools:
- `generate_pdf` - Create PDF documents
- `generate_docx` - Create Word documents
- `generate_csv` - Create CSV files
- `generate_image` - Generate images
- `generate_html` - Create HTML documents

## Dependencies

```python
deepagents>=0.2.6           # Deep agent framework
langchain>=0.3.0            # LLM integration
langchain-openai>=0.2.0     # OpenAI compatibility
langgraph-cli>=0.1.55       # Graph CLI tools
python-dotenv>=1.0.0        # Environment management
pyyaml>=6.0.0               # YAML parsing
fpdf2>=2.7.0                # PDF generation
python-docx>=1.0.0          # Word document generation
google-genai>=1.57.0        # Google AI support (optional)
```

## Installation

```bash
# Install dependencies
pip install -e .

# Or with uv:
uv pip install -e .
```

## Usage

```python
from agent import agent

# Use the agent to handle requests
response = agent.invoke({"input": "Your business analysis request here"})
print(response)
```

## Logging

The entire project includes comprehensive logging at DEBUG, INFO, and WARNING levels:
- **config.py** - Logs environment and model configuration
- **agent.py** - Logs model initialization, skill discovery, and agent creation
- **utils/skill_loader.py** - Logs skill discovery and loading
- **utils/skill_parser.py** - Logs markdown parsing operations
- **tools/__init__.py** - Logs tool registry initialization

Enable detailed logging by setting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Project Structure

### Root Prompt ([prompts/root.md](prompts/root.md))

The root prompt includes:
1. **Analyze Request** - Understand task and break into subtasks
2. **Load Skill Prompt** - Fetch SKILL.md from provided paths
3. **Delegate to Subagents** - Assign to best-matching skills
4. **Execute and Coordinate** - Orchestrate execution

### Configuration ([config.py](config.py))

- API keys management
- Model configuration
- Skills directory path

### Utilities

- **skill_loader.py** - Discovers and loads skills with metadata
- **skill_parser.py** - Parses YAML frontmatter from markdown files

### Tools ([tools/](tools/))

Output generation tools organized by format type.

## Development

### Adding a New Skill

1. Create a folder in `skills/` with skill name
2. Add `prompt.md` with YAML frontmatter:
   ```yaml
   ---
   name: Skill Name
   description: What this skill does
   tools:
     - tool_name1
     - tool_name2
   ---
   System prompt content...
   ```
3. Add `SKILL.md` with detailed instructions
4. Skill is automatically discovered on next run

### Adding a New Tool

1. Create `tools/my_tool.py` with a tool function
2. Register in `tools/__init__.py`:
   ```python
   from .my_tool import my_tool
   
   TOOL_REGISTRY = {
       ...
       "my_tool": my_tool,
   }
   ```

## Troubleshooting

### Model Initialization Fails
- Verify `OPENROUTER_API_KEY` is set in `.env`
- Check OpenRouter API status
- Ensure model name is correct in config

### Skills Not Found
- Verify `skills/` directory exists
- Check that skill folders contain `prompt.md`
- Review logs for parsing errors

### Tool Not Available
- Check tool is registered in `TOOL_REGISTRY`
- Verify tool name matches in skill's prompt.md
- Check tool function is properly implemented

## License

[Your License Here]

## Version

v0.2.0 - Skills Discovery Pattern with dynamic subagent creation
