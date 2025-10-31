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
├── prompts/              # 按类别分类的提示词模板
│   ├── coding/          # 编程和开发
│   ├── writing/         # 内容创作和编辑
│   ├── analysis/        # 数据分析和研究
│   └── creative/        # 创意任务
├── skills/              # 高级技术和技能
├── integrations/        # 集成指南
└── docs/               # 附加文档
```

## 🎯 精选技能

### 1. 代码生成与审查
- 生成生产就绪的代码
- 执行全面的代码审查
- 调试和优化现有代码

### 2. 内容创作
- 撰写博客文章和文章
- 创建技术文档
- 生成营销文案

### 3. 数据分析
- 分析数据集并提取洞察
- 创建可视化和报告
- 执行统计分析

### 4. 研究与学习
- 总结研究论文
- 解释复杂概念
- 生成学习材料

## 💻 使用示例

### 示例 1: 代码审查提示词

```markdown
请审查以下代码:
1. 代码质量和最佳实践
2. 潜在的 bug 或安全问题
3. 性能优化
4. 改进建议

[你的代码]
```

### 示例 2: 技术写作

```markdown
创建一篇关于 [主题] 的技术博客文章:
- 为初学者清晰解释概念
- 包含实际示例
- 遵循 SEO 最佳实践
- 大约 1000 字
```

### 示例 3: API 集成

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "你的提示词"}
    ]
)

print(message.content)
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

- **🔧 开发** - 编码、调试、架构
- **✍️ 写作** - 内容创作、编辑、文案
- **📊 分析** - 数据分析、研究、洞察
- **🎨 创意** - 设计、头脑风暴、讲故事
- **🏢 商业** - 战略、规划、沟通
- **🎓 教育** - 教学、学习、辅导
- **🔬 研究** - 学术、科学、技术

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

*最后更新: 2024年10月*

