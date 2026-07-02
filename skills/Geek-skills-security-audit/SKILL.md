---
name: security-audit
version: 1.1.0
description: 全面的代码安全检查和服务器安全审计skill。适用于：(1) 代码漏洞扫描 - 检测SQL注入、XSS、SSRF等OWASP Top 10漏洞，(2) 依赖安全检查 - 识别过时或有漏洞的第三方库，结合实时搜索确认最新CVE，(3) 服务器配置审计 - 检查SSH、防火墙、权限等安全配置，(4) 敏感信息泄露检测 - API密钥、密码、令牌等硬编码检测，(5) 容器安全扫描 - Docker镜像和Kubernetes配置审计，(6) CI/CD安全检查。触发关键词："安全检查"、"漏洞扫描"、"代码审计"、"security audit"、"vulnerability scan"、"SAST"、"dependency check"、"CVE检测"等。不用于：修复单个已定位的bug、编写新的安全功能代码、对无授权的第三方系统做扫描或渗透测试。
---

# Security Audit Skill

全面的安全审计工具，覆盖代码静态分析(SAST)、依赖检查(SCA)和服务器配置审计。

## 授权与边界（先确认再动手）

- 只审计用户拥有或明确获得授权的代码/服务器；对第三方系统的扫描请求一律拒绝并说明原因
- 本skill做**审计与建议**，不做主动攻击性测试（漏洞利用、爆破、DoS验证）
- 发现硬编码凭证时只报告**位置与类型**，不在输出中回显完整明文
- 除非用户明确要求，不直接修改业务代码；修复以建议形式给出

## 时效性规则（重要）

本文件**不维护具体CVE清单**。凡涉及"某版本是否有漏洞"的结论，必须现场查询：
用 web search 查 `[框架/库名] CVE advisory [当前年份]`，或查官方 security advisory 页面。
正文中出现的具体CVE（如 Log4Shell CVE-2021-44228）仅作为漏洞**类别**的历史案例，不代表当前威胁全貌。

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
# 安装核心Python扫描工具（优先用 venv/pipx，避免污染系统 Python）
pipx install bandit semgrep || pip install safety bandit semgrep pip-audit

# 安装Node.js安全工具（如需要）
npm install -g npm-audit-html retire
```

### 一键全面扫描

运行综合扫描脚本：
```bash
python3 /path/to/skill/scripts/full_scan.py /path/to/project
```

只需单项检查时用独立脚本：`scripts/dependency_check.py`（仅依赖漏洞）、`scripts/secrets_scan.py`（仅敏感信息/密钥，输出已对命中值脱敏）。

注意：`dependency_check.py` 内置的是**离线基线表**（会过时），命中结果标注 `source: offline-baseline`，必须用 pip-audit/npm audit 或官方 advisory 实时确认后才能下结论——与上文"不维护 CVE 清单"原则一致，基线表是预筛工具而非权威来源。

## 检测能力

### 1. 高危漏洞（Critical）

| 漏洞类型 | 历史案例 | 检测方式 |
|---------|--------|---------|
| 框架/依赖 RCE | Log4Shell (CVE-2021-44228) | 依赖版本检查 + 现场搜索最新 advisory |
| SQL注入 | CWE-89 | SAST + 模式匹配 |
| 命令注入 | CWE-78 | SAST + 模式匹配 |

框架级 RCE 层出不穷（React/Next.js 等生态近年多次爆出），检查依赖前先 web search 该框架当年的 CVE 列表。

### 2. OWASP Top 10（以官方当前版本为准）

> 运行时先 web search 确认当前版本（现行为 2025 版）；无法联网时使用下面这份记录时点的离线清单，并在报告中标注可能过时。以下条目为通用类别参考：

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
```

框架专项检查：先 web search 确认该框架当前的高危 CVE 及官方检测工具，再执行（历史案例见 `references/remediation_guide.md`）。

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

### 依赖类漏洞的通用修复流程

1. **查官方 advisory**：确认受影响版本范围和官方推荐的修复路径（升级/降级/补丁工具），不要依赖任何写死在文档里的版本号
2. **执行修复**：优先用官方修复工具，其次手动升级到 advisory 指明的安全版本
3. **修复后必做**（RCE 类漏洞尤其不能跳过）：
   - 轮换所有可能暴露的应用密钥
   - 检查是否有异常进程或网络连接（入侵痕迹排查）
4. **回归验证**：重跑依赖扫描确认漏洞消除

具体漏洞的修复命令和历史案例（含 React2Shell 完整处置记录）详见 `references/remediation_guide.md`。

## 报告格式

`full_scan.py` 在 `security_report/` 下生成：

```
security_report/
├── summary.md            # 执行摘要 + 覆盖范围声明（工具缺失时列出缩窄项）
└── security_report.json  # 结构化发现，按 critical/high/medium/low/info 分级 + skipped_tools
```

`secrets_scan.py` 另行生成 `secrets_report.{json,md}`（命中值已脱敏）。
汇总多来源发现、按严重性分文件时，从 `security_report.json` 的分级结构派生即可，不必依赖固定的六文件布局。

## 验收标准（完成前逐条自查）

- [ ] 报告含 summary.md（带覆盖范围声明）与结构化 JSON；缺失的扫描器已在报告中列出
- [ ] 每个 Critical/High 发现都有：证据位置（文件+行号或配置项）+ 影响说明 + 可执行的修复建议
- [ ] 依赖漏洞结论基于**本次运行**的扫描或搜索结果，未引用过时的内置CVE知识
- [ ] 未给出"已确认安全"式结论——只报告"在已执行的检查范围内未发现"，并列出未覆盖项
- [ ] 泄露凭证只报告位置与类型，输出中无完整明文

## 已知陷阱

| 陷阱 | 具体表现 | 应对 |
|------|---------|------|
| 扫描工具缺失时静默跳过 | 环境装不上 bandit/semgrep，直接不扫也不说明 | 降级为 grep 模式匹配，并在报告中**明确声明覆盖范围缩窄** |
| 把"扫描通过"当"安全" | 工具零报告就写"系统安全" | 工具只覆盖已知模式；结论必须限定范围并列出未检查项 |
| `--break-system-packages` 污染环境 | 全局 pip 安装扫描工具破坏系统 Python | 优先用 venv 或 pipx；用户环境受限时先征求同意 |
| 误报未过滤直接进报告 | SAST 把测试夹具、示例代码报为漏洞 | 每条 Critical 人工复核上下文，误报标注原因后移出 critical 列表 |

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
- 触发边界回归用例: `evals/routing-evals.json`（改动本 skill 的 description 后应重跑）
