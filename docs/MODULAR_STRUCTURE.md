# Modular Structure Documentation

## Overview
The multi-agent workflow system has been refactored into a clean, modular package structure with each component in its own file. This follows Python best practices and makes the codebase highly maintainable, testable, and extensible.

## Directory Structure

```
multiagent_system/                    # Main package
├── __init__.py                       # Package initialization & exports
├── workflow.py                       # MultiAgentWorkflow orchestrator
├── agents/                           # Agents subpackage
│   ├── __init__.py                  # Agents exports
│   ├── base_agent.py                # BaseAgent abstract class
│   ├── supervisor_agent.py          # SupervisorAgent
│   ├── enhancer_agent.py            # EnhancerAgent
│   ├── researcher_agent.py          # ResearcherAgent
│   ├── coder_agent.py               # CoderAgent
│   ├── generic_agent.py             # GenericAgent
│   └── validator_agent.py           # ValidatorAgent
└── models/                           # Models subpackage
    ├── __init__.py                  # Models exports
    └── decisions.py                 # Pydantic decision models

run_multiagent.py                     # Main entry point
```

## File Descriptions

### Core Package Files

#### `multiagent_system/__init__.py`
**Purpose**: Package initialization and central import location

**Exports**:
- `MultiAgentWorkflow` - Main orchestrator
- All agent classes
- All decision models

**Features**:
- Loads environment variables automatically
- Provides version information
- Single import point for entire system

**Usage**:
```python
from multiagent_system import MultiAgentWorkflow
```

#### `multiagent_system/workflow.py`
**Purpose**: Main orchestrator class

**Class**: `MultiAgentWorkflow`

**Responsibilities**:
- Initialize all agents
- Build LangGraph workflow
- Manage graph compilation
- Provide high-level execution interface

**Key Methods**:
- `__init__(model_name)` - Initialize with model
- `_build_graph()` - Build workflow graph
- `run(user_input, config)` - Execute workflow
- `run_and_print(user_input, config)` - Execute with formatted output
- `get_graph_image()` - Visualize workflow
- `validate_environment()` - Check environment vars

### Agents Subpackage

#### `multiagent_system/agents/__init__.py`
**Purpose**: Export all agent classes

**Exports**:
- `BaseAgent`
- `SupervisorAgent`
- `EnhancerAgent`
- `ResearcherAgent`
- `CoderAgent`
- `GenericAgent`
- `ValidatorAgent`

#### `multiagent_system/agents/base_agent.py`
**Purpose**: Abstract base class for all agents

**Class**: `BaseAgent` (ABC)

**Features**:
- Enforces consistent interface
- Provides LLM storage
- Defines abstract `process()` method

**Key Methods**:
- `__init__(llm)` - Store language model
- `process(state)` - Abstract method (must be implemented)

#### `multiagent_system/agents/supervisor_agent.py`
**Purpose**: Orchestrate workflow routing

**Class**: `SupervisorAgent`

**Responsibilities**:
- Analyze requests and responses
- Route to appropriate specialist
- Provide routing rationale
- Maintain workflow momentum

**Routing Options**:
- `enhancer` - Query clarification
- `researcher` - Information gathering
- `coder` - Technical implementation
- `generic` - General questions

#### `multiagent_system/agents/enhancer_agent.py`
**Purpose**: Improve and clarify user queries

**Class**: `EnhancerAgent`

**Responsibilities**:
- Query refinement
- Ambiguity resolution
- Context expansion
- Clarity improvement

**Routes to**: `supervisor`

#### `multiagent_system/agents/researcher_agent.py`
**Purpose**: Gather information using web search

**Class**: `ResearcherAgent`

**Responsibilities**:
- Web search execution (Tavily)
- Information gathering
- Source citation
- Data organization

**Tools**:
- `TavilySearchResults` (max 2 results)
- React agent for autonomous research

**Routes to**: `validator`

#### `multiagent_system/agents/coder_agent.py`
**Purpose**: Handle technical implementation and calculations

**Class**: `CoderAgent`

**Responsibilities**:
- Code execution
- Mathematical calculations
- Technical problem-solving
- Data analysis

**Tools**:
- `PythonREPLTool` for code execution
- React agent for autonomous coding

**Routes to**: `validator`

#### `multiagent_system/agents/generic_agent.py`
**Purpose**: Handle general questions

**Class**: `GenericAgent`

**Responsibilities**:
- General knowledge questions
- Direct Q&A
- Simple queries without tools

**Routes to**: `validator`

#### `multiagent_system/agents/validator_agent.py`
**Purpose**: Validate response quality

**Class**: `ValidatorAgent`

**Responsibilities**:
- Quality assurance
- Response validation
- Workflow termination decisions
- Loop prevention

**Routes to**: `supervisor` (retry) or `__end__` (finish)

### Models Subpackage

#### `multiagent_system/models/__init__.py`
**Purpose**: Export decision models

**Exports**:
- `SupervisorDecision`
- `ValidatorDecision`

#### `multiagent_system/models/decisions.py`
**Purpose**: Pydantic models for structured outputs

**Models**:
1. `SupervisorDecision`
   - `next`: Literal["enhancer", "researcher", "coder", "generic"]
   - `reason`: str

2. `ValidatorDecision`
   - `next`: Literal["supervisor", "FINISH"]
   - `reason`: str

### Entry Point

#### `run_multiagent.py`
**Purpose**: Main entry point with examples

**Features**:
- Demonstrates all agent types
- Shows different query categories
- Formatted output
- Easy to customize

## Import Patterns

### Simple Usage
```python
from multiagent_system import MultiAgentWorkflow

workflow = MultiAgentWorkflow()
workflow.run_and_print("Your query here")
```

### Importing Individual Agents
```python
from multiagent_system.agents import SupervisorAgent, EnhancerAgent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-5")
supervisor = SupervisorAgent(llm)
```

### Importing Models
```python
from multiagent_system.models import SupervisorDecision, ValidatorDecision
```

### Complete Import
```python
from multiagent_system import (
    MultiAgentWorkflow,
    BaseAgent,
    SupervisorAgent,
    EnhancerAgent,
    ResearcherAgent,
    CoderAgent,
    GenericAgent,
    ValidatorAgent,
    SupervisorDecision,
    ValidatorDecision,
)
```

## Benefits of Modular Structure

### 1. **Separation of Concerns**
- Each file has a single, clear purpose
- Changes to one agent don't affect others
- Easy to locate specific functionality

### 2. **Maintainability**
- Small, focused files are easier to understand
- Changes are localized and predictable
- Reduces cognitive load for developers

### 3. **Testability**
- Each module can be tested independently
- Mock dependencies easily
- Unit tests are straightforward

### 4. **Reusability**
- Import only what you need
- Use agents in different contexts
- Create custom workflows with subset of agents

### 5. **Collaboration**
- Multiple developers can work on different files
- Reduced merge conflicts
- Clear ownership of components

### 6. **IDE Support**
- Better autocomplete and intellisense
- Easier navigation between files
- Clearer import suggestions

### 7. **Type Checking**
- Mypy and other type checkers work better
- Import cycles are easier to detect
- Type hints are more effective

## Usage Examples

### Basic Usage
```python
from multiagent_system import MultiAgentWorkflow

# Initialize
workflow = MultiAgentWorkflow()

# Run a query
workflow.run_and_print("Tell me a short story")
```

### Custom Model
```python
from multiagent_system import MultiAgentWorkflow

# Use a different model
workflow = MultiAgentWorkflow(model_name="gpt-4-turbo")
workflow.run_and_print("Explain quantum computing")
```

### Using Individual Agents
```python
from multiagent_system.agents import ResearcherAgent
from langchain_openai import ChatOpenAI

# Create and use a single agent
llm = ChatOpenAI(model="gpt-5")
researcher = ResearcherAgent(llm)

# Use in custom workflow
result = researcher.process(state)
```

### With Configuration
```python
from multiagent_system import MultiAgentWorkflow

workflow = MultiAgentWorkflow()

# Custom configuration
config = {
    "callbacks": [my_callback],
    "recursion_limit": 25
}

for event in workflow.run("Calculate Fibonacci 30", config):
    # Process events
    pass
```

## Running the System

### Using UV (Recommended)
```bash
# Run the main demo
uv run run_multiagent.py

# Or using Python directly
uv run python run_multiagent.py
```

### Traditional Python
```bash
# Ensure dependencies are installed
python run_multiagent.py
```

### As a Module
```bash
# Run as a module
python -m multiagent_system
```

## Extending the System

### Adding a New Agent

1. **Create new agent file**:
```python
# multiagent_system/agents/new_agent.py
from typing import Literal
from .base_agent import BaseAgent

class NewAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm)
        self.system_prompt = "..."
    
    def process(self, state):
        # Implementation
        pass
```

2. **Export from agents/__init__.py**:
```python
from .new_agent import NewAgent

__all__ = [
    # ... existing agents
    "NewAgent",
]
```

3. **Use in workflow**:
```python
# multiagent_system/workflow.py
self.new_agent = NewAgent(self.llm)
graph.add_node("new_agent", self.new_agent.process)
```

### Adding a New Decision Model

1. **Add to models/decisions.py**:
```python
class NewDecision(BaseModel):
    next: Literal["option1", "option2"]
    reason: str
```

2. **Export from models/__init__.py**:
```python
from .decisions import NewDecision

__all__ = [
    # ... existing models
    "NewDecision",
]
```

## Testing Strategy

### Unit Tests
```python
# tests/test_agents.py
from multiagent_system.agents import SupervisorAgent
from langchain_openai import ChatOpenAI

def test_supervisor_routing():
    llm = ChatOpenAI(model="gpt-5")
    supervisor = SupervisorAgent(llm)
    # Test logic
```

### Integration Tests
```python
# tests/test_workflow.py
from multiagent_system import MultiAgentWorkflow

def test_full_workflow():
    workflow = MultiAgentWorkflow()
    events = list(workflow.run("test query"))
    assert len(events) > 0
```

## Best Practices

1. **Always import from package root**:
   ```python
   from multiagent_system import MultiAgentWorkflow  # ✅ Good
   from multiagent_system.workflow import MultiAgentWorkflow  # ❌ Avoid
   ```

2. **Use relative imports within package**:
   ```python
   # Inside package
   from .base_agent import BaseAgent  # ✅ Good
   from multiagent_system.agents.base_agent import BaseAgent  # ❌ Avoid
   ```

3. **Keep files focused and small**:
   - One class per file (except models)
   - Clear, descriptive filenames
   - Single responsibility

4. **Document each module**:
   - Module-level docstring
   - Class docstrings
   - Method docstrings

5. **Export explicitly**:
   - Use `__all__` in `__init__.py`
   - Makes public API clear
   - Prevents accidental imports

## Migration from Monolithic File

### Old Way
```python
from langgraph_07_supervisor_multiagent_workflow import MultiAgentWorkflow
```

### New Way
```python
from multiagent_system import MultiAgentWorkflow
```

**Note**: Both files coexist, so you can migrate gradually!

## Conclusion

The modular structure provides a professional, maintainable foundation for the multi-agent system. Each component is isolated, testable, and reusable, following Python best practices and industry standards.
