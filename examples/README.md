# Examples

Example scripts demonstrating the multi-agent workflow system.

## Available Examples

### demo.py
Complete demonstration with 4 example scenarios:
1. **Story Generation** (Generic Agent) - Creative writing
2. **Fibonacci Calculation** (Coder Agent) - Mathematical computation
3. **AI Research** (Researcher Agent) - Web search and information gathering
4. **General Knowledge** (Generic Agent) - Straightforward Q&A

## Running Examples

```bash
# Run all demo scenarios
uv run examples/demo.py

# Or use Python directly
uv run python examples/demo.py
```

## Creating Custom Examples

```python
#!/usr/bin/env python3
from multiagent_system import MultiAgentWorkflow

def main():
    workflow = MultiAgentWorkflow()
    
    # Your custom query
    workflow.run_and_print("Your question here")

if __name__ == "__main__":
    main()
```

## More Information

- See [../docs/API_REFERENCE.md](../docs/API_REFERENCE.md) for complete API documentation
- See [../docs/QUICK_REFERENCE.md](../docs/QUICK_REFERENCE.md) for command examples
- See [../docs/TESTING_GUIDE.md](../docs/TESTING_GUIDE.md) for testing examples
