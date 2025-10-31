# 🤖 ClaudeSkills

Claude AI 技能、提示词和最佳实践精选集合

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![GitHub stars](https://img.shields.io/github/stars/staruhub/ClaudeSkills.svg?style=social&label=Star)](https://github.com/staruhub/ClaudeSkills)

[English](./README.md) | 简体中文

## 📖 关于本项目

ClaudeSkills 是一个综合性仓库,旨在帮助开发者、研究人员和 AI 爱好者最大化 Claude AI 的生产力。本集合包括:

- 🎯 **提示词模板** - 常见任务的即用型提示词
- 🛠️ **技能与技巧** - 获得更好结果的高级技术
- 📚 **最佳实践** - 有效使用 Claude 的指南
- 💡 **使用案例** - 真实世界的示例和应用
- 🔧 **集成指南** - 如何将 Claude 集成到你的工作流程

## 🚀 快速开始

### 前置要求

- 访问 Claude AI（通过 [Claude.ai](https://claude.ai) 或 Anthropic API）
- 基本的提示词工程理解
- （可选）用于编程访问的 API 密钥

### 开始使用

1. **克隆仓库**
   ```bash
   git clone https://github.com/staruhub/ClaudeSkills.git
   cd ClaudeSkills
   ```

2. **浏览技能**
   - 浏览仓库中的不同类别
   - 每个技能都包含详细的文档和示例

3. **尝试一个技能**
   - 复制提示词模板
   - 根据你的具体用例进行自定义
   - 在 Claude AI 中使用

## 📂 仓库结构

```
ClaudeSkills/
├── prompts/                    # 按类别分类的提示词模板
│   ├── coding/                # 编程和开发
│   └── writing/               # 内容创作和编辑
├── skills/                    # Claude 技能集合
│   ├── code-review/          # 代码审查专家技能
│   ├── coze-api/             # Coze API 集成技能
│   ├── crewai-developer/     # CrewAI API 技能
│   ├── document-skills/      # Anthropic 官方文档技能
│   ├── flutter-api/          # Flutter API 技能
│   ├── mcp-builder/          # MCP 服务器构建器技能(官方)
│   ├── podcast/              # 播客生成器(使用火山引擎)
│   └── wechat-article-writer/ # 微信公众号文章写作助手
└── docs/                     # 附加文档
```

## 🎯 可用技能

### 1. 🔍 代码审查专家
**路径**: `skills/code-review/`

基于 2025 年最佳实践的专业代码审查技能,帮助你进行全面、高质量的代码审查。

**功能特点**:
- 结构化的三步审查流程
- 8 大审查维度(功能、质量、安全、性能、测试、文档、架构、可维护性)
- 优先级反馈(🔴 必须修复、🟡 强烈建议、🟢 建议、💡 可选)
- 建设性反馈指南

### 2. 🤖 Coze API 集成
**路径**: `skills/coze-api/`

字节跳动扣子(Coze) AI 智能体平台的完整集成指南。

**功能特点**:
- 对话 API 进行会话交互
- 工作流 API 执行工作流
- 消息管理和状态跟踪
- 支持流式和非流式模式

### 3. 🚢 CrewAI 开发者
**路径**: `skills/crewai-developer/`

使用 CrewAI 框架构建多智能体 AI 系统的技能。

**功能特点**:
- 多智能体协作模式
- 任务编排和工作流管理
- 智能体角色定义和配置
- 与各种 AI 模型集成

### 4. 📄 文档技能(官方)
**路径**: `skills/document-skills/`

Anthropic 官方的文档处理技能,支持多种格式。

**功能特点**:
- **DOCX**: Word 文档创建和操作
- **PDF**: PDF 生成和表单处理
- **PPTX**: PowerPoint 演示文稿创建
- **XLSX**: Excel 电子表格操作

### 5. 📱 Flutter API
**路径**: `skills/flutter-api/`

包含 API 参考的综合 Flutter 开发技能。

**功能特点**:
- Flutter 组件和 API 文档
- Flutter 开发最佳实践
- 跨平台移动应用开发指导
- 状态管理模式

### 6. 🔧 MCP 构建器(官方)
**路径**: `skills/mcp-builder/`

构建高质量模型上下文协议(MCP)服务器的官方技能。

**功能特点**:
- 以智能体为中心的设计原则
- 支持 Python (FastMCP) 和 Node.js/TypeScript
- 工具设计最佳实践
- 全面的评估指南

### 7. 🎙️ 播客生成器
**路径**: `skills/podcast/`

使用火山引擎的播客模型生成 AI 播客。

**功能特点**:
- 双人对话生成
- 多种音频格式(MP3、OGG、PCM、AAC)
- 可调节语速和音色
- 流式音频接收
- 断点续传支持

### 8. ✍️ 微信文章写作助手
**路径**: `skills/wechat-article-writer/`

专业的微信公众号文章创作助手。

**功能特点**:
- 将网页内容、文本或图像转换为微信文章
- 官方文案风格优化
- 使用经过验证的公式优化标题
- 使用搜索工具丰富内容
- 质量检查清单和风格指南

## 💻 使用示例

### 示例 1: 使用代码审查技能

只需上传代码或在对话中粘贴:

```
请审查这段代码的安全问题和性能优化。

[你的代码]
```

技能会自动提供带有优先级的结构化反馈。

### 示例 2: 生成播客

```
生成一个关于"人工智能的未来"的播客,保存为 podcast.mp3
```

播客技能将使用火山引擎创建中文双人对话。

### 示例 3: 创建微信文章

```
将这篇博客文章转换为微信公众号文章:
[粘贴 URL 或内容]

目标受众: 科技专业人士
风格: 专业且信息丰富
```

### 示例 4: 构建 MCP 服务器

```
我想构建一个 GitHub API 集成的 MCP 服务器。
请帮我按照最佳实践设计工具。
```

### 示例 5: Coze API 集成

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
            "content": "你好!",
            "content_type": "text"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 🤝 贡献

我们欢迎社区贡献!以下是你可以帮助的方式:

1. **Fork 仓库**
2. **创建功能分支** (`git checkout -b feature/AmazingSkill`)
3. **提交你的更改** (`git commit -m 'Add some AmazingSkill'`)
4. **推送到分支** (`git push origin feature/AmazingSkill`)
5. **开启 Pull Request**

### 贡献指南

- 确保你的技能/提示词有良好的文档
- 包含示例和使用案例
- 提交前测试你的提示词
- 遵循现有的结构和格式
- 添加适当的标签和类别

## 📋 技能分类

我们的技能按以下类别组织:

- **🔧 开发与代码质量**
  - 代码审查专家
  - Flutter API
  - CrewAI 开发者

- **🤖 AI 与集成**
  - Coze API 集成
  - MCP 构建器(官方)

- **📄 文档处理**
  - 文档技能(DOCX、PDF、PPTX、XLSX)

- **✍️ 内容创作**
  - 微信文章写作助手
  - 播客生成器

- **🎙️ 媒体与音频**
  - 播客生成器(火山引擎)

## 🌟 最佳实践

1. **具体明确** - 提供清晰的上下文和要求
2. **使用示例** - 用示例向 Claude 展示你想要什么
3. **迭代优化** - 根据结果改进你的提示词
4. **结构化** - 使用清晰的格式和组织
5. **提供上下文** - 提供相关的背景信息
6. **设定约束** - 指定限制和要求

## 📚 资源

- [Claude AI 官方文档](https://docs.anthropic.com/)
- [Anthropic API 参考](https://docs.anthropic.com/claude/reference)
- [提示词工程指南](https://www.promptingguide.ai/)
- [模型上下文协议](https://modelcontextprotocol.io/)

## 🔗 相关项目

- [Awesome Claude](https://github.com/topics/claude-ai) - Claude 资源精选列表
- [LangChain](https://github.com/langchain-ai/langchain) - LLM 应用框架
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) - 官方示例

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 感谢 Anthropic 创建了 Claude AI
- 感谢分享技能和提示词的贡献者
- 感谢 AI 社区的持续创新

## 📞 联系方式

- **GitHub Issues** - 用于 bug 报告和功能请求
- **Discussions** - 用于问题和社区讨论
- **Twitter** - [@staruhub](https://twitter.com/staruhub)（如适用）

## ⭐ Star 历史

如果你觉得这个仓库有帮助,请考虑给它一个 star! ⭐

---

**由 Claude 社区用 ❤️ 制作**

*最后更新: 2024年10月31日*

