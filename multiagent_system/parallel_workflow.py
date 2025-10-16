"""
Parallel Workflow Module
Executes multiple testing agents in parallel for faster test generation
"""
import asyncio
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from .agents import (
    SupervisorAgent,
    FunctionalTesterAgent,
    UnitTesterAgent,
    IntegrationTesterAgent,
    ValidatorAgent,
)


class ParallelTestingWorkflow:
    """Parallel execution workflow for faster test generation"""
    
    def __init__(self, model_name: str = "gpt-4o"):
        """
        Initialize the parallel workflow
        
        Args:
            model_name: The OpenAI model to use (default: gpt-4o)
        """
        # Initialize LLM
        self.llm = ChatOpenAI(model=model_name)
        
        # Initialize agents
        self.supervisor = SupervisorAgent(self.llm)
        self.unit_tester = UnitTesterAgent(self.llm)
        self.functional_tester = FunctionalTesterAgent(self.llm)
        self.integration_tester = IntegrationTesterAgent(self.llm)
        self.validator = ValidatorAgent(self.llm)
    
    async def _run_agent_async(self, agent, state: Dict[str, Any], agent_name: str) -> Dict[str, Any]:
        """
        Run a single agent asynchronously
        
        Args:
            agent: The agent to run
            state: The current state
            agent_name: Name of the agent for logging
            
        Returns:
            Result dictionary with agent name and output
        """
        print(f"🚀 Starting {agent_name}...")
        
        try:
            # Run agent synchronously in async context
            result = await asyncio.to_thread(agent.process, state)
            
            print(f"✅ {agent_name} completed")
            
            return {
                "agent": agent_name,
                "success": True,
                "result": result,
                "messages": result.update.get("messages", [])
            }
        except Exception as e:
            print(f"❌ {agent_name} failed: {e}")
            return {
                "agent": agent_name,
                "success": False,
                "error": str(e),
                "messages": []
            }
    
    async def run_parallel(self, user_input: str) -> Dict[str, Any]:
        """
        Run all testing agents in parallel
        
        Args:
            user_input: The user's request
            
        Returns:
            Combined results from all agents
        """
        print("=" * 80)
        print("🔀 PARALLEL EXECUTION MODE")
        print("=" * 80)
        print()
        
        # Initial state
        initial_state = {
            "messages": [
                HumanMessage(content=user_input, name="user")
            ]
        }
        
        # Phase 1: Supervisor analyzes the request
        print("📋 Phase 1: Supervisor Analysis")
        print("-" * 80)
        supervisor_result = self.supervisor.process(initial_state)
        supervisor_decision = supervisor_result.goto
        
        print(f"Supervisor recommends: {supervisor_decision}")
        print()
        
        # Phase 2: Run all testing agents in parallel
        print("⚡ Phase 2: Parallel Test Generation")
        print("-" * 80)
        print("Running Unit, Functional, and Integration testers simultaneously...")
        print()
        
        # Prepare states for each agent
        unit_state = {
            "messages": initial_state["messages"] + supervisor_result.update["messages"]
        }
        functional_state = unit_state.copy()
        integration_state = unit_state.copy()
        
        # Run agents in parallel
        results = await asyncio.gather(
            self._run_agent_async(self.unit_tester, unit_state, "UnitTester"),
            self._run_agent_async(self.functional_tester, functional_state, "FunctionalTester"),
            self._run_agent_async(self.integration_tester, integration_state, "IntegrationTester"),
            return_exceptions=True
        )
        
        print()
        print("=" * 80)
        print("📊 Phase 3: Results Summary")
        print("=" * 80)
        print()
        
        # Collect successful results
        successful_results = [r for r in results if not isinstance(r, Exception) and r.get("success")]
        failed_results = [r for r in results if isinstance(r, Exception) or not r.get("success")]
        
        print(f"✅ Successful: {len(successful_results)}")
        print(f"❌ Failed: {len(failed_results)}")
        print()
        
        # Phase 4: Validate combined results
        if successful_results:
            print("🔍 Phase 4: Validation")
            print("-" * 80)
            
            # Combine all messages
            all_messages = initial_state["messages"].copy()
            for result in successful_results:
                all_messages.extend(result.get("messages", []))
            
            validation_state = {"messages": all_messages}
            validation_result = self.validator.process(validation_state)
            
            decision = validation_result.goto
            print(f"Validator decision: {decision}")
            print()
        
        return {
            "supervisor_decision": supervisor_decision,
            "parallel_results": results,
            "successful_count": len(successful_results),
            "failed_count": len(failed_results),
            "validation": validation_result if successful_results else None,
            "all_messages": all_messages if successful_results else initial_state["messages"]
        }
    
    def run_parallel_sync(self, user_input: str) -> Dict[str, Any]:
        """
        Synchronous wrapper for parallel execution
        
        Args:
            user_input: The user's request
            
        Returns:
            Combined results from all agents
        """
        return asyncio.run(self.run_parallel(user_input))
    
    def print_results(self, results: Dict[str, Any]):
        """
        Pretty print the results
        
        Args:
            results: Results dictionary from run_parallel
        """
        print()
        print("=" * 80)
        print("📈 FINAL RESULTS")
        print("=" * 80)
        print()
        
        print(f"Supervisor Initial Recommendation: {results['supervisor_decision']}")
        print(f"Agents Run in Parallel: 3 (Unit, Functional, Integration)")
        print(f"Successful Completions: {results['successful_count']}")
        print(f"Failed Attempts: {results['failed_count']}")
        print()
        
        print("Agent Outputs:")
        print("-" * 80)
        for result in results['parallel_results']:
            if isinstance(result, Exception):
                print(f"❌ Exception: {result}")
                continue
                
            agent_name = result.get('agent', 'Unknown')
            success = result.get('success', False)
            status = "✅" if success else "❌"
            
            print(f"{status} {agent_name}:")
            if success:
                messages = result.get('messages', [])
                if messages:
                    content = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
                    preview = content[:200] + "..." if len(content) > 200 else content
                    print(f"   Output: {preview}")
            else:
                error = result.get('error', 'Unknown error')
                print(f"   Error: {error}")
            print()
        
        if results.get('validation'):
            print("Validation Decision:")
            print("-" * 80)
            val_result = results['validation']
            print(f"Next Step: {val_result.goto}")
            if val_result.update.get('messages'):
                val_msg = val_result.update['messages'][-1].content
                print(f"Reason: {val_msg[:300]}...")
        
        print()
        print("=" * 80)
