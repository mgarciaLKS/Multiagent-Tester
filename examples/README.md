# 🎮 Examples# Examples



> Demonstrations of the parallel multi-agent testing systemExample scripts demonstrating the multi-agent workflow system.



---## Available Examples



## 📁 Available Examples### demo.py

Complete demonstration with 4 example scenarios:

### `demo.py` - Complete Test Generation Demo1. **Story Generation** (Generic Agent) - Creative writing

2. **Fibonacci Calculation** (Coder Agent) - Mathematical computation

The main demonstration showing how to generate comprehensive tests for a real project using parallel execution.3. **AI Research** (Researcher Agent) - Web search and information gathering

4. **General Knowledge** (Generic Agent) - Straightforward Q&A

**What it does**:

- Analyzes a Python project## Running Examples

- Runs Unit, Functional, and Integration testers in parallel

- Generates complete test suite```bash

- Validates test quality# Run all demo scenarios

uv run examples/demo.py

**Run it**:

```bash# Or use Python directly

uv run python examples/demo.pyuv run python examples/demo.py

``````



**Time**: ~2 minutes  ## Creating Custom Examples

**Output**: Complete test suite with all test types

```python

---#!/usr/bin/env python3

from multiagent_system import MultiAgentWorkflow

## 🎯 Quick Start

def main():

```bash    workflow = MultiAgentWorkflow()

# Run the main demo    

uv run python examples/demo.py    # Your custom query

```    workflow.run_and_print("Your question here")



This will generate tests for the WhatsApp MCP project, demonstrating:if __name__ == "__main__":

- ⚡ Parallel execution of all 3 testing agents    main()

- 📝 Unit test generation with mocking```

- 🔗 Integration test creation for APIs

- 🎭 Functional test development for workflows## More Information

- ✅ Quality validation and coverage checks

- See [../docs/API_REFERENCE.md](../docs/API_REFERENCE.md) for complete API documentation

---- See [../docs/QUICK_REFERENCE.md](../docs/QUICK_REFERENCE.md) for command examples

- See [../docs/TESTING_GUIDE.md](../docs/TESTING_GUIDE.md) for testing examples

## 💡 Use in Your Code

```python
from multiagent_system import MultiAgentWorkflow

# Initialize
workflow = MultiAgentWorkflow()

# Generate tests for your project
results = workflow.run_parallel_sync("""
    Generate comprehensive tests for /path/to/project
    
    Requirements:
    - pytest framework
    - 70%+ coverage
    - Mock external dependencies
""")

# Show results
workflow.print_results(results)
```

---

## 📊 What to Expect

When you run `demo.py`, you'll see:

```
🔀 PARALLEL EXECUTION MODE
================================================================================

Phase 1: Supervisor Analysis
✅ Analyzes project structure

Phase 2: Parallel Test Generation
🚀 Starting UnitTester...
🚀 Starting FunctionalTester...
🚀 Starting IntegrationTester...

✅ All agents complete simultaneously (2-3x faster!)

Phase 3: Results Summary
✅ Successful: 3
❌ Failed: 0

Phase 4: Validation
✅ Tests meet quality standards
```

---

## 🎓 Learning Path

1. **Run the demo**: See it in action
2. **Read the output**: Understand what each agent does
3. **Modify the request**: Try your own project
4. **Check generated tests**: See the quality
5. **Customize agents**: Adapt to your needs

---

**Back to main README**: [../README.md](../README.md)
