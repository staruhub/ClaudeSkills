# CrewAI Advanced Patterns and Integration Guide

This document provides advanced patterns, integrations, and production deployment strategies for CrewAI.

## MCP (Model Context Protocol) Integration

CrewAI supports MCP servers to extend agent capabilities with external services.

### Using MCP Servers as Tools

```python
from crewai import Agent
from crewai_tools import MCPTool

# Connect to MCP server
mcp_tool = MCPTool(
    server_name="filesystem",
    tool_name="read_file",
    server_config={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    }
)

# Use in agent
agent = Agent(
    role="File Analyst",
    goal="Analyze file contents",
    tools=[mcp_tool]
)
```

### Multiple MCP Servers

```python
# File system server
fs_tool = MCPTool(
    server_name="filesystem",
    tool_name="read_file"
)

# Database server
db_tool = MCPTool(
    server_name="postgres",
    tool_name="query"
)

# Web search server
search_tool = MCPTool(
    server_name="brave-search",
    tool_name="search"
)

agent = Agent(
    role="Data Analyst",
    tools=[fs_tool, db_tool, search_tool]
)
```

## Observability and Tracing

### LangChain Tracing

```python
import os

# Enable LangChain tracing
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = 'your-api-key'
os.environ['LANGCHAIN_PROJECT'] = 'crewai-production'

from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    verbose=True
)

# Traces will appear in LangSmith
result = crew.kickoff()
```

### Arize Phoenix

```python
from phoenix.otel import register

# Initialize Phoenix tracing
tracer_provider = register(
    project_name="crewai-project",
    endpoint="http://localhost:6006/v1/traces"
)

from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2]
)

result = crew.kickoff()
```

### OpenLIT

```python
import openlit

# Initialize OpenLIT
openlit.init(
    otlp_endpoint="http://localhost:4318",
    application_name="crewai-app"
)

from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2]
)

result = crew.kickoff()
```

## Production Deployment Strategies

### Environment Management

```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment-specific config
env = os.getenv('ENVIRONMENT', 'development')
env_file = Path(f'.env.{env}')

if env_file.exists():
    load_dotenv(env_file)

# Configuration
class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SERPER_API_KEY = os.getenv('SERPER_API_KEY')
    MAX_RPM = int(os.getenv('MAX_RPM', '10'))
    VERBOSE = os.getenv('VERBOSE', 'false').lower() == 'true'
    ENABLE_MEMORY = os.getenv('ENABLE_MEMORY', 'true').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
```

### Retry Logic and Error Handling

```python
from crewai import Crew, Agent, Task
import time

def execute_crew_with_retry(crew, inputs, max_retries=3):
    """Execute crew with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            result = crew.kickoff(inputs=inputs)
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)

# Usage
crew = Crew(agents=[agent], tasks=[task])
result = execute_crew_with_retry(
    crew,
    inputs={'topic': 'AI'},
    max_retries=3
)
```

### Rate Limiting

```python
from crewai import Crew
from ratelimit import limits, sleep_and_retry

# Rate limit at crew level
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    max_rpm=10  # 10 requests per minute
)

# Custom rate limiting wrapper
@sleep_and_retry
@limits(calls=100, period=3600)  # 100 calls per hour
def execute_crew_rate_limited(crew, inputs):
    return crew.kickoff(inputs=inputs)

result = execute_crew_rate_limited(crew, {'topic': 'AI'})
```

### Caching Strategies

```python
from crewai import Crew
import functools
import hashlib
import json

# Result caching
@functools.lru_cache(maxsize=128)
def cached_crew_execution(inputs_hash):
    """Cache crew results based on input hash"""
    inputs = json.loads(inputs_hash)
    crew = Crew(agents=[agent], tasks=[task])
    return crew.kickoff(inputs=inputs)

# Usage
inputs = {'topic': 'AI'}
inputs_hash = hashlib.md5(
    json.dumps(inputs, sort_keys=True).encode()
).hexdigest()
result = cached_crew_execution(inputs_hash)

# Enable crew-level caching
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    cache=True  # Enable response caching
)
```

## Advanced Flow Patterns

### Conditional Branching Flow

```python
from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel

class AnalysisState(BaseModel):
    data: str = ""
    complexity: str = "low"  # low, medium, high
    result: str = ""

class DataAnalysisFlow(Flow[AnalysisState]):

    @start()
    def assess_complexity(self):
        # Analyze data complexity
        if len(self.state.data) < 100:
            self.state.complexity = "low"
        elif len(self.state.data) < 1000:
            self.state.complexity = "medium"
        else:
            self.state.complexity = "high"
        return self.state.complexity

    @router(assess_complexity)
    def route_analysis(self, complexity):
        routes = {
            "low": "quick_analysis",
            "medium": "standard_analysis",
            "high": "deep_analysis"
        }
        return routes[complexity]

    @listen("quick_analysis")
    def quick_analysis(self):
        # Fast analysis for simple data
        self.state.result = "Quick analysis complete"
        return self.state.result

    @listen("standard_analysis")
    def standard_analysis(self):
        # Standard analysis with crew
        crew = Crew(agents=[analyst], tasks=[analysis_task])
        result = crew.kickoff()
        self.state.result = result
        return self.state.result

    @listen("deep_analysis")
    def deep_analysis(self):
        # Deep analysis with multiple agents
        crew = Crew(
            agents=[researcher, analyst, reviewer],
            tasks=[research, analyze, review],
            process=Process.sequential
        )
        result = crew.kickoff()
        self.state.result = result
        return self.state.result
```

### Parallel Execution Flow

```python
from crewai.flow.flow import Flow, listen, start
from concurrent.futures import ThreadPoolExecutor, as_completed

class ParallelProcessingFlow(Flow):

    @start()
    def distribute_tasks(self):
        """Distribute tasks to multiple crews"""
        tasks = ["task1", "task2", "task3", "task4"]
        return tasks

    @listen(distribute_tasks)
    def process_parallel(self, tasks):
        """Execute crews in parallel"""
        def process_single_task(task):
            crew = Crew(agents=[agent], tasks=[task_template])
            return crew.kickoff(inputs={'task': task})

        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(process_single_task, task): task
                for task in tasks
            }
            for future in as_completed(futures):
                task = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Task {task} failed: {e}")

        return results

    @listen(process_parallel)
    def aggregate_results(self, results):
        """Combine results from parallel execution"""
        # Aggregate and summarize
        summary = "\n\n".join(results)
        return summary
```

### Long-Running Workflow with Persistence

```python
from crewai.flow.flow import Flow, listen, start
import pickle
from pathlib import Path

class PersistentWorkflow(Flow):

    def __init__(self, state_file='workflow_state.pkl'):
        super().__init__()
        self.state_file = Path(state_file)
        self.load_state()

    def save_state(self):
        """Save current state to disk"""
        with open(self.state_file, 'wb') as f:
            pickle.dump(self.state, f)

    def load_state(self):
        """Load state from disk if exists"""
        if self.state_file.exists():
            with open(self.state_file, 'rb') as f:
                self.state = pickle.load(f)

    @start()
    def step1(self):
        print("Executing step 1...")
        result = "Step 1 complete"
        self.save_state()
        return result

    @listen(step1)
    def step2(self, data):
        print("Executing step 2...")
        result = "Step 2 complete"
        self.save_state()
        return result

    @listen(step2)
    def step3(self, data):
        print("Executing step 3...")
        result = "Step 3 complete"
        self.save_state()
        return result

# Resume from saved state
workflow = PersistentWorkflow()
workflow.kickoff()
```

## Performance Optimization

### Agent Reuse

```python
from crewai import Agent

# Create reusable agent instances
_agent_cache = {}

def get_or_create_agent(role, goal, backstory, tools):
    """Cache and reuse agent instances"""
    cache_key = f"{role}:{goal}"
    if cache_key not in _agent_cache:
        _agent_cache[cache_key] = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools
        )
    return _agent_cache[cache_key]

# Usage
researcher = get_or_create_agent(
    role='Researcher',
    goal='Research topics',
    backstory='Expert researcher',
    tools=[search_tool]
)
```

### Lazy Loading

```python
from crewai import Crew, Agent, Task

class LazyCrewBuilder:
    def __init__(self):
        self._agents = None
        self._tasks = None
        self._crew = None

    @property
    def agents(self):
        if self._agents is None:
            self._agents = [
                Agent(role='Agent1', ...),
                Agent(role='Agent2', ...)
            ]
        return self._agents

    @property
    def tasks(self):
        if self._tasks is None:
            self._tasks = [
                Task(description='Task1', agent=self.agents[0]),
                Task(description='Task2', agent=self.agents[1])
            ]
        return self._tasks

    @property
    def crew(self):
        if self._crew is None:
            self._crew = Crew(
                agents=self.agents,
                tasks=self.tasks
            )
        return self._crew

# Usage - only creates crew when needed
builder = LazyCrewBuilder()
result = builder.crew.kickoff()
```

### Batch Processing

```python
from crewai import Crew
from typing import List, Dict

def batch_process(crew: Crew, inputs_list: List[Dict], batch_size: int = 10):
    """Process inputs in batches to manage resources"""
    results = []

    for i in range(0, len(inputs_list), batch_size):
        batch = inputs_list[i:i+batch_size]
        batch_results = crew.kickoff_for_each(inputs=batch)
        results.extend(batch_results)

        # Optional: Clear cache between batches
        crew.cache.clear() if hasattr(crew, 'cache') else None

    return results

# Usage
inputs_list = [{'topic': f'Topic {i}'} for i in range(100)]
crew = Crew(agents=[agent], tasks=[task])
results = batch_process(crew, inputs_list, batch_size=10)
```

## Testing Patterns

### Integration Testing

```python
import pytest
from crewai import Crew, Agent, Task

@pytest.fixture
def research_crew():
    """Fixture for research crew"""
    researcher = Agent(
        role='Researcher',
        goal='Research topics',
        backstory='Expert researcher',
        tools=[search_tool]
    )

    task = Task(
        description='Research {topic}',
        expected_output='Research report',
        agent=researcher
    )

    return Crew(agents=[researcher], tasks=[task])

def test_research_crew_integration(research_crew):
    """Test full research workflow"""
    result = research_crew.kickoff(inputs={'topic': 'AI'})

    assert result is not None
    assert len(result) > 0
    assert 'AI' in result

@pytest.mark.slow
def test_long_running_crew(research_crew):
    """Test crew with longer timeout"""
    import pytest
    import time

    start = time.time()
    result = research_crew.kickoff(inputs={'topic': 'Complex AI Topic'})
    duration = time.time() - start

    assert duration < 300  # Should complete within 5 minutes
    assert result is not None
```

### Mocking External Services

```python
import pytest
from unittest.mock import Mock, patch
from crewai import Agent, Task, Crew

@pytest.fixture
def mock_search_tool():
    """Mock external search tool"""
    tool = Mock()
    tool.run.return_value = "Mocked search results about AI"
    return tool

def test_crew_with_mocked_tools(mock_search_tool):
    """Test crew with mocked external dependencies"""
    agent = Agent(
        role='Researcher',
        goal='Research AI',
        backstory='Expert',
        tools=[mock_search_tool]
    )

    task = Task(
        description='Research AI',
        expected_output='Report',
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task])

    with patch.object(crew, 'kickoff', return_value="Test result"):
        result = crew.kickoff()
        assert result == "Test result"
        mock_search_tool.run.assert_called()
```

## Additional Resources

### Official Resources
- CrewAI Documentation: https://docs.crewai.com/
- CrewAI API Reference: https://docs.crewai.com/api-reference
- GitHub Repository: https://github.com/joaomdmoura/crewAI
- Examples and Cookbooks: https://github.com/joaomdmoura/crewAI-examples

### Community Resources
- CrewAI Community Forum: https://community.crewai.com/
- Discord Community: https://discord.gg/crewai
- YouTube Tutorials: Search for "CrewAI tutorials"

### Integration Guides
- MCP Integration: https://docs.crewai.com/mcp-integration
- LangChain Integration: https://docs.crewai.com/langchain
- Observability Tools: https://docs.crewai.com/observability

### Production Deployment
- CrewAI Enterprise: https://www.crewai.com/enterprise
- Deployment Best Practices: https://docs.crewai.com/deployment
- Scaling Guidelines: https://docs.crewai.com/scaling
