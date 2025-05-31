from typing import Dict, List, Any
from loguru import logger
from .base_agent import BaseAgent, AgentConfig

class OrchestratorAgent(BaseAgent):
    """Orchestrator agent that coordinates between different agents."""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.agents: Dict[str, BaseAgent] = {}
        self.logger = logger.bind(agent="orchestrator")
    
    def register_agent(self, agent: BaseAgent) -> None:
        """Register a new agent with the orchestrator.
        
        Args:
            agent: The agent instance to register
        """
        self.agents[agent.config.name] = agent
        self.logger.info(f"Registered agent: {agent.config.name}")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data by coordinating between registered agents.
        
        Args:
            input_data: Dictionary containing input data for processing
            
        Returns:
            Dictionary containing combined results from all agents
        """
        results = {}
        errors = []
        
        for agent_name, agent in self.agents.items():
            if not agent.config.enabled:
                self.logger.warning(f"Agent {agent_name} is disabled, skipping")
                continue
                
            try:
                if await agent.validate_input(input_data):
                    agent_result = await agent.process(input_data)
                    results[agent_name] = agent_result
                else:
                    self.logger.warning(f"Input validation failed for agent {agent_name}")
                    errors.append(f"Input validation failed for {agent_name}")
            except Exception as e:
                error_result = await agent.handle_error(e)
                errors.append(error_result)
        
        return {
            "status": "success" if not errors else "partial_success",
            "results": results,
            "errors": errors
        }
    
    def get_agent_statuses(self) -> List[Dict[str, Any]]:
        """Get the status of all registered agents.
        
        Returns:
            List of dictionaries containing status information for each agent
        """
        return [agent.get_status() for agent in self.agents.values()]
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for orchestrator processing.
        
        Args:
            input_data: Dictionary containing input data to validate
            
        Returns:
            Boolean indicating if input is valid
        """
        if not isinstance(input_data, dict):
            return False
        if not self.agents:
            self.logger.error("No agents registered with orchestrator")
            return False
        return True 