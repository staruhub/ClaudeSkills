---
name: Geek-skills-security-audit
version: 1.0.0
description: 全面的代码安全检查和服务器安全审计skill。适用于：(1) 代码漏洞扫描 - 检测SQL注入、XSS、SSRF等OWASP Top 10漏洞，(2) 依赖安全检查 - 识别过时或有漏洞的第三方库（如React2Shell CVE-2025-55182、Next.js CVE-2025-66478），(3) 服务器配置审计 - 检查SSH、防火墙、权限等安全配置，(4) 敏感信息泄露检测 - API密钥、密码、令牌等硬编码检测，(5) 容器安全扫描 - Docker镜像和Kubernetes配置审计，(6) CI/CD安全检查。触发关键词："安全检查"、"漏洞扫描"、"代码审计"、"security audit"、"vulnerability scan"、"penetration test"、"SAST"、"DAST"、"dependency check"、"CVE检测"等。
---

# Security Audit Skill

全面的安全审计工具，覆盖代码静态分析(SAST)、动态测试(DAST)、依赖检查(SCA)和服务器配置审计。

## 工作流程

安全审计遵循以下步骤：

1. **环境检测** → 识别项目类型和技术栈
2. **依赖检查** → 扫描第三方库漏洞（优先级最高）
3. **静态代码分析** → SAST扫描源代码漏洞
4. **敏感信息检测** → 扫描硬编码的密钥和凭证
5. **配置审计** → 检查安全相关配置
6. **生成报告** → 汇总发现并提供修复建议

## 快速开始

### 依赖安装

```bash
# 安装核心Python扫描工具
pip install safety bandit semgrep pip-audit --break-system-packages

# 安装Node.js安全工具（如需要）
npm install -g npm-audit-html retire
```

### 一键全面扫描

运行综合扫描脚本：
```bash
python3 /path/to/skill/scripts/full_scan.py /path/to/project
```

## 检测能力

### 1. 高危漏洞（Critical）

| 漏洞类型 | CVE示例 | 检测方式 |
|---------|--------|---------|
| React2Shell RCE | CVE-2025-55182 | 依赖版本检查 |
| Next.js RCE | CVE-2025-66478 | 依赖版本检查 |
| Log4Shell | CVE-2021-44228 | 依赖版本检查 |
| SQL注入 | CWE-89 | SAST + 模式匹配 |
| 命令注入 | CWE-78 | SAST + 模式匹配 |

### 2. OWASP Top 10 2024

- **A01**: Broken Access Control - 访问控制缺陷
- **A02**: Cryptographic Failures - 加密失败
- **A03**: Injection - 注入攻击（SQL/XSS/Command）
- **A04**: Insecure Design - 不安全设计
- **A05**: Security Misconfiguration - 安全配置错误
- **A06**: Vulnerable Components - 易受攻击的组件
- **A07**: Authentication Failures - 身份认证失败
- **A08**: Software Integrity Failures - 软件完整性失败
- **A09**: Logging Failures - 日志记录失败
- **A10**: SSRF - 服务端请求伪造

## 扫描工具使用

### Python项目

```bash
# Bandit - Python SAST
bandit -r ./src -f json -o bandit_report.json

# Safety - 依赖漏洞检查
safety check --json > safety_report.json

# pip-audit - 依赖审计
pip-audit --format json > pip_audit.json
```

### JavaScript/Node.js项目

```bash
# npm audit - 依赖漏洞
npm audit --json > npm_audit.json

# Retire.js - 检测过时库
retire --js --outputformat json > retire_report.json

# React/Next.js 特别检查（CVE-2025-55182）
npx fix-react2shell-next --check-only
```

### 通用检测

```bash
# Semgrep - 多语言SAST
semgrep scan --config=auto --json > semgrep_report.json

# Gitleaks - 密钥泄露检测
gitleaks detect --source . --report-format json --report-path gitleaks.json

# Trivy - 容器/依赖扫描
trivy fs --format json --output trivy.json .
```

## 服务器安全检查

### SSH配置审计
```bash
# 检查SSH配置
grep -E "^(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)" /etc/ssh/sshd_config
```

### 防火墙状态
```bash
# UFW状态
sudo ufw status verbose

# iptables规则
sudo iptables -L -n -v
```

### 权限检查
```bash
# 查找SUID文件
find / -perm -4000 -type f 2>/dev/null

# 检查world-writable文件
find / -perm -002 -type f 2>/dev/null
```

## 修复建议

### React2Shell漏洞修复（CVE-2025-55182）

**受影响版本**:
- React 19.0, 19.1.0, 19.1.1, 19.2.0
- Next.js ≥14.3.0-canary.77, ≥15, ≥16

**修复步骤**:
```bash
# 使用官方修复工具
npx fix-react2shell-next

# 或手动升级
# Next.js 15.x -> 升级到 15.1.4+
# Next.js 14.x -> 降级到稳定14.x版本
```

**修复后必做**:
- 轮换所有应用密钥（特别是2024年12月4日后暴露的）
- 检查是否有异常进程或网络连接

### 常见漏洞修复参考

详见 `references/remediation_guide.md`

## 报告格式

扫描完成后生成的报告包含：

```
security_report/
├── summary.md           # 执行摘要
├── critical.json        # 高危漏洞
├── dependencies.json    # 依赖漏洞
├── code_issues.json     # 代码问题
├── secrets.json         # 泄露的密钥
└── recommendations.md   # 修复建议
```

## 最佳实践

1. **每次提交前**运行快速扫描
2. **每日**运行依赖漏洞检查
3. **每周**运行完整安全审计
4. 将扫描集成到 **CI/CD** 流水线
5. 订阅安全公告（如CVE、NVD）
6. 定期更新扫描工具和规则库

## 参考资料

- 详细漏洞检测规则: `references/detection_rules.md`
- 修复指南: `references/remediation_guide.md`
- 服务器加固: `references/server_hardening.md`
