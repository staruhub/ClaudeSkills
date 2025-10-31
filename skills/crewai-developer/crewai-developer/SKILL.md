---
name: crewai-developer
description: Comprehensive CrewAI framework guide for building collaborative AI agent teams and structured workflows. Use when developing multi-agent systems with CrewAI, creating autonomous AI crews, orchestrating flows, implementing agents with roles and tools, or building production-ready AI automation. Essential for developers building intelligent agent systems, task automation, and complex AI workflows.
---

# CrewAI Developer Guide

## Overview

CrewAI is a lean, lightning-fast Python framework for building collaborative AI agent teams and structured workflows. It empowers developers to create autonomous AI agents with specific roles, tools, and goals that work together to tackle complex tasks. This skill covers Crews (autonomous collaboration), Flows (structured orchestration), agents, tasks, and enterprise deployment.

## Core Concepts

### Agents: Specialized Team Members

Agents are autonomous AI units with specific roles, goals, and capabilities.

```python
from crewai import Agent

# Create a research agent
researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI and data science',
    backstory="""You are an expert at a leading tech think tank.
    Your expertise lies in identifying emerging trends and technologies in AI,
    data science, and machine learning.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, scrape_tool]
)

# Create a writer agent
writer = Agent(
    role='Tech Content Strategist',
    goal='Craft compelling content on tech advancements',
    backstory="""You are a renowned content strategist, known for
    your insightful and engaging articles on technology and innovation.
    You transform complex concepts into compelling narratives.""",
    verbose=True,
    allow_delegation=True,
    tools=[write_tool]
)
```

#### Agent Key Properties

```python
agent = Agent(
    role='Role Name',              # The agent's job title
    goal='Specific objective',     # What the agent aims to achieve
    backstory='Background story',  # Context and expertise
    verbose=True,                  # Enable detailed logging
    allow_delegation=False,        # Can delegate tasks to other agents
    tools=[tool1, tool2],         # Available tools
    llm=custom_llm,               # Custom LLM configuration
    max_iter=15,                  # Maximum iterations for task
    max_rpm=10,                   # Rate limit (requests per minute)
    memory=True,                  # Enable memory
    cache=True,                   # Enable response caching
    system_template="template",   # Custom system prompt template
    prompt_template="template",   # Custom prompt template
    response_template="template"  # Custom response template
)
```

### Tasks: Individual Assignments

Tasks define specific work to be completed by agents.

```python
from crewai import Task

# Research task
research_task = Task(
    description="""Conduct a comprehensive analysis of the latest advancements in AI.
    Identify key trends, breakthrough technologies, and potential industry impacts.
    Compile your findings in a detailed report.""",
    expected_output='A comprehensive 3-paragraph report on AI advancements',
    agent=researcher,
    tools=[search_tool],
    output_file='research_report.md'
)

# Writing task
write_task = Task(
    description="""Using the research analyst's report, develop an engaging blog post
    highlighting the most significant AI advancements.
    Make it accessible and engaging for a general audience.""",
    expected_output='A 4-paragraph blog post about AI advancements',
    agent=writer,
    context=[research_task],  # Depends on research_task output
    output_file='blog_post.md'
)
```

#### Task Key Properties

```python
task = Task(
    description='Detailed task description',
    expected_output='Clear output format',
    agent=agent_instance,
    tools=[tool1, tool2],           # Task-specific tools
    context=[previous_task],        # Dependencies
    async_execution=False,          # Run asynchronously
    output_json=OutputClass,        # Structured output (Pydantic)
    output_pydantic=OutputClass,    # Pydantic validation
    output_file='result.txt',       # Save output to file
    callback=callback_function,     # Callback on completion
    human_input=False              # Request human feedback
)
```

### Crews: Organizing Agent Teams

Crews orchestrate agents working together toward a common goal.

```python
from crewai import Crew, Process

# Create a crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # or Process.hierarchical
    verbose=True,
    memory=True,
    cache=True,
    max_rpm=10,
    share_crew=False
)

# Kickoff the crew
result = crew.kickoff()
print(result)

# Kickoff with custom inputs
result = crew.kickoff(inputs={
    'topic': 'Artificial Intelligence',
    'audience': 'developers'
})
```

#### Process Types

```python
# Sequential process (tasks run one after another)
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sequential
)

# Hierarchical process (manager delegates to agents)
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.hierarchical,
    manager_llm='gpt-4'  # Required for hierarchical
)
```

### Flows: Structured Workflow Orchestration

Flows provide event-driven, deterministic control over execution paths.

```python
from crewai.flow.flow import Flow, listen, start

class BlogPostFlow(Flow):

    @start()
    def fetch_topic(self):
        """Entry point - fetch the topic to write about"""
        print("Starting blog post generation")
        return "AI advancements in 2024"

    @listen(fetch_topic)
    def research_topic(self, topic):
        """Research the topic"""
        print(f"Researching: {topic}")
        # Integrate with Crew for autonomous research
        research_crew = Crew(
            agents=[researcher],
            tasks=[research_task]
        )
        result = research_crew.kickoff(inputs={'topic': topic})
        return result

    @listen(research_topic)
    def write_blog_post(self, research_data):
        """Write the blog post"""
        print("Writing blog post...")
        write_crew = Crew(
            agents=[writer],
            tasks=[write_task]
        )
        result = write_crew.kickoff(inputs={'research': research_data})
        return result

    @listen(write_blog_post)
    def finalize(self, blog_post):
        """Finalize and save"""
        print("Blog post completed!")
        return blog_post

# Execute flow
flow = BlogPostFlow()
result = flow.kickoff()
```

#### Flow State Management

```python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class ArticleState(BaseModel):
    topic: str = ""
    research: str = ""
    draft: str = ""
    final: str = ""

class ArticleFlow(Flow[ArticleState]):

    @start()
    def set_topic(self):
        self.state.topic = "AI Ethics"
        return self.state.topic

    @listen(set_topic)
    def research(self, topic):
        # Research logic
        self.state.research = "Research findings..."
        return self.state.research

    @listen(research)
    def write_draft(self, research):
        self.state.draft = "Draft content..."
        return self.state.draft

# Access state
flow = ArticleFlow()
flow.kickoff()
print(flow.state.topic)
print(flow.state.research)
```

#### Router Pattern

```python
from crewai.flow.flow import Flow, listen, start, router

class ContentFlow(Flow):

    @start()
    def categorize_content(self):
        return "technical"  # or "marketing", "blog"

    @router(categorize_content)
    def route_content(self, category):
        if category == "technical":
            return "write_technical"
        elif category == "marketing":
            return "write_marketing"
        else:
            return "write_blog"

    @listen("write_technical")
    def write_technical_doc(self):
        return "Technical documentation..."

    @listen("write_marketing")
    def write_marketing_copy(self):
        return "Marketing content..."

    @listen("write_blog")
    def write_blog_post(self):
        return "Blog post..."
```

## Tools: Extending Agent Capabilities

### Built-in Tools

```python
from crewai_tools import (
    SerperDevTool,      # Google search
    ScrapeWebsiteTool,  # Web scraping
    FileReadTool,       # Read files
    DirectoryReadTool,  # Read directories
    CodeDocsSearchTool, # Search code documentation
    CSVSearchTool,      # Search CSV files
    JSONSearchTool,     # Search JSON files
    MDXSearchTool,      # Search MDX files
    PDFSearchTool,      # Search PDF files
    TXTSearchTool,      # Search text files
    WebsiteSearchTool,  # Search websites
    SeleniumScrapingTool, # Browser automation
    YoutubeChannelSearchTool, # YouTube search
    YoutubeVideoSearchTool   # YouTube video search
)

# Using tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
file_tool = FileReadTool()

agent = Agent(
    role='Researcher',
    tools=[search_tool, scrape_tool, file_tool]
)
```

### Custom Tools

```python
from crewai_tools import BaseTool

class MyCustomTool(BaseTool):
    name: str = "Custom Tool Name"
    description: str = "Clear description of what the tool does"

    def _run(self, argument: str) -> str:
        # Implementation
        result = perform_operation(argument)
        return result

# Using custom tool
custom_tool = MyCustomTool()
agent = Agent(
    role='Specialist',
    tools=[custom_tool]
)
```

### Function as Tool

```python
from crewai import Agent

def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers"""
    return a + b

agent = Agent(
    role='Calculator',
    tools=[calculate_sum]  # Pass function directly
)
```

## Memory: Learning from Past Interactions

```python
from crewai import Crew, Agent, Task

# Enable crew memory
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,  # Enable all memory types
    verbose=True
)

# Configure specific memory types
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,
    memory_config={
        'short_term': True,   # Remember within single run
        'long_term': True,    # Remember across runs
        'entity': True        # Remember entities (people, places)
    }
)
```

## Knowledge: RAG Integration

```python
from crewai import Agent, Crew, Task, knowledge

# Create knowledge source
docs_knowledge = knowledge.StringKnowledgeSource(
    content="Company policies and procedures...",
    metadata={"source": "policy_docs"}
)

# Using knowledge in agent
agent = Agent(
    role='Policy Expert',
    goal='Answer questions about company policies',
    backstory='Expert in company policies',
    knowledge_sources=[docs_knowledge]
)

# Load knowledge from files
pdf_knowledge = knowledge.PDFKnowledgeSource(
    file_path='./documents/handbook.pdf'
)

txt_knowledge = knowledge.TextKnowledgeSource(
    file_path='./documents/faq.txt'
)

agent = Agent(
    role='Support Agent',
    knowledge_sources=[pdf_knowledge, txt_knowledge]
)
```

## Structured Outputs with Pydantic

```python
from pydantic import BaseModel
from crewai import Task, Agent

class BlogPost(BaseModel):
    title: str
    content: str
    tags: list[str]
    word_count: int

# Task with structured output
write_task = Task(
    description='Write a blog post about AI',
    expected_output='Blog post with title, content, tags, and word count',
    agent=writer,
    output_pydantic=BlogPost
)

# Execute and get structured output
result = crew.kickoff()
blog_post: BlogPost = write_task.output.pydantic
print(blog_post.title)
print(blog_post.tags)
```

## Training: Improving Performance

```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2]
)

# Training loop
crew.train(
    n_iterations=10,
    inputs={'topic': 'AI'},
    filename='trained_crew.pkl'
)

# Load trained crew
trained_crew = Crew.load('trained_crew.pkl')
```

## Human-in-the-Loop

```python
from crewai import Task

# Task requiring human input
review_task = Task(
    description='Review the draft and provide feedback',
    expected_output='Approved draft or feedback for revision',
    agent=editor,
    human_input=True  # Will pause and ask for input
)

# Conditional human input
task = Task(
    description='Generate report',
    expected_output='Final report',
    agent=analyst,
    callback=lambda output: validate_output(output),
    human_input=True if needs_review else False
)
```

## Testing Crews

```python
from crewai import Crew
import pytest

def test_research_crew():
    # Setup
    crew = Crew(
        agents=[researcher],
        tasks=[research_task]
    )

    # Execute
    result = crew.kickoff(inputs={'topic': 'AI'})

    # Assert
    assert result is not None
    assert 'AI' in result
    assert len(result) > 100

def test_crew_with_mock():
    # Mock agent behavior for testing
    mock_agent = Agent(
        role='Mock Agent',
        goal='Return test data',
        backstory='Test agent'
    )

    mock_task = Task(
        description='Test task',
        expected_output='Test output',
        agent=mock_agent
    )

    crew = Crew(agents=[mock_agent], tasks=[mock_task])
    result = crew.kickoff()

    assert result == 'Test output'
```

## Custom LLMs

```python
from langchain_openai import ChatOpenAI
from crewai import Agent, Crew

# Using custom LLM
custom_llm = ChatOpenAI(
    model='gpt-4-turbo-preview',
    temperature=0.7,
    max_tokens=2000
)

agent = Agent(
    role='Writer',
    llm=custom_llm
)

# Crew-level LLM
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    manager_llm=custom_llm  # For hierarchical process
)
```

## Async Execution

```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2]
)

# Async kickoff
async def run_crew():
    result = await crew.kickoff_async(inputs={'topic': 'AI'})
    return result

# Kickoff for each (parallel execution)
inputs_list = [
    {'topic': 'AI'},
    {'topic': 'ML'},
    {'topic': 'Data Science'}
]

results = crew.kickoff_for_each(inputs=inputs_list)
```

## Callbacks and Event Listeners

```python
from crewai import Task, Agent

def on_task_complete(output):
    print(f"Task completed with output: {output}")
    # Log, notify, or process output

def on_task_error(error):
    print(f"Task failed with error: {error}")
    # Handle error, retry, or notify

task = Task(
    description='Analyze data',
    expected_output='Analysis report',
    agent=analyst,
    callback=on_task_complete
)

# Agent-level callbacks
agent = Agent(
    role='Analyst',
    step_callback=lambda step: print(f"Agent step: {step}"),
    task_callback=on_task_complete
)
```

## Enterprise Deployment

### Environment Configuration

```python
import os

# API keys
os.environ['OPENAI_API_KEY'] = 'your-key'
os.environ['SERPER_API_KEY'] = 'your-key'

# CrewAI+ (Enterprise)
os.environ['CREWAI_API_KEY'] = 'your-enterprise-key'

# Observability
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = 'your-langchain-key'
```

### Project Structure

```
my_crew_project/
├── src/
│   └── my_crew_project/
│       ├── __init__.py
│       ├── main.py
│       ├── crew.py
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── tools/
│           └── custom_tool.py
├── tests/
│   └── test_crew.py
├── pyproject.toml
└── README.md
```

### YAML Configuration

**agents.yaml**
```yaml
researcher:
  role: >
    Senior Research Analyst
  goal: >
    Uncover cutting-edge developments in {topic}
  backstory: >
    You are an expert researcher with deep knowledge in {topic}

writer:
  role: >
    Content Writer
  goal: >
    Create engaging content about {topic}
  backstory: >
    You are a skilled writer who makes complex topics accessible
```

**tasks.yaml**
```yaml
research_task:
  description: >
    Conduct comprehensive research on {topic}
  expected_output: >
    A detailed research report with key findings
  agent: researcher

writing_task:
  description: >
    Write an article based on the research
  expected_output: >
    A well-structured article
  agent: writer
  context:
    - research_task
```

## Best Practices

### Agent Design

✅ **Good Practices**:
- Give agents clear, specific roles
- Provide detailed backstories for context
- Limit tools to what's necessary
- Enable delegation for managers
- Use verbose mode during development

❌ **Avoid**:
- Vague or overlapping roles
- Too many tools (causes confusion)
- Missing backstories
- Overly complex goals

### Task Design

✅ **Good Practices**:
- Write clear, actionable descriptions
- Specify expected output format
- Set up proper task dependencies
- Use context for task chaining
- Enable human input for critical decisions

❌ **Avoid**:
- Ambiguous descriptions
- Missing expected output
- Circular dependencies
- Overly complex single tasks

### Crew Organization

✅ **Good Practices**:
- Start with sequential process
- Use hierarchical for complex coordination
- Enable memory for context retention
- Set reasonable rate limits
- Test with small datasets first

❌ **Avoid**:
- Too many agents (3-5 is optimal)
- Complex hierarchies without testing
- Disabled memory in multi-step flows
- No rate limiting

## Common Patterns

### Research and Write Pipeline

```python
# 1. Research agent gathers information
# 2. Analyst agent processes data
# 3. Writer agent creates content
# 4. Editor agent reviews and refines

researcher = Agent(role='Researcher', ...)
analyst = Agent(role='Analyst', ...)
writer = Agent(role='Writer', ...)
editor = Agent(role='Editor', ...)

research = Task(agent=researcher, ...)
analysis = Task(agent=analyst, context=[research], ...)
draft = Task(agent=writer, context=[analysis], ...)
final = Task(agent=editor, context=[draft], ...)

crew = Crew(
    agents=[researcher, analyst, writer, editor],
    tasks=[research, analysis, draft, final],
    process=Process.sequential
)
```

### Multi-Stage Approval Flow

```python
class ApprovalFlow(Flow):

    @start()
    def create_draft(self):
        # Generate initial draft
        return draft_content

    @listen(create_draft)
    def request_review(self, draft):
        # Send for review
        return review_request

    @router(request_review)
    def check_approval(self, review):
        if review.approved:
            return "finalize"
        else:
            return "revise"

    @listen("revise")
    def revise_draft(self):
        # Revise and loop back
        return revised_draft

    @listen("finalize")
    def finalize_content(self):
        return final_content
```

## Quick Reference

### Installation

```bash
# Using uv (recommended)
uv pip install crewai crewai-tools

# Using pip
pip install crewai crewai-tools

# With all extras
pip install 'crewai[all]'
```

### CLI Commands

```bash
# Create new project
crewai create crew my_project

# Create flow
crewai create flow my_flow

# Install dependencies
crewai install

# Run project
crewai run

# Train crew
crewai train

# Replay task
crewai replay <task_id>

# Test crew
crewai test
```

### Essential Imports

```python
from crewai import Agent, Task, Crew, Process
from crewai.flow.flow import Flow, listen, start, router
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel
```

## Resources

For advanced patterns, integration examples, and troubleshooting:
- Official Documentation: https://docs.crewai.com/
- API Reference: https://docs.crewai.com/api-reference
- GitHub: https://github.com/joaomdmoura/crewAI
- Community Forum: https://community.crewai.com/

### Extended Reference
See `references/advanced_patterns.md` for:
- MCP (Model Context Protocol) integration
- Observability and tracing setup
- Production deployment strategies
- Advanced flow patterns
- Performance optimization
