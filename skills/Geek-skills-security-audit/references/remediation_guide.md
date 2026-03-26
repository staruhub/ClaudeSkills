# 漏洞修复指南

## 紧急漏洞修复流程

### 1. React2Shell (CVE-2025-55182) 修复

**紧急程度**: 🔴 Critical - 立即修复

**步骤一：确认受影响**
```bash
# 检查React版本
npm ls react | grep -E "19\.(0|1\.[01]|2\.0)"

# 检查Next.js版本
npm ls next | grep -E "(14\.3\.0-canary|15\.|16\.)"

# 使用官方检测工具
npx fix-react2shell-next --check-only
```

**步骤二：升级到安全版本**
```bash
# Next.js 15.x 用户
npm install next@15.1.4

# Next.js 14.x 用户（降级到稳定版）
npm install next@14.2.21

# React 用户
npm install react@19.1.0-rc.1 react-dom@19.1.0-rc.1
```

**步骤三：轮换密钥**
```bash
# 列出所有环境变量
grep -r "API_KEY\|SECRET\|PASSWORD\|TOKEN" .env*

# 重新生成数据库凭证
# 重新生成API密钥
# 更新OAuth客户端密钥
# 轮换JWT签名密钥
```

**步骤四：检查入侵痕迹**
```bash
# 检查可疑进程
ps aux | grep -E "(sex\.sh|slt|wget|curl)" 

# 检查网络连接
netstat -an | grep ESTABLISHED

# 检查定时任务
crontab -l
cat /etc/crontab

# 检查最近修改的文件
find /var/www -mtime -7 -type f
```

---

## OWASP Top 10 修复指南

### A01: Broken Access Control

**问题示例**:
```python
# 危险：直接使用用户输入
@app.route('/user/<id>')
def get_user(id):
    return User.query.get(id)
```

**修复方案**:
```python
# 安全：验证用户权限
@app.route('/user/<id>')
@login_required
def get_user(id):
    user = User.query.get(id)
    if user.id != current_user.id and not current_user.is_admin:
        abort(403)
    return user
```

**最佳实践**:
- 默认拒绝所有访问
- 实施RBAC（基于角色的访问控制）
- 记录所有访问控制失败
- 禁用目录列表
- 限制API和控制器访问速率

### A02: Cryptographic Failures

**危险配置**:
```python
# 危险：使用MD5存储密码
password_hash = hashlib.md5(password.encode()).hexdigest()

# 危险：硬编码密钥
SECRET_KEY = "hardcoded_secret_key"
```

**修复方案**:
```python
# 安全：使用bcrypt或argon2
from argon2 import PasswordHasher
ph = PasswordHasher()
password_hash = ph.hash(password)

# 安全：从环境变量读取
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
```

**最佳实践**:
- 使用TLS 1.2+传输数据
- 使用强加密算法（AES-256, RSA-2048+）
- 使用安全的密码哈希（Argon2, bcrypt, scrypt）
- 不存储明文敏感数据
- 使用安全的随机数生成器

### A03: Injection

**SQL注入修复**:
```python
# 危险
query = f"SELECT * FROM users WHERE name = '{name}'"

# 安全：使用参数化查询
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))

# 安全：使用ORM
User.query.filter_by(name=name).first()
```

**命令注入修复**:
```python
# 危险
os.system(f"ping {host}")

# 安全：使用subprocess列表形式
import subprocess
subprocess.run(["ping", "-c", "4", host], capture_output=True)
```

**XSS修复**:
```javascript
// 危险
element.innerHTML = userInput;

// 安全
element.textContent = userInput;

// 如果必须使用HTML，进行转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

### A04: Insecure Design

**设计原则**:
- 威胁建模：识别潜在攻击者和攻击向量
- 安全设计模式：使用经过验证的安全架构
- 安全控制库：使用成熟的安全组件
- 分层验证：不信任任何输入

**检查清单**:
- [ ] 业务逻辑是否有滥用风险？
- [ ] 敏感操作是否有速率限制？
- [ ] 是否实现了深度防御？
- [ ] 是否有安全测试用例？

### A05: Security Misconfiguration

**常见问题修复**:

```nginx
# Nginx安全配置
server {
    # 禁用服务器版本号
    server_tokens off;
    
    # 安全头
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
    add_header Content-Security-Policy "default-src 'self'";
    
    # 禁用不需要的HTTP方法
    if ($request_method !~ ^(GET|POST|HEAD)$) {
        return 405;
    }
}
```

```yaml
# Docker安全配置
services:
  app:
    security_opt:
      - no-new-privileges:true
    read_only: true
    user: "1000:1000"
    cap_drop:
      - ALL
```

### A06: Vulnerable and Outdated Components

**依赖更新流程**:
```bash
# Python
pip list --outdated
pip-audit
safety check

# Node.js
npm audit
npm outdated
npx npm-check-updates

# 自动更新补丁版本
npm update
pip install --upgrade -r requirements.txt
```

**依赖管理策略**:
- 使用锁文件（package-lock.json, requirements.txt）
- 定期运行安全扫描
- 订阅安全公告
- 使用Dependabot或Renovate自动更新

### A07: Authentication Failures

**安全认证实现**:
```python
# 密码策略
import re
def validate_password(password):
    if len(password) < 12:
        return False, "密码至少12个字符"
    if not re.search(r'[A-Z]', password):
        return False, "需要大写字母"
    if not re.search(r'[a-z]', password):
        return False, "需要小写字母"
    if not re.search(r'\d', password):
        return False, "需要数字"
    if not re.search(r'[!@#$%^&*]', password):
        return False, "需要特殊字符"
    return True, "密码有效"

# 登录限速
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["5 per minute"])

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # 登录逻辑
    pass
```

### A08: Software and Data Integrity Failures

**CI/CD安全**:
```yaml
# GitHub Actions安全配置
name: Secure Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - name: Verify dependencies
        run: npm audit --audit-level=high
      - name: SAST scan
        run: semgrep scan --config=auto
```

**依赖验证**:
```bash
# 验证npm包完整性
npm ci --ignore-scripts

# 验证Python包
pip install --require-hashes -r requirements.txt
```

### A09: Security Logging and Monitoring Failures

**日志配置**:
```python
import logging
from datetime import datetime

# 配置安全日志
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

handler = logging.FileHandler('security.log')
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s - IP: %(ip)s - User: %(user)s'
)
handler.setFormatter(formatter)
security_logger.addHandler(handler)

# 记录安全事件
def log_security_event(event_type, message, request):
    extra = {
        'ip': request.remote_addr,
        'user': getattr(request, 'user', 'anonymous')
    }
    security_logger.info(f"{event_type}: {message}", extra=extra)

# 记录登录失败
log_security_event('LOGIN_FAILED', 'Invalid credentials', request)
```

**应该记录的事件**:
- 登录成功/失败
- 权限提升
- 敏感数据访问
- 配置变更
- 异常和错误

### A10: Server-Side Request Forgery (SSRF)

**SSRF防护**:
```python
import ipaddress
from urllib.parse import urlparse
import socket

def is_safe_url(url):
    """验证URL是否安全"""
    try:
        parsed = urlparse(url)
        
        # 只允许http/https
        if parsed.scheme not in ('http', 'https'):
            return False
        
        # 解析主机名
        hostname = parsed.hostname
        if not hostname:
            return False
        
        # 获取IP地址
        ip = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip)
        
        # 禁止私有IP
        if ip_obj.is_private:
            return False
        
        # 禁止环回地址
        if ip_obj.is_loopback:
            return False
        
        # 禁止链接本地地址
        if ip_obj.is_link_local:
            return False
        
        # 禁止AWS元数据端点
        if ip == '169.254.169.254':
            return False
        
        return True
    except Exception:
        return False

# 使用示例
if is_safe_url(user_url):
    response = requests.get(user_url)
else:
    raise ValueError("URL不安全")
```

---

## 快速修复清单

### 紧急修复（立即执行）

- [ ] 更新React/Next.js到安全版本
- [ ] 轮换所有泄露的密钥
- [ ] 禁用DEBUG模式
- [ ] 更新所有高危依赖

### 短期修复（24-48小时）

- [ ] 实施输入验证
- [ ] 添加CSRF保护
- [ ] 配置安全HTTP头
- [ ] 启用日志记录

### 中期修复（1-2周）

- [ ] 实施RBAC
- [ ] 添加速率限制
- [ ] 配置WAF
- [ ] 安全代码审查

### 长期改进（持续）

- [ ] CI/CD集成安全扫描
- [ ] 定期渗透测试
- [ ] 安全培训
- [ ] 建立漏洞披露流程
