from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from loguru import logger
from pydantic import BaseModel

class AgentConfig(BaseModel):
    """Configuration for an agent."""
    name: str
    description: str
    enabled: bool = True
    max_retries: int = 3
    timeout: int = 30

class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logger.bind(agent=config.name)
        self.logger.info(f"Initializing agent: {config.name}")
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the input data and return results.
        
        Args:
            input_data: Dictionary containing input data for processing
            
        Returns:
            Dictionary containing processing results
        """
        pass
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate the input data.
        
        Args:
            input_data: Dictionary containing input data to validate
            
        Returns:
            Boolean indicating if input is valid
        """
        return True
    
    async def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle any errors that occur during processing.
        
        Args:
            error: The exception that occurred
            
        Returns:
            Dictionary containing error information
        """
        self.logger.error(f"Error in {self.config.name}: {str(error)}")
        return {
            "status": "error",
            "message": str(error),
            "agent": self.config.name
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent.
        
        Returns:
            Dictionary containing agent status information
        """
        return {
            "name": self.config.name,
            "description": self.config.description,
            "enabled": self.config.enabled,
            "status": "active"
        } 