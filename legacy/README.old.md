# Multi-Agent Workflow System

A LangGraph-based multi-agent system with a supervisor pattern for handling various types of queries through specialized agents.

## Architecture

The system consists of the following components:

### Agents (`agents.py`)
- **SupervisorAgent**: Orchestrates the workflow by routing to appropriate specialists
- **EnhancerAgent**: Improves and clarifies user queries
- **ResearcherAgent**: Gathers information using web search (Tavily)
- **CoderAgent**: Handles technical implementation and calculations
- **GenericAgent**: Processes general questions that don't require specialized handling
- **ValidatorAgent**: Validates response quality and decides whether to continue or finish

### Workflow Orchestrator (`workflow.py`)
- **MultiAgentWorkflow**: Main class that initializes agents and manages the workflow graph

### Main Application (`main.py`)
- Entry point with example usage scenarios

## Setup

### Option 1: UV (Recommended - Fast & Modern)

**Why UV?**
- ⚡ **10-100x faster** than pip for dependency resolution and installation
- 🔒 **Reliable dependency locking** with uv.lock
- 🐍 **Python version management** built-in
- 📦 **Modern pyproject.toml** standard support
- 🚀 **Single binary** - no Python required for installation
- 🔄 **Automatic virtual environment** management

#### 1. Install UV
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.cargo/env
```

#### 2. Quick Setup
```bash
# Run the setup script
./setup.sh
```

#### 3. Configure Environment Variables
Edit the `.env` file created by setup:
```bash
# Required
OPENAI_API_KEY=your_actual_openai_api_key

# Optional (for enhanced functionality)  
TAVILY_API_KEY=your_actual_tavily_api_key
LANGSMITH_API_KEY=your_actual_langsmith_api_key
LANGFUSE_PUBLIC_KEY=your_actual_langfuse_public_key
LANGFUSE_SECRET_KEY=your_actual_langfuse_secret_key
```

#### 4. Run the Application
```bash
# Test the setup
uv run test_import.py

# Run the main application
uv run run.py

# Or use the script entry point
uv run workflow-demo
```

### Option 2: Traditional pip

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Configure Environment Variables  
Copy the `.env` file and fill in your API keys

#### 3. Run the Application
```bash
python main.py
```

## Usage

### UV Commands

#### Quick Task Runner
```bash
# Show all available tasks
uv run tasks.py help

# Initial setup (sync + test)
uv run tasks.py setup

# Test the installation
uv run tasks.py test

# Run the full demo
uv run tasks.py demo

# Add new dependencies
uv run tasks.py add requests

# Format code
uv run tasks.py format

# Lint code  
uv run tasks.py lint
```

#### Direct UV Commands
```bash
# Test the installation
uv run test_import.py

# Run the full demo
uv run run.py

# Run with script entry point
uv run workflow-demo

# Add new dependencies
uv add requests beautifulsoup4

# Install development dependencies
uv sync --group dev

# Run with specific Python version
uv run --python 3.11 run.py

# Sync dependencies
uv sync
```

### Basic Usage (Code)
```python
from workflow import MultiAgentWorkflow

# Initialize the workflow
workflow = MultiAgentWorkflow()

# Process a query
workflow.run_and_print("Tell me a short story")
```

### Advanced Usage with Custom Configuration
```python
from workflow import MultiAgentWorkflow

# Initialize with custom model
workflow = MultiAgentWorkflow(model_name="gpt-4")

# Run with custom configuration
config = {"callbacks": [your_callback_handler]}
for event in workflow.run("Calculate the 20th Fibonacci number", config):
    # Process events as needed
    pass
```

## Features

- **Supervisor Pattern**: Intelligent routing to appropriate specialist agents
- **Flexible Architecture**: Easy to extend with new agents
- **Environment Validation**: Automatic checking of required configurations
- **Multiple Examples**: Pre-built examples for different query types
- **Optional Integrations**: Support for LangSmith and LangFuse tracing

## Agent Workflow

1. **Supervisor** receives the user query
2. **Supervisor** routes to appropriate specialist:
   - **Enhancer** for query clarification
   - **Researcher** for information gathering
   - **Coder** for technical/mathematical tasks
   - **Generic** for simple general questions
3. Specialist processes the query
4. **Validator** checks the response quality
5. Either finish (if satisfactory) or route back to **Supervisor** for further processing

## Requirements

- Python 3.8+
- OpenAI API key (required)
- Tavily API key (optional, for web search)
- LangSmith credentials (optional, for tracing)
- LangFuse credentials (optional, for monitoring)

## Original vs Refactored

This is a refactored version of the original Google Colab notebook with the following improvements:

- ✅ Removed Google Colab dependencies
- ✅ Added proper class-based architecture
- ✅ Separated concerns into different modules
- ✅ Added environment variable management
- ✅ Added proper error handling
- ✅ Added comprehensive documentation
- ✅ Made the system easily extensible
