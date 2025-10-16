#!/usr/bin/env python3
"""
Demo: Automated Test Generation for a Real Project
===================================================

This script demonstrates the multi-agent system generating comprehensive
tests for the whatsapp-mcp project.

The workflow:
1. User provides project path
2. Supervisor analyzes project structure
3. Agents generate unit, integration, and functional tests
4. Validator ensures quality and coverage
5. Complete test suite is created

Usage:
    uv run python examples/test_project_generation.py
"""

from multiagent_system import MultiAgentWorkflow


def main():
    """Run the test generation demo for whatsapp-mcp project"""
    
    print("=" * 80)
    print("AUTOMATED TEST GENERATION DEMO")
    print("=" * 80)
    print()
    print("📦 Target Project: whatsapp-mcp")
    print("📁 Location: /home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/whatsapp-mcp")
    print()
    print("🎯 Objective: Generate comprehensive test suite")
    print("   - Unit tests for individual functions")
    print("   - Integration tests for API interactions")
    print("   - Functional tests for user workflows")
    print()
    print("=" * 80)
    print()
    
    # Initialize workflow
    workflow = MultiAgentWorkflow()
    
    # Project request
    project_request = """
    I need you to generate a comprehensive test suite for the WhatsApp MCP project.
    
    Project Path: /home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/whatsapp-mcp/whatsapp-mcp-server
    
    The project has 3 main Python files:
    1. main.py - FastMCP server with tool endpoints (~250 lines)
    2. whatsapp.py - Core WhatsApp operations (~767 lines)
    3. audio.py - Audio file processing (~110 lines)
    
    Please analyze the code and generate:
    
    1. **Unit Tests** (tests/test_*.py):
       - Test individual functions in whatsapp.py
       - Test audio processing functions in audio.py
       - Mock external dependencies (database, WhatsApp API)
       - Cover edge cases and error handling
    
    2. **Integration Tests** (tests/integration/):
       - Test FastMCP tool integrations in main.py
       - Test database operations with test data
       - Test file operations with temporary files
       - Verify error propagation between modules
    
    3. **Functional Tests** (tests/functional/):
       - Test complete user workflows:
         * Searching contacts and sending messages
         * Listing messages with filters
         * Downloading and sending media files
         * Managing chats
       - Test realistic scenarios end-to-end
    
    Requirements:
    - Use pytest framework
    - Follow best practices (fixtures, mocks, descriptive names)
    - Aim for 70%+ code coverage
    - Create tests/ directory in project root
    - Generate complete, runnable test files
    
    Please start by analyzing the code and creating unit tests first, then integration, then functional tests.
    """
    
    print("🚀 Starting test generation workflow...")
    print()
    
    # Run the workflow and collect results
    final_state = None
    step = 0
    for event in workflow.run(project_request):
        step += 1
        # Print node transitions
        for node, state in event.items():
            print(f"\n{'='*80}")
            print(f"📍 Step {step} - Node: {node.upper()}")
            print('='*80)
            if "messages" in state and state["messages"]:
                last_msg = state["messages"][-1]
                agent_name = getattr(last_msg, 'name', 'unknown')
                print(f"Agent: {agent_name}")
                print(f"Message Preview: {last_msg.content[:300]}...")
                print()
        final_state = state
    
    print()
    print("=" * 80)
    print("✅ WORKFLOW COMPLETE")
    print("=" * 80)
    print()
    print("📊 Results:")
    if final_state and "messages" in final_state:
        print(f"   Total messages: {len(final_state['messages'])}")
        print(f"   Total steps: {step}")
    print()
    print("📁 Check the project directory for generated test files:")
    print("   - tests/test_*.py (unit tests)")
    print("   - tests/integration/ (integration tests)")
    print("   - tests/functional/ (functional tests)")
    print()
    print("🧪 To run the generated tests:")
    print("   cd /home/mgarcia/Desktop/Otros/IA/CURSO\\ UPV\\ MCP/whatsapp-mcp/whatsapp-mcp-server")
    print("   pytest tests/ -v --cov")
    print()


if __name__ == "__main__":
    main()
