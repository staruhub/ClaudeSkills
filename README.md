# 🤖 ClaudeSkills

[![Run in Smithery](https://smithery.ai/badge/skills/staruhub)](https://smithery.ai/skills?ns=staruhub&utm_source=github&utm_medium=badge)


A curated collection of skills, prompts, and best practices for Claude AI by Anthropic.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![GitHub stars](https://img.shields.io/github/stars/staruhub/ClaudeSkills.svg?style=social&label=Star)](https://github.com/staruhub/ClaudeSkills)

English | [简体中文](./README.zh-CN.md)

## 📖 About

ClaudeSkills is a comprehensive repository designed to help developers, researchers, and AI enthusiasts maximize their productivity with Claude AI. This collection includes:

- 🎯 **Prompt Templates** - Ready-to-use prompts for common tasks
- 🛠️ **Skills & Techniques** - Advanced techniques for better results
- 📚 **Best Practices** - Guidelines for effective Claude interactions
- 💡 **Use Cases** - Real-world examples and applications
- 🔧 **Integration Guides** - How to integrate Claude into your workflow

## 🚀 Quick Start

### Prerequisites

- Access to Claude AI (via [Claude.ai](https://claude.ai) or Anthropic API)
- Basic understanding of prompt engineering
- (Optional) API key for programmatic access

### Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/staruhub/ClaudeSkills.git
   cd ClaudeSkills
   ```

2. **Browse the skills**
   - Navigate through different categories in the repository
   - Each skill includes detailed documentation and examples

3. **Try a skill**
   - Copy a prompt template
   - Customize it for your specific use case
   - Use it with Claude AI

## 📂 Repository Structure

```
ClaudeSkills/
├── prompts/                    # Prompt templates by category
│   ├── coding/                # Programming and development
│   └── writing/               # Content creation and editing
├── skills/                    # Claude Skills collection
│   ├── code-review/          # Code review expert skill
│   ├── coze-api/             # Coze API integration skill
│   ├── crewai-developer/     # CrewAI API skill
│   ├── document-skills/      # Anthropic official document skills
│   ├── flutter-api/          # Flutter API skill
│   ├── mcp-builder/          # MCP server builder skill (official)
│   ├── podcast/              # Podcast generator using Volcano Engine
│   └── wechat-article-writer/ # WeChat official account article writer
└── docs/                     # Additional documentation
```

## 🎯 Available Skills

### 1. 🔍 Code Review Expert
**Path**: `skills/code-review/`

A professional code review skill that helps you conduct comprehensive, high-quality code reviews based on 2025 best practices.

**Features**:
- Structured 3-step review process
- 8 comprehensive review dimensions (functionality, quality, security, performance, testing, documentation, architecture, maintainability)
- Priority-based feedback (🔴 Must Fix, 🟡 Strongly Recommended, 🟢 Suggested, 💡 Optional)
- Constructive feedback guidelines

### 2. 🤖 Coze API Integration
**Path**: `skills/coze-api/`

Complete guide for integrating with Coze (扣子) AI agent platform by ByteDance.

**Features**:
- Chat API for conversational interactions
- Workflow API for executing workflows
- Message management and status tracking
- Support for both streaming and non-streaming modes

### 3. 🚢 CrewAI Developer
**Path**: `skills/crewai-developer/`

Skill for building multi-agent AI systems using CrewAI framework.

**Features**:
- Multi-agent collaboration patterns
- Task orchestration and workflow management
- Agent role definition and configuration
- Integration with various AI models

### 4. 📄 Document Skills (Official)
**Path**: `skills/document-skills/`

Anthropic's official document processing skills for various formats.

**Features**:
- **DOCX**: Word document creation and manipulation
- **PDF**: PDF generation and form handling
- **PPTX**: PowerPoint presentation creation
- **XLSX**: Excel spreadsheet operations

### 5. 📱 Flutter API
**Path**: `skills/flutter-api/`

Comprehensive Flutter development skill with API references.

**Features**:
- Flutter widget and API documentation
- Best practices for Flutter development
- Cross-platform mobile app development guidance
- State management patterns

### 6. 🔧 MCP Builder (Official)
**Path**: `skills/mcp-builder/`

Official skill for building high-quality Model Context Protocol (MCP) servers.

**Features**:
- Agent-centric design principles
- Support for Python (FastMCP) and Node.js/TypeScript
- Best practices for tool design
- Comprehensive evaluation guidelines

### 7. 🎙️ Podcast Generator
**Path**: `skills/podcast/`

Generate AI podcasts using Volcano Engine's podcast model.

**Features**:
- Dual-speaker dialogue generation
- Multiple audio formats (MP3, OGG, PCM, AAC)
- Adjustable speech rate and voice
- Streaming audio reception
- Resume from breakpoint support

### 8. ✍️ WeChat Article Writer
**Path**: `skills/wechat-article-writer/`

Professional WeChat official account article creation assistant.

**Features**:
- Convert web content, text, or images into WeChat articles
- Official copywriting style optimization
- Title optimization with proven formulas
- Content enrichment using search tools
- Quality checklist and style guide

## 💻 Usage Examples

### Example 1: Using Code Review Skill

Simply upload your code or paste it in the conversation:

```
Please review this code for security issues and performance optimizations.

[Your code here]
```

The skill will automatically provide structured feedback with priority levels.

### Example 2: Generating a Podcast

```
Generate a podcast about "The Future of AI" and save it as podcast.mp3
```

The podcast skill will create a dual-speaker dialogue in Chinese using Volcano Engine.

### Example 3: Creating WeChat Articles

```
Convert this blog post into a WeChat official account article:
[Paste URL or content]

Target audience: Tech professionals
Style: Professional and informative
```

### Example 4: Building an MCP Server

```
I want to build an MCP server for GitHub API integration.
Help me design the tools following best practices.
```

### Example 5: Coze API Integration

```python
import requests

url = "https://api.coze.cn/v3/chat"
headers = {
    "Authorization": "Bearer YOUR_PAT_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "bot_id": "your_bot_id",
    "user_id": "user_123",
    "stream": False,
    "auto_save_history": True,
    "additional_messages": [
        {
            "role": "user",
            "content": "Hello!",
            "content_type": "text"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingSkill`)
3. **Commit your changes** (`git commit -m 'Add some AmazingSkill'`)
4. **Push to the branch** (`git push origin feature/AmazingSkill`)
5. **Open a Pull Request**

### Contribution Guidelines

- Ensure your skill/prompt is well-documented
- Include examples and use cases
- Test your prompts before submitting
- Follow the existing structure and formatting
- Add appropriate tags and categories

## 📋 Skill Categories

Our skills are organized into the following categories:

- **🔧 Development & Code Quality**
  - Code Review Expert
  - Flutter API
  - CrewAI Developer

- **🤖 AI & Integration**
  - Coze API Integration
  - MCP Builder (Official)

- **📄 Document Processing**
  - Document Skills (DOCX, PDF, PPTX, XLSX)

- **✍️ Content Creation**
  - WeChat Article Writer
  - Podcast Generator

- **🎙️ Media & Audio**
  - Podcast Generator (Volcano Engine)

## 🌟 Best Practices

1. **Be Specific** - Provide clear context and requirements
2. **Use Examples** - Show Claude what you want with examples
3. **Iterate** - Refine your prompts based on results
4. **Structure** - Use clear formatting and organization
5. **Context** - Provide relevant background information
6. **Constraints** - Specify limitations and requirements

## 📚 Resources

- [Claude AI Official Documentation](https://docs.anthropic.com/)
- [Anthropic API Reference](https://docs.anthropic.com/claude/reference)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 🔗 Related Projects

- [Awesome Claude](https://github.com/topics/claude-ai) - Curated list of Claude resources
- [LangChain](https://github.com/langchain-ai/langchain) - Framework for LLM applications
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) - Official examples

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to Anthropic for creating Claude AI
- Contributors who share their skills and prompts
- The AI community for continuous innovation

## 📞 Contact

- **GitHub Issues** - For bug reports and feature requests
- **Discussions** - For questions and community chat
- **Twitter** - [@staruhub](https://twitter.com/staruhub) (if applicable)

## ⭐ Star History

If you find this repository helpful, please consider giving it a star! ⭐

---

**Made with ❤️ by the Claude community**

*Last updated: October 31, 2024*

