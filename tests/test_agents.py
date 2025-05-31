import pytest
from agents.base_agent import AgentConfig
from agents.orchestrator import OrchestratorAgent
from agents.research_agent import ResearchAgent

@pytest.fixture
def orchestrator_config():
    return AgentConfig(
        name="test_orchestrator",
        description="Test orchestrator"
    )

@pytest.fixture
def research_config():
    return AgentConfig(
        name="test_research",
        description="Test research agent"
    )

@pytest.fixture
async def orchestrator(orchestrator_config):
    return OrchestratorAgent(orchestrator_config)

@pytest.fixture
async def research_agent(research_config):
    return ResearchAgent(research_config)

@pytest.mark.asyncio
async def test_orchestrator_initialization(orchestrator):
    """Test orchestrator initialization."""
    assert orchestrator.config.name == "test_orchestrator"
    assert orchestrator.config.description == "Test orchestrator"
    assert len(orchestrator.agents) == 0

@pytest.mark.asyncio
async def test_agent_registration(orchestrator, research_agent):
    """Test agent registration with orchestrator."""
    orchestrator.register_agent(research_agent)
    assert len(orchestrator.agents) == 1
    assert "test_research" in orchestrator.agents

@pytest.mark.asyncio
async def test_research_agent_processing(research_agent):
    """Test research agent processing."""
    input_data = {
        "query": "test query"
    }
    result = await research_agent.process(input_data)
    assert result["status"] == "success"
    assert "results" in result
    assert len(result["results"]) > 0

@pytest.mark.asyncio
async def test_invalid_input_handling(research_agent):
    """Test handling of invalid input."""
    input_data = {
        "invalid_field": "test"
    }
    result = await research_agent.process(input_data)
    assert result["status"] == "error"
    assert "message" in result

@pytest.mark.asyncio
async def test_orchestrator_processing(orchestrator, research_agent):
    """Test orchestrator processing with registered agent."""
    orchestrator.register_agent(research_agent)
    input_data = {
        "query": "test query"
    }
    result = await orchestrator.process(input_data)
    assert result["status"] in ["success", "partial_success"]
    assert "results" in result
    assert "test_research" in result["results"] 