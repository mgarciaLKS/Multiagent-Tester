# Multi-Agent Workflow System# Multi-Agent Workflow System



> A modular multi-agent system built with LangGraph, LangChain, and OpenAI GPT-4oA LangGraph-based multi-agent system with a supervisor pattern for handling various types of queries through specialized agents.



[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)## Architecture

[![UV](https://img.shields.io/badge/uv-fast%20package%20manager-green.svg)](https://docs.astral.sh/uv/)

[![LangGraph](https://img.shields.io/badge/LangGraph-0.6.10-orange.svg)](https://langchain-ai.github.io/langgraph/)The system consists of the following components:



## ✨ Features### Agents (`agents.py`)

- **SupervisorAgent**: Orchestrates the workflow by routing to appropriate specialists

- 🎯 **Intelligent Routing** - Supervisor agent directs queries to specialists- **EnhancerAgent**: Improves and clarifies user queries

- 🔍 **Query Enhancement** - Clarifies vague requests automatically- **ResearcherAgent**: Gathers information using web search (Tavily)

- 🌐 **Web Research** - Real-time information via Tavily search- **CoderAgent**: Handles technical implementation and calculations

- 💻 **Code Execution** - Safe Python code execution with PythonREPL- **GenericAgent**: Processes general questions that don't require specialized handling

- ✅ **Quality Validation** - Ensures responses meet quality standards- **ValidatorAgent**: Validates response quality and decides whether to continue or finish

- 📦 **Modular Design** - Clean separation, easy to extend

### Workflow Orchestrator (`workflow.py`)

## 🚀 Quick Start (30 seconds)- **MultiAgentWorkflow**: Main class that initializes agents and manages the workflow graph



```bash### Main Application (`main.py`)

# Install UV package manager- Entry point with example usage scenarios

curl -LsSf https://astral.sh/uv/install.sh | sh

## Setup

# Set up environment

echo "OPENAI_API_KEY=your_key_here" > .env### Option 1: UV (Recommended - Fast & Modern)



# Install dependencies**Why UV?**

uv sync- ⚡ **10-100x faster** than pip for dependency resolution and installation

- 🔒 **Reliable dependency locking** with uv.lock

# Run demo- 🐍 **Python version management** built-in

uv run examples/demo.py- 📦 **Modern pyproject.toml** standard support

```- 🚀 **Single binary** - no Python required for installation

- 🔄 **Automatic virtual environment** management

## 📦 Project Structure

#### 1. Install UV

``````bash

testing-multiagent/# Install UV (if not already installed)

├── multiagent_system/          # Main packagecurl -LsSf https://astral.sh/uv/install.sh | sh

│   ├── agents/                 # Agent implementationssource ~/.cargo/env

│   ├── models/                 # Pydantic models```

│   └── workflow.py             # Orchestrator

├── examples/                   # Usage examples#### 2. Quick Setup

│   └── demo.py                 # Demo with 4 scenarios```bash

├── docs/                       # 📚 Complete documentation# Run the setup script

│   ├── INDEX.md                # Documentation navigation./setup.sh

│   ├── QUICK_REFERENCE.md      # Command cheat sheet```

│   ├── API_REFERENCE.md        # Complete API docs

│   └── ...                     # 7 more guides#### 3. Configure Environment Variables

├── scripts/                    # Utility scriptsEdit the `.env` file created by setup:

├── legacy/                     # Old files (reference)```bash

├── .env                        # Environment variables# Required

└── pyproject.toml              # UV configurationOPENAI_API_KEY=your_actual_openai_api_key

```

# Optional (for enhanced functionality)  

## 💻 Basic UsageTAVILY_API_KEY=your_actual_tavily_api_key

LANGSMITH_API_KEY=your_actual_langsmith_api_key

```pythonLANGFUSE_PUBLIC_KEY=your_actual_langfuse_public_key

from multiagent_system import MultiAgentWorkflowLANGFUSE_SECRET_KEY=your_actual_langfuse_secret_key

```

# Initialize workflow

workflow = MultiAgentWorkflow()#### 4. Run the Application

```bash

# Run a query# Test the setup

workflow.run_and_print("What is quantum computing?")uv run test_import.py

```

# Run the main application

## 🤖 Available Agentsuv run run.py



| Agent | Purpose | Tools |# Or use the script entry point

|-------|---------|-------|uv run workflow-demo

| **Supervisor** | Routes to specialists | None |```

| **Enhancer** | Clarifies queries | None |

| **Researcher** | Web search | Tavily |### Option 2: Traditional pip

| **Coder** | Code execution | PythonREPL |

| **Generic** | General Q&A | None |#### 1. Install Dependencies

| **Validator** | Quality check | None |```bash

pip install -r requirements.txt

## 📚 Documentation```



All documentation is in the [`docs/`](docs/) folder:#### 2. Configure Environment Variables  

Copy the `.env` file and fill in your API keys

- **[INDEX.md](docs/INDEX.md)** - Start here! Master navigation guide

- **[QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)** - Command cheat sheet#### 3. Run the Application

- **[API_REFERENCE.md](docs/API_REFERENCE.md)** - Complete API documentation```bash

- **[MODULAR_STRUCTURE.md](docs/MODULAR_STRUCTURE.md)** - Architecture detailspython main.py

- **[TESTING_GUIDE.md](docs/TESTING_GUIDE.md)** - Testing strategies```

- **[COMPLETE_DOCUMENTATION.md](docs/COMPLETE_DOCUMENTATION.md)** - All-in-one reference

## Usage

**Total**: 11 comprehensive documents (~134 KB, ~70 pages)

### UV Commands

## 🔧 Environment Variables

#### Quick Task Runner

### Required```bash

```bash# Show all available tasks

OPENAI_API_KEY=sk-...              # OpenAI API keyuv run tasks.py help

```

# Initial setup (sync + test)

### Optionaluv run tasks.py setup

```bash

TAVILY_API_KEY=tvly-...            # For web search (researcher agent)# Test the installation

LANGSMITH_API_KEY=...              # For LangSmith tracinguv run tasks.py test

LANGSMITH_TRACING=true

LANGFUSE_PUBLIC_KEY=...            # For Langfuse monitoring# Run the full demo

LANGFUSE_SECRET_KEY=...uv run tasks.py demo

```

# Add new dependencies

## 🧪 Testinguv run tasks.py add requests



```bash# Format code

# Run demouv run tasks.py format

uv run examples/demo.py

# Lint code  

# Test importsuv run tasks.py lint

uv run python -c "from multiagent_system import *; print('✅ OK')"```



# Interactive mode#### Direct UV Commands

uv run python```bash

>>> from multiagent_system import MultiAgentWorkflow# Test the installation

>>> workflow = MultiAgentWorkflow()uv run test_import.py

>>> workflow.run_and_print("Your question")

```# Run the full demo

uv run run.py

## 🎯 Example Queries

# Run with script entry point

```bashuv run workflow-demo

# Research query (uses researcher agent)

uv run python -c "# Add new dependencies

from multiagent_system import MultiAgentWorkflowuv add requests beautifulsoup4

MultiAgentWorkflow().run_and_print('Latest AI trends 2024')

"# Install development dependencies

uv sync --group dev

# Coding query (uses coder agent)

uv run python -c "# Run with specific Python version

from multiagent_system import MultiAgentWorkflowuv run --python 3.11 run.py

MultiAgentWorkflow().run_and_print('Calculate Fibonacci 20')

"# Sync dependencies

uv sync

# General query (uses generic agent)```

uv run python -c "

from multiagent_system import MultiAgentWorkflow### Basic Usage (Code)

MultiAgentWorkflow().run_and_print('What is the capital of France?')```python

"from workflow import MultiAgentWorkflow

```

# Initialize the workflow

## 🛠️ Developmentworkflow = MultiAgentWorkflow()



### Add Custom Agent# Process a query

workflow.run_and_print("Tell me a short story")

```python```

# 1. Create agent file

from multiagent_system.agents import BaseAgent### Advanced Usage with Custom Configuration

```python

class CustomAgent(BaseAgent):from workflow import MultiAgentWorkflow

    def process(self, state):

        # Your logic here# Initialize with custom model

        passworkflow = MultiAgentWorkflow(model_name="gpt-4")



# 2. Add to workflow# Run with custom configuration

# See docs/MODULAR_STRUCTURE.md for detailsconfig = {"callbacks": [your_callback_handler]}

```for event in workflow.run("Calculate the 20th Fibonacci number", config):

    # Process events as needed

### Run Tests    pass

```

```bash

# Install test dependencies## Features

uv sync --extra test

- **Supervisor Pattern**: Intelligent routing to appropriate specialist agents

# Run tests- **Flexible Architecture**: Easy to extend with new agents

uv run pytest- **Environment Validation**: Automatic checking of required configurations

```- **Multiple Examples**: Pre-built examples for different query types

- **Optional Integrations**: Support for LangSmith and LangFuse tracing

## 📖 Learn More

## Agent Workflow

### For Beginners

1. Read [docs/INDEX.md](docs/INDEX.md) - Documentation navigation1. **Supervisor** receives the user query

2. Read [docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) - Commands2. **Supervisor** routes to appropriate specialist:

3. Run `uv run examples/demo.py` - Try it out   - **Enhancer** for query clarification

   - **Researcher** for information gathering

### For Developers   - **Coder** for technical/mathematical tasks

1. Read [docs/MODULAR_STRUCTURE.md](docs/MODULAR_STRUCTURE.md) - Architecture   - **Generic** for simple general questions

2. Read [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - API details3. Specialist processes the query

3. Read [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md) - Write tests4. **Validator** checks the response quality

5. Either finish (if satisfactory) or route back to **Supervisor** for further processing

### For Complete Understanding

- Read [docs/COMPLETE_DOCUMENTATION.md](docs/COMPLETE_DOCUMENTATION.md) - Everything!## Requirements



## 🔗 Resources- Python 3.8+

- OpenAI API key (required)

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)- Tavily API key (optional, for web search)

- [LangChain Documentation](https://python.langchain.com/)- LangSmith credentials (optional, for tracing)

- [UV Package Manager](https://docs.astral.sh/uv/)- LangFuse credentials (optional, for monitoring)

- [OpenAI API](https://platform.openai.com/docs)

## Original vs Refactored

## 📝 License

This is a refactored version of the original Google Colab notebook with the following improvements:

[Your License Here]

- ✅ Removed Google Colab dependencies

## 🙏 Acknowledgments- ✅ Added proper class-based architecture

- ✅ Separated concerns into different modules

Built with LangChain, LangGraph, OpenAI, Tavily, and UV.- ✅ Added environment variable management

- ✅ Added proper error handling

---- ✅ Added comprehensive documentation

- ✅ Made the system easily extensible

**Version**: 1.0.0 | **Status**: Production Ready ✅ | **Documentation**: [`docs/`](docs/)
