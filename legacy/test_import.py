#!/usr/bin/env python3
"""
Test script to validate UV installation and imports
"""
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        print("  📦 Testing basic Python imports...")
        import os
        import sys
        from typing import Literal
        from pydantic import BaseModel, Field
        print("  ✅ Basic imports OK")
        
        print("  📦 Testing dotenv...")
        from dotenv import load_dotenv
        load_dotenv()
        print("  ✅ dotenv OK")
        
        print("  📦 Testing LangChain core...")
        from langchain_core.messages import HumanMessage
        print("  ✅ LangChain core OK")
        
        print("  📦 Testing LangGraph...")
        from langgraph.graph import StateGraph, START, MessagesState
        from langgraph.types import Command
        from langgraph.prebuilt import create_react_agent
        print("  ✅ LangGraph OK")
        
        print("  📦 Testing OpenAI integration...")
        from langchain_openai import ChatOpenAI
        print("  ✅ OpenAI integration OK")
        
        print("  📦 Testing community tools...")
        from langchain_community.tools.tavily_search import TavilySearchResults
        from langchain_experimental.tools import PythonREPLTool
        print("  ✅ Community tools OK")
        
        print("  📦 Testing custom modules...")
        from agents import SupervisorAgent, EnhancerAgent, ResearcherAgent, CoderAgent, GenericAgent, ValidatorAgent
        from workflow import MultiAgentWorkflow
        print("  ✅ Custom modules OK")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try running: uv sync")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_environment():
    """Test environment variable setup"""
    print("\n🔍 Testing environment setup...")
    
    import os
    
    env_vars = {
        'OPENAI_API_KEY': 'Required',
        'TAVILY_API_KEY': 'Optional', 
        'LANGSMITH_API_KEY': 'Optional',
        'LANGFUSE_PUBLIC_KEY': 'Optional'
    }
    
    for var, status in env_vars.items():
        value = os.getenv(var)
        if value and not value.endswith('_here'):
            print(f"  ✅ {var}: Configured")
        elif status == 'Required':
            print(f"  ❌ {var}: Missing (Required)")
        else:
            print(f"  ⚠️  {var}: Not configured ({status})")
    
    print("💡 Update .env file with your actual API keys")

def main():
    """Main test runner"""
    print("🧪 UV Multi-Agent Workflow Test Suite")
    print("=" * 40)
    
    success = test_imports()
    test_environment()
    
    if success:
        print("\n🎉 All tests passed! Ready to run the workflow.")
        print("💡 Use: uv run run.py")
        return 0
    else:
        print("\n❌ Some tests failed. Please check your setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
