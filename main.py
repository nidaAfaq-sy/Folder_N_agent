import asyncio
import json
from typing import Dict, Any
from loguru import logger
from dotenv import load_dotenv
from agents.base_agent import AgentConfig
from agents.orchestrator import OrchestratorAgent
from agents.research_agent import ResearchAgent

# Load environment variables
load_dotenv()

# Configure logging
logger.add("agent_system.log", rotation="500 MB")

async def process_request(orchestrator: OrchestratorAgent, request: Dict[str, Any]) -> Dict[str, Any]:
    """Process a request through the orchestrator.
    
    Args:
        orchestrator: The orchestrator agent instance
        request: The request to process
        
    Returns:
        Dictionary containing processing results
    """
    try:
        result = await orchestrator.process(request)
        logger.info(f"Request processed successfully: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

async def main():
    """Main application entry point."""
    try:
        # Create agent configurations
        orchestrator_config = AgentConfig(
            name="orchestrator",
            description="Main orchestrator agent"
        )
        
        research_config = AgentConfig(
            name="research",
            description="Research agent for information gathering"
        )
        
        # Initialize agents
        orchestrator = OrchestratorAgent(orchestrator_config)
        research_agent = ResearchAgent(research_config)
        
        # Register agents with orchestrator
        orchestrator.register_agent(research_agent)
        
        # Example request
        request = {
            "query": "artificial intelligence",
            "max_results": 5
        }
        
        # Process request
        result = await process_request(orchestrator, request)
        
        # Print results
        print("\nProcessing Results:")
        print(json.dumps(result, indent=2))
        
        # Print agent statuses
        print("\nAgent Statuses:")
        for status in orchestrator.get_agent_statuses():
            print(json.dumps(status, indent=2))
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 