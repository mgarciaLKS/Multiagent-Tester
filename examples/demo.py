#!/usr/bin/env python3
"""
Main Entry Point for Multi-Agent Workflow System
Run examples and demonstrations of the multi-agent system
"""
from multiagent_system import MultiAgentWorkflow


def main():
    """Main function to demonstrate the multi-agent workflow system"""
    
    # Initialize the workflow
    print("🤖 Initializing Multi-Agent Workflow System...")
    print("📦 Loading from modular package structure...")
    workflow = MultiAgentWorkflow()
    print("✅ Workflow initialized successfully!\n")
    
    # Example 1: Short story request
    print("="*70)
    print("Example 1: Creative Content Generation")
    print("="*70)
    workflow.run_and_print("Cuéntame un cuento corto")
    
    # Example 2: Fibonacci calculation
    print("="*70)
    print("Example 2: Mathematical Computation")
    print("="*70)
    workflow.run_and_print("calcula el número 20 en la serie de Fibonacci")
    
    # Example 3: Research question
    print("="*70)
    print("Example 3: Research & Information Gathering")
    print("="*70)
    workflow.run_and_print("What are the latest developments in AI?")
    
    # Example 4: Generic question
    print("="*70)
    print("Example 4: General Knowledge Question")
    print("="*70)
    workflow.run_and_print("What is the capital of France?")
    
    print("✅ All examples completed!")


if __name__ == "__main__":
    main()
