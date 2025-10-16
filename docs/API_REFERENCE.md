# API Reference - Multi-Agent System

## Table of Contents
1. [MultiAgentWorkflow](#multiagentworkflow)
2. [Base Agent](#baseagent)
3. [Agent Classes](#agent-classes)
4. [Decision Models](#decision-models)
5. [Usage Examples](#usage-examples)
6. [Type Definitions](#type-definitions)

---

## MultiAgentWorkflow

**Module**: `multiagent_system.workflow`

**Import**: `from multiagent_system import MultiAgentWorkflow`

### Class Definition

```python
class MultiAgentWorkflow:
    """
    Orchestrator class for the multi-agent workflow system.
    
    This class manages the entire workflow graph, including all agents
    (supervisor, enhancer, researcher, coder, generic, validator) and
    coordinates their interactions through a LangGraph state graph.
    """
```

### Constructor

#### `__init__(model_name: str = "gpt-4o")`

Initialize the multi-agent workflow system.

**Parameters:**
- `model_name` (str, optional): Name of the OpenAI model to use. Default: `"gpt-4o"`

**Raises:**
- `ValueError`: If OPENAI_API_KEY is not set in environment

**Example:**
```python
# Use default model
workflow = MultiAgentWorkflow()

# Use specific model
workflow = MultiAgentWorkflow(model_name="gpt-4o-mini")
```

### Methods

#### `run(user_input: str, config: dict = None) -> Generator`

Execute the workflow with a user input.

**Parameters:**
- `user_input` (str): The user's query or request
- `config` (dict, optional): Configuration dict for LangGraph execution

**Returns:**
- Generator yielding workflow events (node_name, state) tuples

**Example:**
```python
workflow = MultiAgentWorkflow()
for event in workflow.run("What is Python?"):
    node_name, state = event
    print(f"Node: {node_name}")
```

---

#### `run_and_print(user_input: str, config: dict = None) -> None`

Execute the workflow and print formatted output.

**Parameters:**
- `user_input` (str): The user's query or request
- `config` (dict, optional): Configuration dict for LangGraph execution

**Returns:**
- None (prints to stdout)

**Example:**
```python
workflow = MultiAgentWorkflow()
workflow.run_and_print("Calculate the factorial of 5")
```

**Output Format:**
```
🤖 Agent: supervisor
📝 Response: [agent output]

🤖 Agent: coder
📝 Response: [agent output]

✅ Final Answer:
[final response]
```

---

#### `get_graph_image() -> bytes`

Generate a visual representation of the workflow graph.

**Returns:**
- bytes: PNG image data of the graph

**Raises:**
- `ImportError`: If pygraphviz is not installed

**Example:**
```python
workflow = MultiAgentWorkflow()
image_data = workflow.get_graph_image()

with open("workflow_graph.png", "wb") as f:
    f.write(image_data)
```

---

#### `validate_environment() -> List[str]`

Validate that required environment variables are set.

**Returns:**
- List[str]: List of warning/error messages (empty if all valid)

**Example:**
```python
workflow = MultiAgentWorkflow()
errors = workflow.validate_environment()

if errors:
    for error in errors:
        print(f"⚠️  {error}")
```

---

### Attributes

#### `llm: ChatOpenAI`
The language model instance used by all agents.

#### `supervisor: SupervisorAgent`
Agent responsible for routing requests.

#### `enhancer: EnhancerAgent`
Agent responsible for query clarification.

#### `researcher: ResearcherAgent`
Agent responsible for web research.

#### `coder: CoderAgent`
Agent responsible for code execution.

#### `generic: GenericAgent`
Agent responsible for general questions.

#### `validator: ValidatorAgent`
Agent responsible for response validation.

#### `graph: CompiledGraph`
The compiled LangGraph workflow.

---

## BaseAgent

**Module**: `multiagent_system.agents.base_agent`

**Import**: `from multiagent_system.agents import BaseAgent`

### Class Definition

```python
class BaseAgent(ABC):
    """
    Abstract base class for all agents in the multi-agent system.
    
    All agents must inherit from this class and implement the process() method.
    """
```

### Constructor

#### `__init__(llm: ChatOpenAI)`

Initialize the base agent.

**Parameters:**
- `llm` (ChatOpenAI): Language model instance

---

### Abstract Methods

#### `process(state: MessagesState) -> Command | dict`

Process the current state and return a decision or updated state.

**Parameters:**
- `state` (MessagesState): Current workflow state containing messages

**Returns:**
- Command | dict: Either a routing Command or updated state dict

**Must be implemented by subclasses.**

---

## Agent Classes

### SupervisorAgent

**Module**: `multiagent_system.agents.supervisor_agent`

**Import**: `from multiagent_system.agents import SupervisorAgent`

#### Class Definition

```python
class SupervisorAgent(BaseAgent):
    """
    Orchestrates the workflow by routing requests to appropriate agents.
    
    Analyzes user requests and conversation history to determine which
    specialist agent should handle the request.
    """
```

#### Constructor

```python
SupervisorAgent(llm: ChatOpenAI)
```

#### Methods

##### `process(state: MessagesState) -> Command`

Route the request to the appropriate agent.

**Returns:**
- Command with routing decision

**Routing Options:**
- `"enhancer"`: For vague or unclear queries
- `"researcher"`: For queries requiring web search
- `"coder"`: For technical/coding tasks
- `"generic"`: For general knowledge questions

**Example:**
```python
from multiagent_system.agents import SupervisorAgent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o")
supervisor = SupervisorAgent(llm)

state = {'messages': [HumanMessage(content="What is AI?")]}
result = supervisor.process(state)
print(f"Route to: {result.goto}")
```

---

### EnhancerAgent

**Module**: `multiagent_system.agents.enhancer_agent`

**Import**: `from multiagent_system.agents import EnhancerAgent`

#### Class Definition

```python
class EnhancerAgent(BaseAgent):
    """
    Clarifies and improves user queries.
    
    Takes vague or ambiguous queries and transforms them into clear,
    specific instructions for other agents.
    """
```

#### Constructor

```python
EnhancerAgent(llm: ChatOpenAI)
```

#### Methods

##### `process(state: MessagesState) -> Command`

Enhance and clarify the user's query.

**Returns:**
- Command routing to supervisor with enhanced query

**Example:**
```python
from multiagent_system.agents import EnhancerAgent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o")
enhancer = EnhancerAgent(llm)

state = {'messages': [HumanMessage(content="Tell me about that thing")]}
result = enhancer.process(state)
```

---

### ResearcherAgent

**Module**: `multiagent_system.agents.researcher_agent`

**Import**: `from multiagent_system.agents import ResearcherAgent`

#### Class Definition

```python
class ResearcherAgent(BaseAgent):
    """
    Gathers information using web search.
    
    Uses Tavily search to find current information and answer
    queries requiring external data.
    """
```

#### Constructor

```python
ResearcherAgent(llm: ChatOpenAI)
```

#### Attributes

##### `tools: List[BaseTool]`
List containing TavilySearchResults tool.

##### `agent_executor: AgentExecutor`
React agent with search capabilities.

#### Methods

##### `process(state: MessagesState) -> Command`

Research the query using web search.

**Returns:**
- Command routing to validator with research results

**Example:**
```python
from multiagent_system.agents import ResearcherAgent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o")
researcher = ResearcherAgent(llm)

state = {'messages': [HumanMessage(content="Latest AI trends 2024")]}
result = researcher.process(state)
```

---

### CoderAgent

**Module**: `multiagent_system.agents.coder_agent`

**Import**: `from multiagent_system.agents import CoderAgent`

#### Class Definition

```python
class CoderAgent(BaseAgent):
    """
    Handles code execution and technical tasks.
    
    Uses PythonREPLTool to execute code, perform calculations,
    and solve technical problems.
    """
```

#### Constructor

```python
CoderAgent(llm: ChatOpenAI)
```

#### Attributes

##### `tools: List[BaseTool]`
List containing PythonREPLTool.

##### `agent_executor: AgentExecutor`
React agent with code execution capabilities.

#### Methods

##### `process(state: MessagesState) -> Command`

Execute code or perform calculations.

**Returns:**
- Command routing to validator with execution results

**Example:**
```python
from multiagent_system.agents import CoderAgent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o")
coder = CoderAgent(llm)

state = {'messages': [HumanMessage(content="Calculate factorial of 10")]}
result = coder.process(state)
```

**Security Note:** PythonREPLTool executes arbitrary code. Use with caution.

---

### GenericAgent

**Module**: `multiagent_system.agents.generic_agent`

**Import**: `from multiagent_system.agents import GenericAgent`

#### Class Definition

```python
class GenericAgent(BaseAgent):
    """
    Handles general knowledge questions.
    
    Provides direct responses to straightforward queries that don't
    require specialized tools or research.
    """
```

#### Constructor

```python
GenericAgent(llm: ChatOpenAI)
```

#### Methods

##### `process(state: MessagesState) -> Command`

Answer general questions directly.

**Returns:**
- Command routing to validator with direct response

**Example:**
```python
from multiagent_system.agents import GenericAgent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o")
generic = GenericAgent(llm)

state = {'messages': [HumanMessage(content="What is the capital of France?")]}
result = generic.process(state)
```

---

### ValidatorAgent

**Module**: `multiagent_system.agents.validator_agent`

**Import**: `from multiagent_system.agents import ValidatorAgent`

#### Class Definition

```python
class ValidatorAgent(BaseAgent):
    """
    Validates response quality and determines workflow continuation.
    
    Assesses whether the response adequately addresses the user's query
    and decides whether to finish or request improvements.
    """
```

#### Constructor

```python
ValidatorAgent(llm: ChatOpenAI)
```

#### Methods

##### `process(state: MessagesState) -> Command`

Validate the response and decide next action.

**Returns:**
- Command routing to either:
  - `"supervisor"`: Request improvements
  - `"__end__"`: Finish workflow (uses Command.FINISH)

**Example:**
```python
from multiagent_system.agents import ValidatorAgent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

llm = ChatOpenAI(model="gpt-4o")
validator = ValidatorAgent(llm)

state = {
    'messages': [
        HumanMessage(content="What is 2+2?"),
        AIMessage(content="2+2 equals 4.")
    ]
}
result = validator.process(state)
print(f"Decision: {result}")
```

---

## Decision Models

### SupervisorDecision

**Module**: `multiagent_system.models.decisions`

**Import**: `from multiagent_system.models import SupervisorDecision`

#### Class Definition

```python
class SupervisorDecision(BaseModel):
    """
    Structured output for supervisor routing decisions.
    """
```

#### Fields

##### `next: Literal["enhancer", "researcher", "coder", "generic"]`
The agent to route to next.

##### `reason: str`
Explanation for the routing decision.

#### Example

```python
from multiagent_system.models import SupervisorDecision

decision = SupervisorDecision(
    next="researcher",
    reason="User query requires current information from web search"
)

print(f"Route to: {decision.next}")
print(f"Reason: {decision.reason}")
```

---

### ValidatorDecision

**Module**: `multiagent_system.models.decisions`

**Import**: `from multiagent_system.models import ValidatorDecision`

#### Class Definition

```python
class ValidatorDecision(BaseModel):
    """
    Structured output for validator continuation decisions.
    """
```

#### Fields

##### `next: Literal["supervisor", "FINISH"]`
Decision to continue or finish workflow.

##### `reason: str`
Explanation for the decision.

#### Example

```python
from multiagent_system.models import ValidatorDecision

# Finish workflow
decision = ValidatorDecision(
    next="FINISH",
    reason="Response completely addresses user query"
)

# Continue workflow
decision = ValidatorDecision(
    next="supervisor",
    reason="Response lacks specific details"
)
```

---

## Usage Examples

### Basic Usage

```python
from multiagent_system import MultiAgentWorkflow

# Initialize workflow
workflow = MultiAgentWorkflow()

# Run a query
workflow.run_and_print("What is machine learning?")
```

### Custom Model

```python
from multiagent_system import MultiAgentWorkflow

# Use a different OpenAI model
workflow = MultiAgentWorkflow(model_name="gpt-4o-mini")
workflow.run_and_print("Tell me a joke")
```

### Streaming Events

```python
from multiagent_system import MultiAgentWorkflow

workflow = MultiAgentWorkflow()

for event in workflow.run("Calculate the Fibonacci sequence up to 100"):
    if len(event) > 0:
        node_name, state = event
        print(f"\n=== {node_name.upper()} ===")
        
        if 'messages' in state and len(state['messages']) > 0:
            last_message = state['messages'][-1]
            print(last_message.content)
```

### With Configuration

```python
from multiagent_system import MultiAgentWorkflow

workflow = MultiAgentWorkflow()

config = {
    "recursion_limit": 30,  # Max workflow steps
    "configurable": {
        "thread_id": "user-123"  # For conversation persistence
    }
}

workflow.run_and_print("Research quantum computing", config=config)
```

### Error Handling

```python
from multiagent_system import MultiAgentWorkflow

try:
    workflow = MultiAgentWorkflow()
    workflow.run_and_print("Your query here")
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Runtime error: {e}")
```

### Environment Validation

```python
from multiagent_system import MultiAgentWorkflow

workflow = MultiAgentWorkflow()

# Check environment setup
errors = workflow.validate_environment()
if errors:
    print("⚠️  Environment Issues:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✅ Environment configured correctly")
```

### Using Individual Agents

```python
from multiagent_system.agents import ResearcherAgent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Create LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Create agent
researcher = ResearcherAgent(llm)

# Create state
state = {
    'messages': [
        HumanMessage(content="What are the latest developments in quantum computing?")
    ]
}

# Process
result = researcher.process(state)
print(result)
```

### Custom Workflow with Subset of Agents

```python
from multiagent_system.agents import SupervisorAgent, GenericAgent, ValidatorAgent
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START

# Create LLM
llm = ChatOpenAI(model="gpt-4o")

# Create agents
supervisor = SupervisorAgent(llm)
generic = GenericAgent(llm)
validator = ValidatorAgent(llm)

# Build custom graph
builder = StateGraph(MessagesState)
builder.add_node("supervisor", supervisor.process)
builder.add_node("generic", generic.process)
builder.add_node("validator", validator.process)

builder.add_edge(START, "supervisor")
# Add more edges...

graph = builder.compile()
```

---

## Type Definitions

### MessagesState

```python
from langgraph.graph import MessagesState

# TypedDict with:
# - messages: List[BaseMessage]
```

### Command

```python
from langgraph.types import Command

# Used for agent routing decisions
# Contains goto attribute for next node
```

### BaseMessage Types

```python
from langchain_core.messages import (
    HumanMessage,    # User input
    AIMessage,       # Agent response
    SystemMessage,   # System prompt
    ToolMessage,     # Tool output
)
```

---

## Environment Variables

### Required

- `OPENAI_API_KEY`: OpenAI API key for LLM access

### Optional

- `TAVILY_API_KEY`: Tavily API key for web search (required for researcher agent)
- `LANGSMITH_API_KEY`: LangSmith API key for tracing
- `LANGSMITH_TRACING`: Enable LangSmith tracing ("true" or "false")
- `LANGSMITH_PROJECT`: LangSmith project name
- `LANGFUSE_PUBLIC_KEY`: Langfuse public key for monitoring
- `LANGFUSE_SECRET_KEY`: Langfuse secret key
- `LANGFUSE_HOST`: Langfuse host URL

---

## Constants

### Model Names (OpenAI)

- `"gpt-4o"`: Most capable model (default)
- `"gpt-4o-mini"`: Faster, more cost-effective
- `"gpt-4-turbo"`: High performance
- `"gpt-3.5-turbo"`: Legacy, cost-effective

### Agent Names

- `"supervisor"`: Routing agent
- `"enhancer"`: Query clarification
- `"researcher"`: Web search
- `"coder"`: Code execution
- `"generic"`: General Q&A
- `"validator"`: Response validation

---

## Version Information

```python
from multiagent_system import __version__

print(__version__)  # "1.0.0"
```

---

## Further Reading

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

## Support

For issues, questions, or contributions, please refer to the project repository or documentation.
