# Contributing to ClaudeSkills

Thank you for your interest in contributing to ClaudeSkills! This document provides guidelines for contributing to this repository.

English | [简体中文](./CONTRIBUTING.zh-CN.md)

## 🎯 How to Contribute

### Reporting Issues

- Use the GitHub issue tracker
- Describe the issue clearly
- Include examples if applicable
- Tag appropriately (bug, enhancement, question, etc.)

### Submitting Skills/Prompts

1. **Fork the repository**
2. **Create a new branch** for your contribution
3. **Add your skill/prompt** in the appropriate category
4. **Include documentation**:
   - Clear description
   - Use cases
   - Examples
   - Expected output
5. **Test your prompt** with Claude AI
6. **Submit a pull request**

## 📝 Skill/Prompt Format

### For Claude Skills (.skill files)

Claude Skills should follow this format:

```markdown
---
name: skill-name
description: Brief description of what this skill does. When to use it and what it helps with.
---

# Skill Name

## Overview
Detailed description of the skill's purpose and capabilities.

## Core Features
1. Feature 1
2. Feature 2
3. Feature 3

## Usage
How to use this skill with examples.

## Examples
Concrete examples of using the skill.

## References (Optional)
Additional reference materials in the `references/` subdirectory.
```

**Important Notes for Skills**:
- Skill name must use lowercase letters, numbers, and hyphens only
- No spaces or uppercase letters in the skill name
- Must start with YAML frontmatter (enclosed in `---`)
- Include comprehensive documentation
- Add reference materials in a `references/` subdirectory if needed

### For Prompt Templates

Each prompt template should include:

```markdown
# Prompt Name

## Description
Brief description of what this prompt does

## Category
- Primary: [category]
- Tags: [tag1, tag2, tag3]

## Prompt Template
\```
[Your prompt template here]
\```

## Example Usage
\```
[Example input]
\```

## Expected Output
\```
[Example output]
\```

## Tips
- Tip 1
- Tip 2

## Variations
- Variation 1
- Variation 2
```

## 🔍 Review Process

1. All submissions will be reviewed by maintainers
2. Feedback may be provided for improvements
3. Once approved, your contribution will be merged
4. You'll be added to the contributors list

## 📋 Guidelines

### Quality Standards

- **Clarity**: Prompts should be clear and unambiguous
- **Effectiveness**: Test prompts before submitting
- **Documentation**: Include comprehensive documentation
- **Examples**: Provide real-world examples
- **Formatting**: Follow the repository's formatting style

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow GitHub's community guidelines

## 🏷️ Categories

When adding content, place it in the appropriate category:

### Prompts
- `prompts/coding/` - Programming and development
- `prompts/writing/` - Content creation

### Skills
- `skills/` - Claude Skills (.skill files)
  - Each skill should be in its own subdirectory
  - Include a SKILL.md file with documentation
  - Add reference materials in a `references/` subdirectory if needed
  - Follow the naming convention: lowercase with hyphens

### Skill Categories
- **Development & Code Quality** - Code review, API development, frameworks
- **AI & Integration** - AI platform integrations, MCP servers
- **Document Processing** - Document creation and manipulation
- **Content Creation** - Article writing, podcast generation
- **Media & Audio** - Audio and media generation tools

## 🚀 Getting Started

1. Check existing issues and PRs to avoid duplicates
2. Discuss major changes in an issue first
3. Keep contributions focused and atomic
4. Write clear commit messages
5. Update documentation as needed

## 📞 Questions?

- Open an issue for questions
- Use GitHub Discussions for broader topics
- Tag maintainers if you need help

Thank you for contributing to ClaudeSkills! 🎉

