#!/usr/bin/env python3
"""
Quick Test: Generate tests for audio.py only
============================================

A simpler demo that generates tests just for the audio.py file
to validate the system works before running the full project test.

Usage:
    uv run python examples/quick_test.py
"""

from multiagent_system import MultiAgentWorkflow


def main():
    """Run a quick test generation for a single file"""
    
    print("=" * 80)
    print("QUICK TEST: Generate Tests for audio.py")
    print("=" * 80)
    print()
    
    # Initialize workflow
    workflow = MultiAgentWorkflow()
    
    # Simpler request for just one file
    request = """
    Generate unit tests for the audio.py file in the WhatsApp MCP project.
    
    File path: /home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/whatsapp-mcp/whatsapp-mcp-server/audio.py
    
    This file handles audio file conversion. Please:
    1. Read the audio.py file
    2. Analyze the functions
    3. Generate comprehensive unit tests
    4. Save tests to /home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/whatsapp-mcp/whatsapp-mcp-server/tests/test_audio.py
    
    Use pytest, mock external dependencies (ffmpeg, file operations), and test edge cases.
    """
    
    print("🚀 Generating tests for audio.py...")
    print()
    
    # Run the workflow and collect results
    final_state = None
    for event in workflow.run(request):
        # Print node transitions
        for node, state in event.items():
            print(f"\n📍 Node: {node}")
            if "messages" in state and state["messages"]:
                last_msg = state["messages"][-1]
                print(f"   Agent: {getattr(last_msg, 'name', 'unknown')}")
                print(f"   Message: {last_msg.content[:200]}...")
        final_state = state
    
    print()
    print("=" * 80)
    print("✅ Test generation complete!")
    print("=" * 80)
    print()
    if final_state and "messages" in final_state:
        print(f"📊 Total messages: {len(final_state['messages'])}")
    print()
    print("Check: /home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/whatsapp-mcp/whatsapp-mcp-server/tests/test_audio.py")
    print()


if __name__ == "__main__":
    main()
