#!/usr/bin/env python3
"""
Main entry point for the Multi-Agent Workflow System
"""
from workflow import MultiAgentWorkflow


def main():
    """Main function to demonstrate the multi-agent workflow system"""
    
    # Initialize the workflow
    try:
        workflow = MultiAgentWorkflow()
        
        # Validate environment setup
        workflow.validate_environment()
        
        print("Multi-Agent Workflow System initialized successfully!\n")
        
        # Example 1: Short story request
        workflow.run_and_print("Cuéntame un cuento corto")
        
        # Example 2: Fibonacci calculation
        workflow.run_and_print("calcula el número 20 en la serie de Fibonacci")
        
        # Example 3: Research question
        workflow.run_and_print("What are the latest developments in AI agents?")
        
        # Example 4: Generic question
        workflow.run_and_print("What is the capital of France?")
        
    except Exception as e:
        print(f"Error initializing workflow: {e}")
        print("\nPlease check your environment variables in the .env file.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
