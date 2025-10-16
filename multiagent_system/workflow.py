"""
Workflow Module
Main orchestrator class for the multi-agent workflow system
"""
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, MessagesState

from .agents import (
    SupervisorAgent,
    FunctionalTesterAgent,
    UnitTesterAgent,
    IntegrationTesterAgent,
    ValidatorAgent,
)


class MultiAgentWorkflow:
    """Main orchestrator class for the multi-agent workflow system"""
    
    def __init__(self, model_name: str = "gpt-4o"):
        """
        Initialize the workflow with agents and graph
        
        Args:
            model_name: The OpenAI model to use (default: gpt-4o)
        """
        # Initialize LLM
        self.llm = ChatOpenAI(model=model_name)
        
        # Initialize agents
        self.supervisor = SupervisorAgent(self.llm)
        self.functional_tester = FunctionalTesterAgent(self.llm)
        self.unit_tester = UnitTesterAgent(self.llm)
        self.integration_tester = IntegrationTesterAgent(self.llm)
        self.validator = ValidatorAgent(self.llm)
        
        # Build the workflow graph
        self.app = self._build_graph()
    
    def _build_graph(self):
        """
        Build and compile the LangGraph workflow
        
        Returns:
            Compiled graph ready for execution
        """
        graph = StateGraph(MessagesState)
        
        # Add nodes with agent process methods
        graph.add_node("supervisor", self.supervisor.process)
        graph.add_node("functional_tester", self.functional_tester.process)
        graph.add_node("unit_tester", self.unit_tester.process)
        graph.add_node("integration_tester", self.integration_tester.process)
        graph.add_node("validator", self.validator.process)
        
        # Set entry point
        graph.add_edge(START, "supervisor")
        
        # Compile and return the application
        return graph.compile()
    
    def run(self, user_input: str, config: dict = None):
        """
        Run the workflow with a user input
        
        Args:
            user_input: The user's query or request
            config: Optional configuration for the workflow
            
        Returns:
            Generator of workflow events
        """
        inputs = {
            "messages": [
                ("user", user_input),
            ]
        }
        
        return self.app.stream(inputs, config=config)
    
    def run_and_print(self, user_input: str, config: dict = None):
        """
        Run the workflow and print the results in a formatted way
        
        Args:
            user_input: The user's query or request  
            config: Optional configuration for the workflow
        """
        import pprint
        
        print(f"=== Processing: {user_input} ===")
        
        for event in self.run(user_input, config):
            for key, value in event.items():
                if value is None:
                    continue
                last_message = value.get("messages", [])[-1] if "messages" in value else None
                if last_message:
                    pprint.pprint(f"Output from node '{key}':")
                    pprint.pprint(last_message, indent=2, width=80, depth=None)
                    print()
        
        print("="*50 + "\n")
    
    def get_graph_image(self):
        """
        Get a visual representation of the workflow graph
        Note: Requires IPython/Jupyter environment
        
        Returns:
            PNG image of the workflow graph or None if IPython is not available
        """
        try:
            from IPython.display import Image, display
            return self.app.get_graph(xray=True).draw_mermaid_png()
        except ImportError:
            print("IPython not available. Cannot display graph image.")
            return None
    
    def validate_environment(self):
        """
        Validate that required environment variables are set
        
        Returns:
            bool: True if validation passes
            
        Raises:
            ValueError: If required environment variables are missing
        """
        import os
        
        required_vars = ['OPENAI_API_KEY']
        optional_vars = ['TAVILY_API_KEY', 'LANGSMITH_API_KEY', 'LANGFUSE_PUBLIC_KEY']
        
        missing_required = []
        missing_optional = []
        
        for var in required_vars:
            if not os.getenv(var) or os.getenv(var) == f"your_{var.lower()}_here":
                missing_required.append(var)
        
        for var in optional_vars:
            if not os.getenv(var) or os.getenv(var) == f"your_{var.lower()}_here":
                missing_optional.append(var)
        
        if missing_required:
            print(f"❌ Missing required environment variables: {missing_required}")
            print("💡 Please update your .env file with actual API keys")
            raise ValueError(f"Missing required environment variables: {missing_required}")
        
        if missing_optional:
            print(f"⚠️  Missing optional environment variables: {missing_optional}")
            print("ℹ️  Some features (search, tracing) may not work properly.")
        else:
            print("✅ All optional environment variables configured!")
        
        print("✅ Environment validation passed!")
        return True
