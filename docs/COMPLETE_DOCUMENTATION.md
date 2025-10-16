# Complete Documentation - Multi-Agent Workflow System

## 📚 Documentation Index

This document serves as the master reference for the entire multi-agent system. For detailed information on specific topics, refer to the specialized documents:

| Document | Description |
|----------|-------------|
| **README.md** | Quick start guide and project overview |
| **MODULAR_STRUCTURE.md** | Detailed package structure and architecture |
| **API_REFERENCE.md** | Complete API documentation for all classes |
| **TESTING_GUIDE.md** | Comprehensive testing strategies and examples |
| **REFACTORING_SUMMARY.md** | Migration guide from monolithic to modular |
| **ARCHITECTURE_DIAGRAM.txt** | Visual workflow diagram |
| **CODE_COMPARISON.md** | Before/after code comparison |

---

## 🎯 Quick Navigation

### For New Users
1. Start with **README.md** - Installation and first steps
2. Read **MODULAR_STRUCTURE.md** - Understand the architecture
3. Try examples in **run_multiagent.py**

### For Developers
1. **API_REFERENCE.md** - All classes and methods
2. **MODULAR_STRUCTURE.md** - Package structure
3. **TESTING_GUIDE.md** - Write and run tests

### For Contributors
1. **REFACTORING_SUMMARY.md** - Design decisions
2. **TESTING_GUIDE.md** - Test requirements
3. **ARCHITECTURE_DIAGRAM.txt** - System design

---

## 🚀 System Overview

### What Is This?

A **modular multi-agent workflow system** built with:
- **LangGraph**: Workflow orchestration
- **LangChain**: LLM integration
- **OpenAI**: GPT-4o language model
- **UV**: Fast Python package management

### Key Features

✅ **Intelligent Routing**: Supervisor agent directs queries to specialists  
✅ **Query Enhancement**: Clarifies vague requests automatically  
✅ **Web Research**: Real-time information gathering via Tavily  
✅ **Code Execution**: Run Python code safely with PythonREPL  
✅ **Quality Validation**: Ensures responses meet quality standards  
✅ **Modular Design**: Clean separation, easy to extend  
✅ **Type Safety**: Pydantic models for structured outputs  

### Architecture

```
User Query
    ↓
Supervisor Agent (routing)
    ↓
┌───────────┬──────────────┬───────────┬─────────┐
│ Enhancer  │  Researcher  │   Coder   │ Generic │
│ (clarify) │  (search)    │  (code)   │  (Q&A)  │
└───────────┴──────────────┴───────────┴─────────┘
    ↓
Validator Agent (quality check)
    ↓
Final Response or Loop Back
```

---

## 📦 Package Structure

```
multiagent_system/
├── __init__.py                          # Package exports
├── workflow.py                          # MultiAgentWorkflow orchestrator
├── agents/
│   ├── __init__.py                     # Agent exports
│   ├── base_agent.py                   # BaseAgent (ABC)
│   ├── supervisor_agent.py             # Routing logic
│   ├── enhancer_agent.py               # Query clarification
│   ├── researcher_agent.py             # Web search
│   ├── coder_agent.py                  # Code execution
│   ├── generic_agent.py                # General Q&A
│   └── validator_agent.py              # Quality control
└── models/
    ├── __init__.py                     # Model exports
    └── decisions.py                    # Pydantic models

run_multiagent.py                        # Main entry point
pyproject.toml                           # UV configuration
.env                                     # Environment variables
```

---

## 🔧 Installation

### Prerequisites
- Python 3.9+
- OpenAI API key
- (Optional) Tavily API key for research

### Quick Setup

```bash
# 1. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone/navigate to project
cd testing-multiagent

# 3. Create .env file
cat > .env << 'ENV'
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here  # Optional
ENV

# 4. Install dependencies
uv sync

# 5. Run demo
uv run run_multiagent.py
```

---

## 💻 Usage Examples

### Basic Usage

```python
from multiagent_system import MultiAgentWorkflow

workflow = MultiAgentWorkflow()
workflow.run_and_print("What is quantum computing?")
```

### Different Models

```python
# Use GPT-4o mini (faster, cheaper)
workflow = MultiAgentWorkflow(model_name="gpt-4o-mini")
workflow.run_and_print("Tell me a joke")
```

### Streaming Events

```python
workflow = MultiAgentWorkflow()

for event in workflow.run("Calculate factorial of 10"):
    if len(event) > 0:
        node, state = event
        print(f"Agent: {node}")
```

### Agent-Specific Queries

```bash
# Research query (uses researcher agent)
uv run python -c "
from multiagent_system import MultiAgentWorkflow
MultiAgentWorkflow().run_and_print('Latest AI trends 2024')
"

# Coding query (uses coder agent)
uv run python -c "
from multiagent_system import MultiAgentWorkflow
MultiAgentWorkflow().run_and_print('Calculate Fibonacci 20')
"

# Vague query (uses enhancer agent)
uv run python -c "
from multiagent_system import MultiAgentWorkflow
MultiAgentWorkflow().run_and_print('Tell me about that thing')
"
```

---

## 🧪 Testing

### Run All Tests

```bash
# Install test dependencies
uv sync --extra test

# Run pytest
uv run pytest

# With coverage
uv run pytest --cov=multiagent_system
```

### Quick Validation

```bash
# Test imports
uv run python -c "from multiagent_system import *; print('✅ All imports OK')"

# Test basic workflow
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
list(workflow.run('test'))
print('✅ Workflow OK')
"
```

### Manual Testing

```python
# Save as test_interactive.py
from multiagent_system import MultiAgentWorkflow

workflow = MultiAgentWorkflow()
while True:
    query = input("You: ")
    if query.lower() in ['quit', 'exit']:
        break
    workflow.run_and_print(query)
```

---

## 🏗️ Architecture Details

### Agent Hierarchy

```
BaseAgent (ABC)
    │
    ├── SupervisorAgent     → Routes to specialists
    ├── EnhancerAgent       → Clarifies queries
    ├── ResearcherAgent     → Web search (Tavily)
    ├── CoderAgent          → Code execution (PythonREPL)
    ├── GenericAgent        → Direct Q&A
    └── ValidatorAgent      → Quality assurance
```

### Workflow Flow

1. **User Input** → `supervisor`
2. **Supervisor** → Routes to specialist:
   - Vague query → `enhancer` → back to `supervisor`
   - Research needed → `researcher` → `validator`
   - Code/math → `coder` → `validator`
   - General Q&A → `generic` → `validator`
3. **Validator** → Decides:
   - Good response → `__end__` (finish)
   - Needs improvement → back to `supervisor`

### Decision Models

```python
# Supervisor routing
class SupervisorDecision(BaseModel):
    next: Literal["enhancer", "researcher", "coder", "generic"]
    reason: str

# Validator continuation
class ValidatorDecision(BaseModel):
    next: Literal["supervisor", "FINISH"]
    reason: str
```

---

## 🔌 API Quick Reference

### MultiAgentWorkflow

```python
workflow = MultiAgentWorkflow(model_name="gpt-4o")

# Run workflow
workflow.run(user_input: str, config: dict = None) -> Generator

# Run with formatted output
workflow.run_and_print(user_input: str, config: dict = None) -> None

# Get graph visualization
workflow.get_graph_image() -> bytes

# Validate environment
workflow.validate_environment() -> List[str]
```

### BaseAgent

```python
class YourAgent(BaseAgent):
    def __init__(self, llm: ChatOpenAI):
        super().__init__(llm)
    
    def process(self, state: MessagesState) -> Command | dict:
        # Implementation
        pass
```

### Individual Agent Usage

```python
from multiagent_system.agents import ResearcherAgent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
researcher = ResearcherAgent(llm)

state = {'messages': [HumanMessage(content="Query")]}
result = researcher.process(state)
```

---

## 🎨 Customization

### Add a New Agent

1. **Create agent file**:
```python
# multiagent_system/agents/translator_agent.py
from .base_agent import BaseAgent
from langgraph.types import Command

class TranslatorAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm)
        self.system_prompt = "You are a translation expert..."
    
    def process(self, state):
        # Translation logic
        result = self.llm.invoke(...)
        return Command(goto="validator", update={"messages": [result]})
```

2. **Export from `agents/__init__.py`**:
```python
from .translator_agent import TranslatorAgent
__all__ = [..., "TranslatorAgent"]
```

3. **Add to workflow**:
```python
# In workflow.py __init__
self.translator = TranslatorAgent(self.llm)

# In _build_graph
builder.add_node("translator", self.translator.process)

# Update supervisor to route to translator
```

### Custom Workflow

```python
from multiagent_system.agents import SupervisorAgent, GenericAgent
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START

llm = ChatOpenAI(model="gpt-4o")
builder = StateGraph(MessagesState)

# Add only agents you need
builder.add_node("supervisor", SupervisorAgent(llm).process)
builder.add_node("generic", GenericAgent(llm).process)

builder.add_edge(START, "supervisor")
# ... define routing logic

graph = builder.compile()
```

---

## 🐛 Troubleshooting

### Common Issues

#### API Key Errors
```bash
# Check environment
cat .env
uv run python -c "import os; print(os.getenv('OPENAI_API_KEY'))"

# Reload environment
source .env  # or restart terminal
```

#### Import Errors
```bash
# Reinstall
uv sync --no-editable

# Verify installation
uv run python -c "import multiagent_system; print('OK')"
```

#### Model Not Found
```python
# Use valid model name
workflow = MultiAgentWorkflow(model_name="gpt-4o")  # ✅
# Not: workflow = MultiAgentWorkflow(model_name="gpt5")  # ❌
```

#### Tavily Search Fails
```bash
# Set API key in .env
TAVILY_API_KEY=your_tavily_key

# Or disable researcher
# (Don't route to researcher in supervisor)
```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print("debug query")
```

---

## 📊 Performance Tips

1. **Use GPT-4o-mini** for faster responses
2. **Limit recursion** with config:
   ```python
   config = {"recursion_limit": 15}
   workflow.run(query, config)
   ```
3. **Cache LLM responses** (LangChain feature)
4. **Use async** for parallel processing (future enhancement)
5. **Monitor with LangSmith** (set env vars)

---

## 🔒 Security Considerations

### PythonREPLTool Warning

The `CoderAgent` uses `PythonREPLTool` which executes arbitrary Python code. 

**Risks:**
- File system access
- Network requests
- System commands

**Mitigations:**
- Run in isolated environment (Docker/VM)
- Limit agent's system prompt
- Monitor executed code
- Use sandboxed execution environment

**Production Alternative:**
```python
# Use safer alternatives:
# - E2B sandbox
# - RestrictedPython
# - Custom code validator
```

---

## 🚢 Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app
COPY . .

RUN uv sync

CMD ["uv", "run", "run_multiagent.py"]
```

### Environment Variables
```bash
# In production, use secrets management
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY myapp
```

### API Server (FastAPI)

```python
# api_server.py
from fastapi import FastAPI
from multiagent_system import MultiAgentWorkflow

app = FastAPI()
workflow = MultiAgentWorkflow()

@app.post("/query")
async def query(text: str):
    events = list(workflow.run(text))
    return {"result": events[-1]}
```

---

## 📈 Monitoring

### LangSmith Integration

```bash
# .env
LANGSMITH_API_KEY=your_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=my-project
```

### Langfuse Integration

```bash
# .env
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

### Custom Logging

```python
from multiagent_system import MultiAgentWorkflow
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('workflow.log'),
        logging.StreamHandler()
    ]
)

workflow = MultiAgentWorkflow()
```

---

## 🤝 Contributing

### Development Setup

```bash
# Install with dev dependencies
uv sync --extra test --extra dev

# Install pre-commit hooks
pre-commit install

# Run tests before committing
uv run pytest
```

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to public methods
- Keep functions small and focused
- Write tests for new features

### Pull Request Process

1. Fork the repository
2. Create feature branch
3. Write tests
4. Update documentation
5. Submit PR with clear description

---

## 📝 License

[Your License Here]

---

## 🔗 Resources

### Official Documentation
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [LangChain](https://python.langchain.com/)
- [OpenAI API](https://platform.openai.com/docs)
- [UV Package Manager](https://docs.astral.sh/uv/)

### Related Projects
- [LangGraph Examples](https://github.com/langchain-ai/langgraph/tree/main/examples)
- [LangChain Templates](https://github.com/langchain-ai/langchain/tree/master/templates)

### Community
- LangChain Discord
- GitHub Discussions
- Stack Overflow (`langchain`, `langgraph` tags)

---

## 📞 Support

For questions or issues:

1. Check documentation (this file and linked docs)
2. Review troubleshooting section
3. Search existing issues
4. Create new issue with:
   - Environment details
   - Error messages
   - Minimal reproduction example

---

## 🎓 Learning Path

### Beginner
1. ✅ Install and run demo (`run_multiagent.py`)
2. ✅ Understand package structure (`MODULAR_STRUCTURE.md`)
3. ✅ Try different queries (research, coding, general)
4. ✅ Read agent code (start with `GenericAgent`)

### Intermediate
1. ✅ Study workflow graph construction (`workflow.py`)
2. ✅ Create custom agent
3. ✅ Write unit tests (`TESTING_GUIDE.md`)
4. ✅ Experiment with different models

### Advanced
1. ✅ Optimize for production
2. ✅ Add async support
3. ✅ Implement custom tools
4. ✅ Build API service
5. ✅ Deploy with monitoring

---

## 🎯 Next Steps

### For Users
- [ ] Set up environment variables
- [ ] Run demo examples
- [ ] Try your own queries
- [ ] Explore different agents

### For Developers
- [ ] Read API reference
- [ ] Run test suite
- [ ] Create custom agent
- [ ] Add new features

### For Contributors
- [ ] Review architecture
- [ ] Set up dev environment
- [ ] Write tests
- [ ] Submit PR

---

## 📄 Document Changelog

### v1.0.0 (Current)
- Initial modular architecture
- Complete documentation suite
- Full test coverage examples
- Production-ready codebase

---

## 🙏 Acknowledgments

Built with:
- **LangChain/LangGraph** - Workflow framework
- **OpenAI** - Language models
- **Tavily** - Web search
- **UV** - Package management
- **Python community** - Countless tools and libraries

---

## 📌 Quick Command Reference

```bash
# Setup
uv sync                          # Install dependencies
uv sync --extra test            # Install with test deps

# Running
uv run run_multiagent.py        # Run demo
uv run python your_script.py    # Run custom script

# Testing
uv run pytest                   # Run all tests
uv run pytest -v               # Verbose output
uv run pytest --cov            # With coverage

# Development
uv add package_name            # Add dependency
uv remove package_name         # Remove dependency
uv pip list                    # List installed packages
```

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Status**: Production Ready ✅
