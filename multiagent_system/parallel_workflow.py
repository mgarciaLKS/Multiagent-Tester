"""
Parallel Workflow Module
Executes multiple testing agents in parallel for faster test generation
"""
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from .agents import (
    SupervisorAgent,
    FunctionalTesterAgent,
    UnitTesterAgent,
    IntegrationTesterAgent,
    ValidatorAgent,
    ReportAgent,
)


class ParallelTestingWorkflow:
    """Parallel execution workflow for faster test generation"""
    
    def __init__(self, model_name: str = "gpt-5", output_dir: Path = None):
        """
        Initialize the parallel workflow
        
        Args:
            model_name: The OpenAI model to use (default: gpt-5)
            output_dir: Directory where tests are generated (for validation)
        """
        # Initialize LLM
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        
        # Set output directory for validator
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "output"
        self.output_dir = output_dir
        
        # Initialize agents
        self.supervisor = SupervisorAgent(self.llm)
        self.unit_tester = UnitTesterAgent(self.llm)
        self.functional_tester = FunctionalTesterAgent(self.llm)
        self.integration_tester = IntegrationTesterAgent(self.llm)
        self.validator = ValidatorAgent(self.llm, self.output_dir)
        self.report_agent = ReportAgent(self.llm, self.output_dir)
    
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
        import time
        print(f"🚀 Starting {agent_name}...")
        start = time.time()
        
        try:
            # Run agent synchronously in async context
            result = await asyncio.to_thread(agent.process, state)
            elapsed = time.time() - start
            
            print(f"✅ {agent_name} completed in {elapsed:.1f}s")
            
            return {
                "agent": agent_name,
                "success": True,
                "result": result,
                "messages": result.update.get("messages", [])
            }
        except Exception as e:
            elapsed = time.time() - start
            print(f"❌ {agent_name} failed after {elapsed:.1f}s: {str(e)[:100]}")
            return {
                "agent": agent_name,
                "success": False,
                "error": str(e),
                "messages": []
            }
    
    async def run_parallel(self, user_input: str, max_iterations: int = 5) -> Dict[str, Any]:
        """
        Run testing agents with feedback loop until tests execute correctly
        
        Args:
            user_input: The user's request
            max_iterations: Maximum number of fix iterations (default: 3)
            
        Returns:
            Combined results from all agents
        """
        print("=" * 80)
        print("🔀 PARALLEL EXECUTION MODE WITH FEEDBACK LOOP")
        print("=" * 80)
        print()
        
        # Initial state
        initial_state = {
            "messages": [
                HumanMessage(content=user_input, name="user")
            ]
        }
        
        all_iterations = []
        iteration = 0
        tests_can_execute = False
        all_messages = initial_state["messages"].copy()
        
        while iteration < max_iterations and not tests_can_execute:
            iteration += 1
            print()
            print("=" * 80)
            print(f"🔄 ITERATION {iteration}/{max_iterations}")
            print("=" * 80)
            print()
            
            if iteration == 1:
                # Phase 1: Initial test generation
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
                
                # Run agents in parallel with longer timeout to ensure completion
                import time
                start_time = time.time()
                try:
                    results = await asyncio.wait_for(
                        asyncio.gather(
                            self._run_agent_async(self.unit_tester, unit_state, "UnitTester"),
                            self._run_agent_async(self.functional_tester, functional_state, "FunctionalTester"),
                            self._run_agent_async(self.integration_tester, integration_state, "IntegrationTester"),
                            return_exceptions=True
                        ),
                        timeout=600.0  # 10 minutes max for all agents to generate tests
                    )
                except asyncio.TimeoutError:
                    print("⚠️ Agents timed out after 300s, continuing with partial results...")
                    results = []
                elapsed = time.time() - start_time
                
                print()
                print("=" * 80)
                print(f"📊 Phase 3: Results Summary (took {elapsed:.1f}s)")
                print("=" * 80)
                print()
                
                # Collect successful results
                successful_results = [r for r in results if not isinstance(r, Exception) and r.get("success")]
                failed_results = [r for r in results if isinstance(r, Exception) or not r.get("success")]
                
                print(f"✅ Successful: {len(successful_results)}")
                print(f"❌ Failed: {len(failed_results)}")
                print()
                
                # Combine all messages - update existing all_messages
                all_messages.extend(supervisor_result.update["messages"])
                for result in successful_results:
                    all_messages.extend(result.get("messages", []))
            else:
                # Subsequent iterations: Fix based on validator feedback
                print("🔧 Phase: Targeted Fixes Based on Validator Feedback")
                print("-" * 80)
                
                # Get validator feedback from previous iteration
                prev_validation = all_iterations[-1].get("validation")
                if prev_validation and prev_validation.update.get("messages"):
                    validator_feedback = prev_validation.update["messages"][-1].content
                    
                    # Supervisor decides which agent needs to fix what
                    fix_state = {
                        "messages": all_messages + [
                            HumanMessage(content=f"Validator found issues. Fix them:\n{validator_feedback}", name="validator")
                        ]
                    }
                    
                    supervisor_result = self.supervisor.process(fix_state)
                    fix_decision = supervisor_result.goto
                    
                    print(f"Supervisor routes to: {fix_decision}")
                    print()
                    
                    # Run the appropriate agent to fix issues
                    agent_map = {
                        "unit_tester": (self.unit_tester, "UnitTester"),
                        "functional_tester": (self.functional_tester, "FunctionalTester"),
                        "integration_tester": (self.integration_tester, "IntegrationTester"),
                    }
                    
                    if fix_decision in agent_map:
                        agent, agent_name = agent_map[fix_decision]
                        fix_agent_state = {
                            "messages": fix_state["messages"] + supervisor_result.update["messages"]
                        }
                        
                        fix_result = await self._run_agent_async(agent, fix_agent_state, agent_name)
                        
                        if fix_result.get("success"):
                            all_messages.extend(fix_result.get("messages", []))
                            results = [fix_result]
                            successful_results = [fix_result]
                        else:
                            print(f"❌ Fix attempt failed: {fix_result.get('error')}")
                            results = [fix_result]
                            successful_results = []
                    else:
                        print(f"⚠️ Supervisor decision '{fix_decision}' not handled in fix loop")
                        results = []
                        successful_results = []
            
            # Phase 4: Validate
            validation_result = None
            
            if successful_results:
                print()
                print("🔍 Phase: Validation")
                print("-" * 80)
                
                validation_state = {"messages": all_messages}
                validation_result = self.validator.process(validation_state)
                
                # Add validation result to messages
                if validation_result.update.get("messages"):
                    all_messages.extend(validation_result.update["messages"])
                
                decision = validation_result.goto
                print(f"Validator decision: {decision}")
                
                # Only exit loop if validator explicitly says to finish (__end__)
                # OR if we're on the last iteration
                if decision == "__end__":
                    tests_can_execute = True
                    print(f"✅ Validator approved! Tests are ready.")
                elif decision == "supervisor":
                    tests_can_execute = False
                    print(f"🔄 Validator found issues, will route back to supervisor for fixes")
                else:
                    tests_can_execute = False
                
                # Get verification details for logging
                if hasattr(self.validator, 'verify_tests'):
                    verification = self.validator.verify_tests()
                    print(f"   Tests collected: {verification.get('tests_total', 0)}")
                    if verification.get('import_analysis', {}).get('has_import_errors'):
                        print(f"   ⚠️ Import errors detected")
                else:
                    tests_can_execute = (decision == "__end__")
                
                print()
            
            # Store iteration results
            all_iterations.append({
                "iteration": iteration,
                "results": results if 'results' in locals() else [],
                "validation": validation_result,
                "tests_executable": tests_can_execute
            })
        
        # Final phase: Generate comprehensive report
        print()
        print("=" * 80)
        print("📊 Final Phase: Report Generation")
        print("=" * 80)
        print()
        
        report_state = {"messages": all_messages}
        report_result = self.report_agent.process(report_state)
        
        if report_result.update.get("messages"):
            all_messages.extend(report_result.update["messages"])
        
        return {
            "iterations": all_iterations,
            "total_iterations": iteration,
            "tests_executable": tests_can_execute,
            "validation": validation_result,
            "report": report_result,
            "all_messages": all_messages
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
        
        print(f"Total Iterations: {results['total_iterations']}")
        print(f"Tests Executable: {'✅ YES' if results['tests_executable'] else '❌ NO'}")
        print()
        
        print("Iteration Summary:")
        print("-" * 80)
        for iteration_data in results['iterations']:
            iter_num = iteration_data['iteration']
            executable = iteration_data.get('tests_executable', False)
            status = "✅" if executable else "🔧"
            
            print(f"{status} Iteration {iter_num}:")
            
            # Show results from this iteration
            iteration_results = iteration_data.get('results', [])
            for result in iteration_results:
                if isinstance(result, Exception):
                    print(f"   ❌ Exception: {result}")
                    continue
                    
                agent_name = result.get('agent', 'Unknown')
                success = result.get('success', False)
                agent_status = "✅" if success else "❌"
                print(f"   {agent_status} {agent_name}")
            
            # Show validation decision
            validation = iteration_data.get('validation')
            if validation:
                print(f"   → Validator: {validation.goto}")
            print()
        
        if results.get('validation'):
            print("Final Validation:")
            print("-" * 80)
            val_result = results['validation']
            print(f"Decision: {val_result.goto}")
            if val_result.update.get('messages'):
                val_msg = val_result.update['messages'][-1].content
                print(f"Reason: {val_msg[:300]}...")
        
        print()
        print("=" * 80)
