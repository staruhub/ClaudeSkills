# 漏洞检测规则参考

## 高危漏洞检测模式

### 1. React2Shell (CVE-2025-55182)

**漏洞描述**: React Server Components (RSC) Flight协议中的不安全反序列化漏洞，允许未经身份验证的远程代码执行。

**CVSS评分**: 10.0 (Critical)

**受影响组件**:
```
react-server-dom-parcel: 19.0.0, 19.1.0, 19.1.1, 19.2.0
react-server-dom-webpack: 19.0.0, 19.1.0, 19.1.1, 19.2.0
react-server-dom-turbopack: 19.0.0, 19.1.0, 19.1.1, 19.2.0
```

**检测方法**:
```bash
# 检查package.json中的React版本
grep -E '"react":|"next":' package.json

# 检查package-lock.json
grep -E 'react-server-dom' package-lock.json
```

**正则模式**:
```regex
"react":\s*"19\.(0|1\.[01]|2\.0)"
"next":\s*"(14\.3\.0-canary|15\.|16\.)"
```

### 2. SQL注入 (CWE-89)

**危险模式**:
```python
# Python - 字符串拼接SQL
cursor.execute("SELECT * FROM users WHERE id = " + user_id)
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)

# 安全写法
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
cursor.execute("SELECT * FROM users WHERE id = %(id)s", {"id": user_id})
```

```javascript
// JavaScript - 字符串拼接SQL
db.query("SELECT * FROM users WHERE id = " + userId);
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// 安全写法
db.query("SELECT * FROM users WHERE id = ?", [userId]);
```

**Semgrep规则**:
```yaml
rules:
  - id: sql-injection
    patterns:
      - pattern-either:
          - pattern: $DB.execute($QUERY + ...)
          - pattern: $DB.execute(f"...{$VAR}...")
          - pattern: $DB.query($QUERY + ...)
    message: "检测到潜在的SQL注入漏洞"
    severity: ERROR
```

### 3. 命令注入 (CWE-78)

**危险模式**:
```python
# Python
os.system("ping " + user_input)
subprocess.call("ls " + filename, shell=True)
os.popen("cat " + filepath)

# 安全写法
subprocess.run(["ping", user_input], shell=False)
subprocess.run(["ls", filename], shell=False)
```

```javascript
// JavaScript
exec("ls " + userInput);
child_process.execSync(`cat ${filepath}`);

// 安全写法
execFile("ls", [userInput]);
```

**检测正则**:
```regex
os\.system\s*\([^)]*\+
subprocess\.(call|run|Popen)\s*\([^)]*shell\s*=\s*True
exec\s*\([^)]*\+
child_process\.exec(Sync)?\s*\(`[^`]*\$\{
```

### 4. XSS跨站脚本 (CWE-79)

**危险模式**:
```javascript
// 直接插入HTML
element.innerHTML = userInput;
document.write(userInput);
$(selector).html(userInput);

// React中的危险用法
<div dangerouslySetInnerHTML={{__html: userInput}} />
```

```python
# Flask模板
return f"<div>{user_input}</div>"
render_template_string("<div>" + user_input + "</div>")
```

**安全实践**:
- 使用textContent替代innerHTML
- 对输出进行HTML实体编码
- 使用CSP (Content Security Policy)
- React中避免dangerouslySetInnerHTML

### 5. SSRF服务端请求伪造 (CWE-918)

**危险模式**:
```python
# Python
requests.get(user_url)
urllib.request.urlopen(user_provided_url)

# 检查URL是否为内部地址
import ipaddress
def is_internal(url):
    ip = socket.gethostbyname(urlparse(url).hostname)
    return ipaddress.ip_address(ip).is_private
```

```javascript
// Node.js
fetch(userUrl);
axios.get(req.body.url);
```

**防护措施**:
- 维护URL白名单
- 禁止访问私有IP范围 (10.x, 172.16-31.x, 192.168.x, 127.x)
- 禁止访问云元数据端点 (169.254.169.254)

### 6. 路径遍历 (CWE-22)

**危险模式**:
```python
# 危险
open("/uploads/" + filename)
os.path.join(base_path, user_input)  # 如果user_input以/开头

# 安全
import os
safe_path = os.path.normpath(os.path.join(base_path, filename))
if not safe_path.startswith(base_path):
    raise ValueError("Invalid path")
```

**检测正则**:
```regex
\.\.\/|\.\.\\
open\s*\([^)]*\+
```

### 7. 不安全的反序列化 (CWE-502)

**危险模式**:
```python
# Python
pickle.loads(user_data)
yaml.load(user_data)  # 使用yaml.safe_load代替
eval(user_input)

# 安全
yaml.safe_load(user_data)
json.loads(user_data)
```

```javascript
// JavaScript
eval(userInput);
new Function(userCode)();
JSON.parse(userInput);  // 相对安全但要验证结构
```

### 8. 硬编码凭证 (CWE-798)

**检测正则**:
```regex
# API Keys
api[_-]?key\s*[:=]\s*['"][a-zA-Z0-9]{20,}['"]
apikey\s*[:=]\s*['"][^'"]+['"]

# AWS
AKIA[0-9A-Z]{16}
aws[_-]?secret[_-]?access[_-]?key

# Private Keys
-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----

# Generic Secrets
password\s*[:=]\s*['"][^'"]+['"]
secret\s*[:=]\s*['"][^'"]+['"]
token\s*[:=]\s*['"][^'"]+['"]

# JWT
eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+
```

### 9. 弱加密算法 (CWE-327)

**危险算法**:
- MD5 (用于密码哈希)
- SHA1 (用于安全目的)
- DES, 3DES
- RC4

**检测模式**:
```python
# 危险
hashlib.md5(password)
hashlib.sha1(secret)
DES.new(key)

# 推荐
from argon2 import PasswordHasher
ph = PasswordHasher()
hash = ph.hash(password)
```

### 10. 不安全的随机数 (CWE-330)

**危险模式**:
```python
# 危险 - 不要用于安全目的
import random
token = ''.join(random.choices(string.ascii_letters, k=32))

# 安全
import secrets
token = secrets.token_urlsafe(32)
```

```javascript
// 危险
Math.random().toString(36)

// 安全
crypto.randomBytes(32).toString('hex')
```

## 依赖漏洞检测

### 已知高危依赖版本

```json
{
  "react": {
    "vulnerable": ["19.0.0", "19.1.0", "19.1.1", "19.2.0"],
    "cve": "CVE-2025-55182",
    "severity": "critical"
  },
  "next": {
    "vulnerable_pattern": ">=14.3.0-canary.77 <14.2.21 || >=15.0.0 <15.1.4",
    "cve": "CVE-2025-66478",
    "severity": "critical"
  },
  "log4j-core": {
    "vulnerable": ["2.0-beta9", "2.14.1"],
    "cve": "CVE-2021-44228",
    "severity": "critical"
  },
  "lodash": {
    "vulnerable": ["<4.17.21"],
    "cve": "CVE-2021-23337",
    "severity": "high"
  },
  "axios": {
    "vulnerable": ["<0.21.1"],
    "cve": "CVE-2021-3749",
    "severity": "high"
  }
}
```

## 文件扫描排除规则

```gitignore
# 排除目录
node_modules/
vendor/
.git/
dist/
build/
__pycache__/
.venv/
venv/

# 排除文件类型
*.min.js
*.map
*.lock
*.sum
```

## 严重性分级

| 级别 | CVSS范围 | 响应时间 | 描述 |
|-----|---------|---------|-----|
| Critical | 9.0-10.0 | 立即修复 | 可被远程利用，无需认证 |
| High | 7.0-8.9 | 24小时内 | 可导致重大安全影响 |
| Medium | 4.0-6.9 | 1周内 | 需要特定条件才能利用 |
| Low | 0.1-3.9 | 下次发布 | 影响有限或难以利用 |
| Info | 0.0 | 可选 | 信息性发现 |
