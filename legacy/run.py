#!/usr/bin/env python3
"""
UV-compatible runner for the Multi-Agent Workflow System
"""
import sys
import os
from pathlib import Path

# Add current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point for UV execution"""
    try:
        from workflow import MultiAgentWorkflow
        
        print("🤖 Multi-Agent Workflow System (UV Edition)")
        print("=" * 50)
        
        # Initialize workflow
        workflow = MultiAgentWorkflow()
        
        # Validate environment
        workflow.validate_environment()
        
        print("\n🚀 Starting demonstrations...\n")
        
        # Run examples
        examples = [
            ("Short Story", "Cuéntame un cuento corto"),
            ("Math Calculation", "calcula el número 20 en la serie de Fibonacci"),
            ("Research Question", "What are the latest developments in AI agents?"),
            ("Generic Question", "What is the capital of France?")
        ]
        
        for name, query in examples:
            print(f"📝 {name}: {query}")
            try:
                workflow.run_and_print(query)
            except Exception as e:
                print(f"❌ Error in {name}: {e}")
                print("Continuing with next example...\n")
        
        return 0
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Try running: uv sync")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Please check your .env configuration")
        return 1

if __name__ == "__main__":
    sys.exit(main())
