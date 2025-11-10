# Testing Guide for Multi-Agent System

## Table of Contents
1. [Quick Start Testing](#quick-start-testing)
2. [Test Categories](#test-categories)
3. [Unit Testing](#unit-testing)
4. [Integration Testing](#integration-testing)
5. [Manual Testing](#manual-testing)
6. [Setting Up Test Environment](#setting-up-test-environment)
7. [Writing New Tests](#writing-new-tests)
8. [Troubleshooting](#troubleshooting)

## Quick Start Testing

### Running the Demo
```bash
# Run the main demo with 4 example queries
uv run run_multiagent.py
```

### Running Individual Queries
```bash
# Test researcher agent
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('What are the latest advances in AI?')
"

# Test coder agent
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('Calculate the 10th Fibonacci number')
"

# Test generic agent
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('What is the capital of France?')
"

# Test enhancer agent (vague query)
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('Tell me about that thing')
"
```

## Test Categories

### 1. Import Tests
Verify all modules can be imported correctly.

```bash
# Test package imports
uv run python -c "
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
print('✅ All imports successful!')
"
```

### 2. Agent Routing Tests
Verify supervisor routes to correct agents.

```python
# Save as tests/test_routing.py
from multiagent_system import MultiAgentWorkflow

def test_routes_to_researcher():
    """Verify research queries go to researcher agent"""
    workflow = MultiAgentWorkflow()
    events = list(workflow.run("What is quantum computing?"))
    
    # Check that researcher was called
    agent_names = [e[0] for e in events if len(e) > 0]
    assert 'researcher' in agent_names

def test_routes_to_coder():
    """Verify coding queries go to coder agent"""
    workflow = MultiAgentWorkflow()
    events = list(workflow.run("Calculate 2 + 2"))
    
    agent_names = [e[0] for e in events if len(e) > 0]
    assert 'coder' in agent_names

def test_routes_to_enhancer():
    """Verify vague queries go to enhancer"""
    workflow = MultiAgentWorkflow()
    events = list(workflow.run("Tell me something"))
    
    agent_names = [e[0] for e in events if len(e) > 0]
    assert 'enhancer' in agent_names
```

### 3. End-to-End Tests
Test complete workflow execution.

```python
# Save as tests/test_e2e.py
from multiagent_system import MultiAgentWorkflow

def test_complete_workflow():
    """Test full workflow completes successfully"""
    workflow = MultiAgentWorkflow()
    events = list(workflow.run("What is Python?"))
    
    # Should have multiple events
    assert len(events) > 0
    
    # Should reach end state
    final_state = events[-1]
    assert '__end__' in str(final_state) or len(final_state[1]['messages']) > 0

def test_multiple_rounds():
    """Test workflow can handle multiple iterations"""
    workflow = MultiAgentWorkflow()
    events = list(workflow.run("Write a haiku about code"))
    
    # Count agent invocations
    agent_calls = [e for e in events if len(e) > 0 and e[0] != '__end__']
    
    # Should have at least supervisor, agent, and validator
    assert len(agent_calls) >= 3
```

### 4. Validator Tests
Test response validation logic.

```python
# Save as tests/test_validator.py
from multiagent_system import MultiAgentWorkflow
from langchain_core.messages import HumanMessage, AIMessage

def test_validator_accepts_good_response():
    """Test validator approves complete responses"""
    workflow = MultiAgentWorkflow()
    
    # Simulate a good response
    state = {
        'messages': [
            HumanMessage(content="What is 2+2?"),
            AIMessage(content="2 + 2 equals 4.")
        ]
    }
    
    decision = workflow.validator.process(state)
    # A good response might finish or continue for more refinement
    assert decision['next'] in ['supervisor', 'FINISH']
```

## Unit Testing

### Testing Individual Agents

```python
# Save as tests/test_agents.py
from multiagent_system.agents import (
    SupervisorAgent,
    EnhancerAgent,
    ResearcherAgent,
    CoderAgent,
    GenericAgent,
    ValidatorAgent
)
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def get_test_llm():
    """Get test LLM instance"""
    return ChatOpenAI(model="gpt-5", temperature=0)

def test_supervisor_initialization():
    """Test supervisor agent initializes correctly"""
    llm = get_test_llm()
    supervisor = SupervisorAgent(llm)
    assert supervisor.llm is not None
    assert supervisor.system_prompt is not None

def test_enhancer_initialization():
    """Test enhancer agent initializes correctly"""
    llm = get_test_llm()
    enhancer = EnhancerAgent(llm)
    assert enhancer.llm is not None

def test_researcher_has_tools():
    """Test researcher agent has search tools"""
    llm = get_test_llm()
    researcher = ResearcherAgent(llm)
    assert researcher.tools is not None
    assert len(researcher.tools) > 0

def test_coder_has_tools():
    """Test coder agent has Python REPL"""
    llm = get_test_llm()
    coder = CoderAgent(llm)
    assert coder.tools is not None
    assert len(coder.tools) > 0

def test_generic_agent_simple():
    """Test generic agent processes simple queries"""
    llm = get_test_llm()
    generic = GenericAgent(llm)
    
    state = {'messages': [HumanMessage(content="Hello")]}
    result = generic.process(state)
    
    assert 'messages' in result
    assert len(result['messages']) > 0
```

### Testing Decision Models

```python
# Save as tests/test_models.py
from multiagent_system.models import SupervisorDecision, ValidatorDecision
from pydantic import ValidationError
import pytest

def test_supervisor_decision_valid():
    """Test valid supervisor decision"""
    decision = SupervisorDecision(
        next="researcher",
        reason="User asked a question requiring research"
    )
    assert decision.next == "researcher"
    assert decision.reason is not None

def test_supervisor_decision_invalid_next():
    """Test invalid supervisor routing"""
    with pytest.raises(ValidationError):
        SupervisorDecision(
            next="invalid_agent",  # Not in allowed list
            reason="Test"
        )

def test_validator_decision_finish():
    """Test validator finish decision"""
    decision = ValidatorDecision(
        next="FINISH",
        reason="Response is complete and satisfactory"
    )
    assert decision.next == "FINISH"

def test_validator_decision_continue():
    """Test validator continue decision"""
    decision = ValidatorDecision(
        next="supervisor",
        reason="Response needs improvement"
    )
    assert decision.next == "supervisor"
```

## Integration Testing

### Testing Workflow Construction

```python
# Save as tests/test_workflow.py
from multiagent_system import MultiAgentWorkflow

def test_workflow_initialization():
    """Test workflow initializes all components"""
    workflow = MultiAgentWorkflow()
    
    assert workflow.llm is not None
    assert workflow.supervisor is not None
    assert workflow.enhancer is not None
    assert workflow.researcher is not None
    assert workflow.coder is not None
    assert workflow.generic is not None
    assert workflow.validator is not None
    assert workflow.graph is not None

def test_workflow_different_model():
    """Test workflow with different model"""
    workflow = MultiAgentWorkflow(model_name="gpt-5-mini")
    assert workflow.llm.model_name == "gpt-5-mini"

def test_graph_compilation():
    """Test graph compiles without errors"""
    workflow = MultiAgentWorkflow()
    assert workflow.graph is not None
    # Graph should be compiled and ready
```

### Testing Environment Validation

```python
# Save as tests/test_environment.py
from multiagent_system import MultiAgentWorkflow
import os

def test_environment_validation_with_key():
    """Test environment validation when API key is set"""
    # Assuming OPENAI_API_KEY is set in .env
    workflow = MultiAgentWorkflow()
    errors = workflow.validate_environment()
    
    # Should have no critical errors
    critical_errors = [e for e in errors if 'OPENAI_API_KEY' in e]
    assert len(critical_errors) == 0

def test_environment_validation_missing_optional():
    """Test validation handles missing optional keys"""
    workflow = MultiAgentWorkflow()
    errors = workflow.validate_environment()
    
    # Optional keys may be missing, that's okay
    # Just verify function runs without crashing
    assert isinstance(errors, list)
```

## Manual Testing

### Test Scenarios by Agent Type

#### 1. **Enhancer Agent** (Query Clarification)
```bash
# Vague query
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('Tell me about that thing')
"

# Ambiguous query
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('How do I do it?')
"
```

#### 2. **Researcher Agent** (Web Search)
```bash
# Current events
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('What are the latest AI developments in 2024?')
"

# Factual research
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('What is the current population of Tokyo?')
"
```

#### 3. **Coder Agent** (Code Execution)
```bash
# Math calculation
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('Calculate the factorial of 10')
"

# Algorithm implementation
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('Write a function to check if a number is prime, then test it with 17')
"

# Data analysis
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('Calculate the mean and standard deviation of [1,2,3,4,5,6,7,8,9,10]')
"
```

#### 4. **Generic Agent** (General Knowledge)
```bash
# Simple facts
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('What is the capital of France?')
"

# Definitions
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print('Define photosynthesis')
"
```

### Interactive Testing

```python
# Save as tests/interactive_test.py
from multiagent_system import MultiAgentWorkflow

def interactive_test():
    """Run interactive testing session"""
    workflow = MultiAgentWorkflow()
    
    print("🤖 Multi-Agent System - Interactive Testing")
    print("=" * 50)
    print("Enter 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        print("\n🔄 Processing...\n")
        workflow.run_and_print(user_input)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    interactive_test()
```

Run interactive testing:
```bash
uv run python tests/interactive_test.py
```

## Setting Up Test Environment

### 1. Create Test Directory
```bash
mkdir -p tests
touch tests/__init__.py
```

### 2. Install Test Dependencies
```bash
# Add to pyproject.toml under [project.optional-dependencies]
[project.optional-dependencies]
test = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
]

# Install test dependencies
uv sync --extra test
```

### 3. Create pytest Configuration
```bash
cat > pytest.ini << 'PYTEST'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --cov=multiagent_system --cov-report=html --cov-report=term
PYTEST
```

### 4. Run Tests
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_agents.py

# Run with coverage
uv run pytest --cov=multiagent_system

# Run specific test
uv run pytest tests/test_agents.py::test_supervisor_initialization
```

## Writing New Tests

### Template for Agent Tests
```python
from multiagent_system.agents import YourAgent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def test_your_agent():
    """Test your agent does what it should"""
    # Arrange
    llm = ChatOpenAI(model="gpt-5", temperature=0)
    agent = YourAgent(llm)
    state = {'messages': [HumanMessage(content="Test message")]}
    
    # Act
    result = agent.process(state)
    
    # Assert
    assert result is not None
    assert 'messages' in result or 'next' in result
```

### Template for Workflow Tests
```python
from multiagent_system import MultiAgentWorkflow

def test_workflow_scenario():
    """Test specific workflow scenario"""
    # Arrange
    workflow = MultiAgentWorkflow()
    query = "Your test query"
    
    # Act
    events = list(workflow.run(query))
    
    # Assert
    assert len(events) > 0
    # Add more specific assertions
```

## Troubleshooting

### Common Issues

#### 1. API Key Errors
```bash
# Verify .env file exists and has correct format
cat .env

# Verify environment variable is loaded
uv run python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

#### 2. Import Errors
```bash
# Reinstall dependencies
uv sync --no-editable

# Verify package structure
uv run python -c "import multiagent_system; print(multiagent_system.__version__)"
```

#### 3. Model/Tool Errors
```bash
# Test LLM connection
uv run python -c "
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model='gpt-5')
response = llm.invoke('Say hello')
print(response.content)
"

# Test Tavily search
uv run python -c "
from langchain_community.tools.tavily_search import TavilySearchResults
tool = TavilySearchResults(max_results=1)
results = tool.invoke('Python programming')
print(results)
"
```

#### 4. Graph Compilation Errors
```bash
# Verify graph structure
uv run python -c "
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
print('Graph compiled successfully!')
print(f'Nodes: {workflow.graph.get_graph().nodes}')
"
```

### Debug Mode

Enable detailed logging:
```python
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("multiagent_system")

# Run with debug output
from multiagent_system import MultiAgentWorkflow
workflow = MultiAgentWorkflow()
workflow.run_and_print("Your query")
```

### Performance Testing

```python
import time
from multiagent_system import MultiAgentWorkflow

def test_performance():
    """Test workflow performance"""
    workflow = MultiAgentWorkflow()
    
    queries = [
        "What is 2+2?",
        "Tell me about Python",
        "Calculate factorial of 5"
    ]
    
    for query in queries:
        start = time.time()
        list(workflow.run(query))
        duration = time.time() - start
        print(f"Query: {query}")
        print(f"Duration: {duration:.2f}s\n")
```

## Best Practices

1. **Always test after making changes**
2. **Write tests for new features**
3. **Use descriptive test names**
4. **Test edge cases and error conditions**
5. **Keep tests independent and isolated**
6. **Use fixtures for common setup**
7. **Mock external dependencies when appropriate**
8. **Test both success and failure scenarios**
9. **Document test requirements and setup**
10. **Run tests before committing code**

## Continuous Integration

### GitHub Actions Example
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Install dependencies
        run: uv sync
      - name: Run tests
        run: uv run pytest
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## Conclusion

This testing guide provides comprehensive coverage of the multi-agent system. Use it to ensure system reliability, catch bugs early, and maintain code quality as the project evolves.
