# Quick Reference Guide

> ⚡ Fast lookup for common tasks and commands

---

## 🚀 Installation (30 seconds)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # Install UV
echo "OPENAI_API_KEY=sk-..." > .env              # Set API key
uv sync                                           # Install deps
uv run run_multiagent.py                         # Run demo
```

---

## 💻 Basic Usage

### Single Query
```python
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print("Your question here")
```

### Different Model
```python
workflow = MultiAgentWorkflow(model_name="gpt-4o-mini")
```

### Stream Events
```python
for event in workflow.run("query"):
    if len(event) > 0:
        node, state = event
        print(f"{node}: {state}")
```

---

## 🧪 Testing Commands

```bash
# Test imports
uv run python -c "from multiagent_system import *; print('OK')"

# Run demo
uv run run_multiagent.py

# Run tests
uv run pytest

# With coverage
uv run pytest --cov
```

---

## 📦 Package Structure

```
multiagent_system/
├── __init__.py           # Main exports
├── workflow.py           # MultiAgentWorkflow
├── agents/
│   ├── base_agent.py     # BaseAgent (ABC)
│   ├── supervisor_agent.py
│   ├── enhancer_agent.py
│   ├── researcher_agent.py
│   ├── coder_agent.py
│   ├── generic_agent.py
│   └── validator_agent.py
└── models/
    └── decisions.py      # Pydantic models
```

---

## 🤖 Agent Quick Reference

| Agent | Purpose | Routes To |
|-------|---------|-----------|
| **supervisor** | Routes requests | enhancer/researcher/coder/generic |
| **enhancer** | Clarifies queries | supervisor |
| **researcher** | Web search | validator |
| **coder** | Code execution | validator |
| **generic** | General Q&A | validator |
| **validator** | Quality check | supervisor or END |

---

## 🔧 Common Tasks

### Add New Agent

```python
# 1. Create file: multiagent_system/agents/new_agent.py
from .base_agent import BaseAgent
from langgraph.types import Command

class NewAgent(BaseAgent):
    def process(self, state):
        # Your logic
        return Command(goto="validator", update={...})

# 2. Export in agents/__init__.py
from .new_agent import NewAgent
__all__ = [..., "NewAgent"]

# 3. Add to workflow.py
self.new_agent = NewAgent(self.llm)
builder.add_node("new_agent", self.new_agent.process)
```

### Environment Validation

```python
workflow = MultiAgentWorkflow()
errors = workflow.validate_environment()
if errors:
    for e in errors: print(e)
```

### Get Graph Image

```python
workflow = MultiAgentWorkflow()
image = workflow.get_graph_image()
with open("graph.png", "wb") as f:
    f.write(image)
```

---

## �� Troubleshooting

### API Key Not Found
```bash
cat .env                           # Check file exists
source .env                        # Reload
echo $OPENAI_API_KEY              # Verify loaded
```

### Import Errors
```bash
uv sync --no-editable             # Reinstall
uv run python -c "import multiagent_system"  # Test
```

### Module Not Found
```bash
uv add package-name               # Add dependency
uv sync                           # Install
```

---

## 📝 Environment Variables

### Required
```bash
OPENAI_API_KEY=sk-...
```

### Optional
```bash
TAVILY_API_KEY=tvly-...           # For researcher
LANGSMITH_API_KEY=...             # For tracing
LANGSMITH_TRACING=true
LANGFUSE_PUBLIC_KEY=...           # For monitoring
LANGFUSE_SECRET_KEY=...
```

---

## 🎯 Query Examples

```bash
# Research
uv run python -c "from multiagent_system import MultiAgentWorkflow; MultiAgentWorkflow().run_and_print('Latest AI trends')"

# Coding
uv run python -c "from multiagent_system import MultiAgentWorkflow; MultiAgentWorkflow().run_and_print('Calculate factorial 10')"

# General
uv run python -c "from multiagent_system import MultiAgentWorkflow; MultiAgentWorkflow().run_and_print('Capital of France?')"
```

---

## 🔍 UV Commands

```bash
uv sync                    # Install dependencies
uv add package            # Add package
uv remove package         # Remove package
uv run python script.py   # Run script
uv pip list              # List packages
uv tree                  # Show dep tree
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Quick start |
| `MODULAR_STRUCTURE.md` | Architecture |
| `API_REFERENCE.md` | Full API |
| `TESTING_GUIDE.md` | Testing |
| `COMPLETE_DOCUMENTATION.md` | Everything |
| `QUICK_REFERENCE.md` | This file |

---

## 🎨 Code Snippets

### Custom Config
```python
config = {
    "recursion_limit": 25,
    "configurable": {"thread_id": "user-123"}
}
workflow.run("query", config)
```

### Error Handling
```python
try:
    workflow = MultiAgentWorkflow()
    workflow.run_and_print("query")
except ValueError as e:
    print(f"Config error: {e}")
```

### Individual Agent
```python
from multiagent_system.agents import ResearcherAgent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
agent = ResearcherAgent(llm)
result = agent.process(state)
```

---

## ⚡ Performance Tips

1. Use `gpt-4o-mini` for faster responses
2. Set `recursion_limit` lower (e.g., 15)
3. Enable LangSmith caching
4. Use specific queries (avoid vague)
5. Limit Tavily results (default: 2)

---

## 🔒 Security Notes

⚠️ **PythonREPLTool** executes arbitrary code!

**Safe Usage**:
- Run in Docker/VM
- Monitor code execution
- Use sandboxed environment
- Implement rate limiting

---

## 📊 Model Options

```python
# Most capable (default)
MultiAgentWorkflow(model_name="gpt-4o")

# Fast & cheap
MultiAgentWorkflow(model_name="gpt-4o-mini")

# High performance
MultiAgentWorkflow(model_name="gpt-4-turbo")
```

---

## 🚀 Quick Deploy

### Docker
```dockerfile
FROM python:3.11-slim
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
WORKDIR /app
COPY . .
RUN uv sync
CMD ["uv", "run", "run_multiagent.py"]
```

### FastAPI
```python
from fastapi import FastAPI
from multiagent_system import MultiAgentWorkflow

app = FastAPI()
workflow = MultiAgentWorkflow()

@app.post("/query")
def query(text: str):
    return {"result": list(workflow.run(text))}
```

---

## 🎓 Learning Path

1. ✅ Run `run_multiagent.py`
2. ✅ Read `MODULAR_STRUCTURE.md`
3. ✅ Try custom queries
4. ✅ Read `base_agent.py`
5. ✅ Create custom agent
6. ✅ Write tests
7. ✅ Deploy to production

---

## 📞 Get Help

1. Check docs (start with `README.md`)
2. Review `COMPLETE_DOCUMENTATION.md`
3. Check troubleshooting section
4. Search issues
5. Create new issue

---

## ✨ Pro Tips

- Always validate environment first
- Use type hints for better IDE support
- Test after each change
- Keep agents focused and small
- Document custom agents
- Use meaningful variable names
- Log important decisions
- Monitor API usage

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Status**: Production Ready ✅

