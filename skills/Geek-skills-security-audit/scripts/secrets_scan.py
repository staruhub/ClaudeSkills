#!/usr/bin/env python3
"""
Security Audit - Secrets Scanner
扫描代码中泄露的密钥、凭证和敏感信息
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Pattern
from dataclasses import dataclass
import base64

@dataclass
class SecretPattern:
    """密钥模式定义"""
    name: str
    pattern: Pattern
    severity: str
    description: str


# 定义密钥检测模式
SECRET_PATTERNS = [
    # AWS
    SecretPattern(
        name="AWS Access Key ID",
        pattern=re.compile(r'AKIA[0-9A-Z]{16}'),
        severity="CRITICAL",
        description="AWS访问密钥ID"
    ),
    SecretPattern(
        name="AWS Secret Access Key",
        pattern=re.compile(r'["\']?aws[_-]?secret[_-]?access[_-]?key["\']?\s*[:=]\s*["\']([A-Za-z0-9/+=]{40})["\']', re.I),
        severity="CRITICAL",
        description="AWS秘密访问密钥"
    ),
    
    # GitHub
    SecretPattern(
        name="GitHub Token",
        pattern=re.compile(r'ghp_[a-zA-Z0-9]{36}'),
        severity="HIGH",
        description="GitHub个人访问令牌"
    ),
    SecretPattern(
        name="GitHub OAuth",
        pattern=re.compile(r'gho_[a-zA-Z0-9]{36}'),
        severity="HIGH",
        description="GitHub OAuth令牌"
    ),
    
    # Slack
    SecretPattern(
        name="Slack Token",
        pattern=re.compile(r'xox[baprs]-[0-9a-zA-Z-]{10,48}'),
        severity="HIGH",
        description="Slack API令牌"
    ),
    SecretPattern(
        name="Slack Webhook",
        pattern=re.compile(r'https://hooks\.slack\.com/services/T[a-zA-Z0-9_]+/B[a-zA-Z0-9_]+/[a-zA-Z0-9_]+'),
        severity="MEDIUM",
        description="Slack Webhook URL"
    ),
    
    # Google
    SecretPattern(
        name="Google API Key",
        pattern=re.compile(r'AIza[0-9A-Za-z\-_]{35}'),
        severity="HIGH",
        description="Google API密钥"
    ),
    SecretPattern(
        name="Google OAuth",
        pattern=re.compile(r'[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com'),
        severity="MEDIUM",
        description="Google OAuth客户端ID"
    ),
    
    # Private Keys
    SecretPattern(
        name="RSA Private Key",
        pattern=re.compile(r'-----BEGIN RSA PRIVATE KEY-----'),
        severity="CRITICAL",
        description="RSA私钥"
    ),
    SecretPattern(
        name="OpenSSH Private Key",
        pattern=re.compile(r'-----BEGIN OPENSSH PRIVATE KEY-----'),
        severity="CRITICAL",
        description="OpenSSH私钥"
    ),
    SecretPattern(
        name="PGP Private Key",
        pattern=re.compile(r'-----BEGIN PGP PRIVATE KEY BLOCK-----'),
        severity="CRITICAL",
        description="PGP私钥"
    ),
    
    # JWT
    SecretPattern(
        name="JWT Token",
        pattern=re.compile(r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+'),
        severity="MEDIUM",
        description="JSON Web Token"
    ),
    
    # Generic API Keys
    SecretPattern(
        name="Generic API Key",
        pattern=re.compile(r'["\']?[a-zA-Z_]*api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']', re.I),
        severity="HIGH",
        description="通用API密钥"
    ),
    SecretPattern(
        name="Generic Secret",
        pattern=re.compile(r'["\']?[a-zA-Z_]*secret["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{16,})["\']', re.I),
        severity="HIGH",
        description="通用密钥"
    ),
    
    # Database
    SecretPattern(
        name="Database Connection String",
        pattern=re.compile(r'(mongodb|mysql|postgresql|postgres|redis)://[a-zA-Z0-9_]+:[^@\s]+@[^\s]+', re.I),
        severity="CRITICAL",
        description="数据库连接字符串（含密码）"
    ),
    
    # Passwords
    SecretPattern(
        name="Password Assignment",
        pattern=re.compile(r'["\']?password["\']?\s*[:=]\s*["\']([^"\']{8,})["\']', re.I),
        severity="HIGH",
        description="硬编码密码"
    ),
    
    # Firebase
    SecretPattern(
        name="Firebase URL",
        pattern=re.compile(r'[a-z0-9-]+\.firebaseio\.com'),
        severity="MEDIUM",
        description="Firebase数据库URL"
    ),
    
    # Stripe
    SecretPattern(
        name="Stripe Secret Key",
        pattern=re.compile(r'sk_live_[0-9a-zA-Z]{24,}'),
        severity="CRITICAL",
        description="Stripe生产环境密钥"
    ),
    SecretPattern(
        name="Stripe Publishable Key",
        pattern=re.compile(r'pk_live_[0-9a-zA-Z]{24,}'),
        severity="MEDIUM",
        description="Stripe生产环境公钥"
    ),
    
    # Twilio
    SecretPattern(
        name="Twilio API Key",
        pattern=re.compile(r'SK[0-9a-fA-F]{32}'),
        severity="HIGH",
        description="Twilio API密钥"
    ),
    
    # SendGrid
    SecretPattern(
        name="SendGrid API Key",
        pattern=re.compile(r'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}'),
        severity="HIGH",
        description="SendGrid API密钥"
    ),
    
    # npm
    SecretPattern(
        name="npm Token",
        pattern=re.compile(r'npm_[a-zA-Z0-9]{36}'),
        severity="HIGH",
        description="npm访问令牌"
    ),
    
    # Discord
    SecretPattern(
        name="Discord Token",
        pattern=re.compile(r'[MN][A-Za-z\d]{23,}\.[\w-]{6}\.[\w-]{27}'),
        severity="HIGH",
        description="Discord Bot令牌"
    ),
    SecretPattern(
        name="Discord Webhook",
        pattern=re.compile(r'https://discord(?:app)?\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_-]+'),
        severity="MEDIUM",
        description="Discord Webhook URL"
    ),
    
    # Heroku
    SecretPattern(
        name="Heroku API Key",
        pattern=re.compile(r'["\']?heroku[_-]?api[_-]?key["\']?\s*[:=]\s*["\']([0-9a-fA-F-]{36})["\']', re.I),
        severity="HIGH",
        description="Heroku API密钥"
    ),
    
    # Azure
    SecretPattern(
        name="Azure Connection String",
        pattern=re.compile(r'DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[^;]+'),
        severity="CRITICAL",
        description="Azure存储连接字符串"
    ),
]

# 排除的目录
EXCLUDED_DIRS = {
    '.git', 'node_modules', '__pycache__', '.venv', 'venv', 
    'dist', 'build', '.next', '.nuxt', 'vendor', 'coverage',
    '.idea', '.vscode', 'target', 'bin', 'obj'
}

# 排除的文件扩展名
EXCLUDED_EXTENSIONS = {
    '.min.js', '.map', '.lock', '.sum', '.png', '.jpg', '.jpeg',
    '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot',
    '.mp3', '.mp4', '.webm', '.zip', '.tar', '.gz', '.pdf'
}

# 应该检查的文件
INCLUDED_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.vue', '.rb', '.php',
    '.java', '.go', '.rs', '.c', '.cpp', '.h', '.cs', '.swift',
    '.kt', '.scala', '.sh', '.bash', '.zsh', '.ps1', '.bat',
    '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
    '.env', '.properties', '.xml', '.md', '.txt', '.sql'
}


def is_likely_false_positive(match: str, filepath: str) -> bool:
    """检查是否可能是误报"""
    # 检查是否在测试文件中
    test_indicators = ['test', 'spec', 'mock', 'fixture', 'example', 'sample', 'demo']
    if any(indicator in filepath.lower() for indicator in test_indicators):
        return True
        
    # 检查是否是占位符
    placeholder_patterns = [
        r'^x{8,}$',
        r'^0{8,}$',
        r'^your[_-]',
        r'^my[_-]',
        r'^example[_-]',
        r'^test[_-]',
        r'^dummy[_-]',
        r'^placeholder',
        r'^changeme$',
        r'^CHANGEME$',
        r'^todo$',
        r'^TODO$',
        r'^\*+$',
        r'^\.\.\.+$',
    ]
    
    for pattern in placeholder_patterns:
        if re.search(pattern, match, re.I):
            return True
            
    return False


def decode_jwt_preview(token: str) -> str:
    """解码JWT token的payload部分（仅用于展示）"""
    try:
        parts = token.split('.')
        if len(parts) == 3:
            # 添加padding
            payload = parts[1]
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += '=' * padding
            decoded = base64.urlsafe_b64decode(payload)
            return decoded.decode('utf-8')[:100] + "..."
    except:
        pass
    return ""


def scan_file(filepath: Path) -> List[Dict]:
    """扫描单个文件"""
    findings = []
    
    try:
        content = filepath.read_text(errors='ignore')
        lines = content.split('\n')
        
        for pattern_def in SECRET_PATTERNS:
            for match in pattern_def.pattern.finditer(content):
                # 获取行号
                line_start = content[:match.start()].count('\n') + 1
                
                # 获取匹配内容
                matched_text = match.group(0)
                
                # 检查误报
                if is_likely_false_positive(matched_text, str(filepath)):
                    continue
                    
                # 获取上下文行
                if line_start <= len(lines):
                    context_line = lines[line_start - 1].strip()[:100]
                else:
                    context_line = ""
                    
                finding = {
                    "type": pattern_def.name,
                    "severity": pattern_def.severity,
                    "file": str(filepath),
                    "line": line_start,
                    "description": pattern_def.description,
                    "context": context_line,
                    "match_preview": matched_text[:50] + "..." if len(matched_text) > 50 else matched_text
                }
                
                # JWT特殊处理
                if pattern_def.name == "JWT Token":
                    jwt_preview = decode_jwt_preview(matched_text)
                    if jwt_preview:
                        finding["jwt_payload_preview"] = jwt_preview
                        
                findings.append(finding)
                
    except Exception as e:
        pass  # 静默处理不可读文件
        
    return findings


def scan_directory(root_path: Path) -> List[Dict]:
    """扫描目录"""
    all_findings = []
    files_scanned = 0
    
    for filepath in root_path.rglob('*'):
        # 跳过目录
        if filepath.is_dir():
            continue
            
        # 跳过排除的目录
        if any(excluded in filepath.parts for excluded in EXCLUDED_DIRS):
            continue
            
        # 跳过排除的扩展名
        if any(filepath.name.endswith(ext) for ext in EXCLUDED_EXTENSIONS):
            continue
            
        # 检查文件扩展名
        if filepath.suffix.lower() not in INCLUDED_EXTENSIONS:
            # 也检查没有扩展名的配置文件
            if filepath.name not in {'.env', '.env.local', '.env.production', 'Dockerfile', 'Makefile'}:
                continue
                
        # 跳过大文件 (>1MB)
        try:
            if filepath.stat().st_size > 1024 * 1024:
                continue
        except:
            continue
            
        files_scanned += 1
        findings = scan_file(filepath)
        all_findings.extend(findings)
        
    print(f"扫描了 {files_scanned} 个文件")
    return all_findings


def generate_report(findings: List[Dict], output_path: Path):
    """生成报告"""
    # 按严重性分组
    by_severity = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": []}
    for f in findings:
        severity = f.get("severity", "MEDIUM")
        if severity in by_severity:
            by_severity[severity].append(f)
            
    # 保存JSON
    json_path = output_path / "secrets_report.json"
    with open(json_path, "w") as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)
        
    # 生成Markdown
    md_path = output_path / "secrets_report.md"
    with open(md_path, "w") as f:
        f.write("# 密钥泄露扫描报告\n\n")
        f.write("## 摘要\n\n")
        f.write(f"- 🔴 Critical: {len(by_severity['CRITICAL'])}\n")
        f.write(f"- 🟠 High: {len(by_severity['HIGH'])}\n")
        f.write(f"- 🟡 Medium: {len(by_severity['MEDIUM'])}\n")
        f.write(f"- 总计: {len(findings)}\n\n")
        
        if by_severity['CRITICAL']:
            f.write("## ⚠️ 严重问题\n\n")
            for finding in by_severity['CRITICAL']:
                f.write(f"### {finding['type']}\n\n")
                f.write(f"- **文件**: `{finding['file']}`\n")
                f.write(f"- **行号**: {finding['line']}\n")
                f.write(f"- **描述**: {finding['description']}\n")
                f.write(f"- **上下文**: `{finding.get('context', '')}`\n\n")
                
        if by_severity['HIGH']:
            f.write("## 高危问题\n\n")
            for finding in by_severity['HIGH']:
                f.write(f"- `{finding['file']}:{finding['line']}` - {finding['type']}\n")
                
    return json_path, md_path


def main():
    if len(sys.argv) < 2:
        print("用法: python secrets_scan.py <项目路径> [输出目录]")
        sys.exit(1)
        
    target_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else target_path
    
    if not target_path.exists():
        print(f"错误: 路径不存在 {target_path}")
        sys.exit(1)
        
    print("=" * 60)
    print("🔑 密钥泄露扫描")
    print("=" * 60)
    print(f"扫描路径: {target_path}\n")
    
    # 执行扫描
    findings = scan_directory(target_path)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📊 扫描结果")
    print("=" * 60)
    
    if not findings:
        print("\n✅ 未发现泄露的密钥")
    else:
        critical = sum(1 for f in findings if f["severity"] == "CRITICAL")
        high = sum(1 for f in findings if f["severity"] == "HIGH")
        
        print(f"\n发现 {len(findings)} 个潜在密钥泄露:")
        print(f"  🔴 Critical: {critical}")
        print(f"  🟠 High: {high}")
        print(f"  🟡 Medium: {len(findings) - critical - high}")
        
        # 显示关键发现
        print("\n关键发现:")
        for finding in findings[:10]:  # 只显示前10个
            severity_icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(finding["severity"], "⚪")
            print(f"  {severity_icon} {finding['file']}:{finding['line']}")
            print(f"     {finding['type']}: {finding['description']}")
            
        if len(findings) > 10:
            print(f"\n  ... 还有 {len(findings) - 10} 个发现")
            
    # 生成报告
    output_path.mkdir(parents=True, exist_ok=True)
    json_path, md_path = generate_report(findings, output_path)
    print(f"\n报告已保存:")
    print(f"  - {json_path}")
    print(f"  - {md_path}")
    
    # 返回码
    if any(f["severity"] == "CRITICAL" for f in findings):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
