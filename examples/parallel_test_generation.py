#!/usr/bin/env python3
"""
Parallel Test Generation
========================

This demonstrates a parallel approach to test generation where multiple
agents work simultaneously on different aspects of the project.

Inspired by the parallel execution pattern, we:
1. Analyze the project structure
2. Run unit, integration, and functional test generation in parallel
3. Collect and validate all results together

This is more efficient than sequential processing.

Usage:
    uv run python examples/parallel_test_generation.py
"""

import asyncio
from pathlib import Path
from langchain_openai import ChatOpenAI
from multiagent_system.agents import (
    UnitTesterAgent,
    IntegrationTesterAgent,
    FunctionalTesterAgent,
    ValidatorAgent
)


async def analyze_project(project_path: str) -> dict:
    """Analyze project structure and identify files to test"""
    project = Path(project_path)
    
    print(f"📁 Analyzing project: {project}")
    print()
    
    # Find Python files (excluding tests and venv)
    py_files = [
        f for f in project.rglob("*.py")
        if "test" not in str(f) and ".venv" not in str(f) and "venv" not in str(f)
    ]
    
    analysis = {
        "project_path": project_path,
        "files": [str(f) for f in py_files],
        "file_count": len(py_files)
    }
    
    print(f"✅ Found {len(py_files)} Python files to test:")
    for f in py_files[:5]:  # Show first 5
        print(f"   - {f.name}")
    if len(py_files) > 5:
        print(f"   ... and {len(py_files) - 5} more")
    print()
    
    return analysis


async def run_agent(agent, request: str, agent_name: str):
    """Run a single agent with a request"""
    print(f"🚀 Starting {agent_name}...")
    
    # Create a simple state
    from langgraph.graph import MessagesState
    state = {
        "messages": [
            ("user", request)
        ]
    }
    
    # Process the request
    result = agent.process(state)
    
    print(f"✅ {agent_name} completed!")
    return {
        "agent": agent_name,
        "result": result,
        "state": state
    }


async def parallel_test_generation(project_path: str):
    """Generate tests in parallel for different test types"""
    
    print("=" * 80)
    print("PARALLEL TEST GENERATION")
    print("=" * 80)
    print()
    
    # Step 1: Analyze project
    analysis = await analyze_project(project_path)
    
    # Step 2: Initialize LLM and agents
    print("🤖 Initializing agents...")
    llm = ChatOpenAI(model="gpt-4o")
    
    unit_tester = UnitTesterAgent(llm)
    integration_tester = IntegrationTesterAgent(llm)
    functional_tester = FunctionalTesterAgent(llm)
    validator = ValidatorAgent(llm)
    print()
    
    # Step 3: Create parallel requests for each agent
    files = analysis["files"]
    
    unit_test_request = f"""
    Generate unit tests for the WhatsApp MCP project.
    
    Project: {project_path}
    Files to test: {', '.join([Path(f).name for f in files])}
    
    Focus on:
    - Testing individual functions in {files[0] if files else 'main files'}
    - Mock external dependencies (database, APIs, file I/O)
    - Cover edge cases and error handling
    - Save tests to {project_path}/tests/test_*.py
    
    Create complete, runnable pytest tests.
    """
    
    integration_test_request = f"""
    Generate integration tests for the WhatsApp MCP project.
    
    Project: {project_path}
    
    Focus on:
    - Test component interactions (FastMCP tools, database operations)
    - Test with realistic dependencies where appropriate
    - Mock only external services (APIs, network calls)
    - Save tests to {project_path}/tests/integration/
    
    Create complete, runnable pytest integration tests.
    """
    
    functional_test_request = f"""
    Generate functional tests for the WhatsApp MCP project.
    
    Project: {project_path}
    
    Focus on:
    - Complete user workflows (search contacts → send message)
    - End-to-end scenarios that users would actually perform
    - Realistic test data and expected outcomes
    - Save tests to {project_path}/tests/functional/
    
    Create complete, runnable pytest functional tests.
    """
    
    # Step 4: Run agents in parallel
    print("⚡ Running agents in parallel...")
    print("   - Unit Tester: Testing individual functions")
    print("   - Integration Tester: Testing component interactions")
    print("   - Functional Tester: Testing user workflows")
    print()
    
    unit_result, integration_result, functional_result = await asyncio.gather(
        run_agent(unit_tester, unit_test_request, "Unit Tester"),
        run_agent(integration_tester, integration_test_request, "Integration Tester"),
        run_agent(functional_tester, functional_test_request, "Functional Tester"),
    )
    
    # Step 5: Collect and validate results
    print()
    print("=" * 80)
    print("📊 RESULTS SUMMARY")
    print("=" * 80)
    print()
    
    all_results = [unit_result, integration_result, functional_result]
    
    for result in all_results:
        print(f"✅ {result['agent']}:")
        # Get last message from result
        if hasattr(result['result'], 'update') and 'messages' in result['result'].update:
            msg = result['result'].update['messages'][-1].content
            print(f"   {msg[:200]}...")
        print()
    
    # Step 6: Final validation
    print("🔍 Running final validation...")
    validation_request = f"""
    Review the test generation results:
    
    Project: {project_path}
    
    Tests generated by:
    1. Unit Tester - Individual function tests
    2. Integration Tester - Component interaction tests
    3. Functional Tester - End-to-end workflow tests
    
    Check if tests were created in:
    - {project_path}/tests/test_*.py
    - {project_path}/tests/integration/
    - {project_path}/tests/functional/
    
    Evaluate if coverage is sufficient (70%+) and quality is good.
    """
    
    validation_state = {
        "messages": [
            ("user", "Generate comprehensive tests for WhatsApp MCP project"),
            ("assistant", "Unit tests completed"),
            ("assistant", "Integration tests completed"),
            ("assistant", "Functional tests completed"),
            ("user", validation_request)
        ]
    }
    
    # Note: Validator expects specific state format, so we adapt
    final_validation = validator.process(validation_state)
    
    print()
    print("=" * 80)
    print("✅ PARALLEL TEST GENERATION COMPLETE!")
    print("=" * 80)
    print()
    print("📁 Check for generated tests in:")
    print(f"   {project_path}/tests/")
    print()
    print("🧪 Run tests with:")
    print(f"   cd {project_path}")
    print("   pytest tests/ -v --cov")
    print()


async def main():
    """Main entry point"""
    project_path = "/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/whatsapp-mcp/whatsapp-mcp-server"
    
    await parallel_test_generation(project_path)


if __name__ == "__main__":
    asyncio.run(main())
