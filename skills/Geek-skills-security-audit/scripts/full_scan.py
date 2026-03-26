#!/usr/bin/env python3
"""
Security Audit - Full Scan Script
全面安全扫描脚本，整合依赖检查、SAST、密钥扫描等
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class SecurityScanner:
    """安全扫描器主类"""
    
    def __init__(self, target_path: str, output_dir: str = None):
        self.target_path = Path(target_path).resolve()
        self.output_dir = Path(output_dir) if output_dir else self.target_path / "security_report"
        self.results: Dict[str, Any] = {
            "scan_time": datetime.now().isoformat(),
            "target": str(self.target_path),
            "findings": {
                "critical": [],
                "high": [],
                "medium": [],
                "low": [],
                "info": []
            },
            "summary": {}
        }
        
    def setup_output_dir(self):
        """创建输出目录"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def detect_project_type(self) -> Dict[str, bool]:
        """检测项目类型"""
        project_types = {
            "python": False,
            "nodejs": False,
            "react": False,
            "nextjs": False,
            "docker": False,
            "java": False,
            "go": False
        }
        
        # Python检测
        if (self.target_path / "requirements.txt").exists() or \
           (self.target_path / "setup.py").exists() or \
           (self.target_path / "pyproject.toml").exists():
            project_types["python"] = True
            
        # Node.js检测
        package_json = self.target_path / "package.json"
        if package_json.exists():
            project_types["nodejs"] = True
            try:
                with open(package_json) as f:
                    pkg = json.load(f)
                    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                    if "react" in deps:
                        project_types["react"] = True
                    if "next" in deps:
                        project_types["nextjs"] = True
            except:
                pass
                
        # Docker检测
        if (self.target_path / "Dockerfile").exists() or \
           (self.target_path / "docker-compose.yml").exists():
            project_types["docker"] = True
            
        # Java检测
        if (self.target_path / "pom.xml").exists() or \
           (self.target_path / "build.gradle").exists():
            project_types["java"] = True
            
        # Go检测
        if (self.target_path / "go.mod").exists():
            project_types["go"] = True
            
        return project_types

    def check_react2shell(self) -> List[Dict]:
        """检查React2Shell漏洞 (CVE-2025-55182)"""
        findings = []
        package_json = self.target_path / "package.json"
        
        if not package_json.exists():
            return findings
            
        try:
            with open(package_json) as f:
                pkg = json.load(f)
            
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            
            # 检查React版本
            react_version = deps.get("react", "")
            vulnerable_react = ["19.0.0", "19.1.0", "19.1.1", "19.2.0"]
            for v in vulnerable_react:
                if v in react_version:
                    findings.append({
                        "type": "CVE-2025-55182",
                        "severity": "critical",
                        "component": f"react@{react_version}",
                        "description": "React2Shell - 远程代码执行漏洞",
                        "remediation": "升级到 react@19.1.0-rc.1 或更高版本"
                    })
                    break
                    
            # 检查Next.js版本
            next_version = deps.get("next", "")
            if next_version:
                # 简单版本检查
                if "15." in next_version or "16." in next_version or "14.3.0-canary" in next_version:
                    findings.append({
                        "type": "CVE-2025-66478",
                        "severity": "critical",
                        "component": f"next@{next_version}",
                        "description": "Next.js RSC远程代码执行漏洞",
                        "remediation": "运行 npx fix-react2shell-next 或升级到安全版本"
                    })
                    
        except Exception as e:
            print(f"检查React2Shell时出错: {e}")
            
        return findings

    def run_npm_audit(self) -> List[Dict]:
        """运行npm audit"""
        findings = []
        package_json = self.target_path / "package.json"
        
        if not package_json.exists():
            return findings
            
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=self.target_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.stdout:
                audit_data = json.loads(result.stdout)
                vulnerabilities = audit_data.get("vulnerabilities", {})
                
                for pkg_name, vuln_info in vulnerabilities.items():
                    severity = vuln_info.get("severity", "unknown")
                    findings.append({
                        "type": "dependency_vulnerability",
                        "severity": severity,
                        "component": pkg_name,
                        "description": vuln_info.get("via", [{}])[0].get("title", "Unknown vulnerability") if isinstance(vuln_info.get("via", []), list) and vuln_info.get("via") else "Unknown",
                        "remediation": f"npm audit fix 或手动更新 {pkg_name}"
                    })
                    
        except subprocess.TimeoutExpired:
            print("npm audit 超时")
        except FileNotFoundError:
            print("npm 未安装")
        except Exception as e:
            print(f"npm audit 出错: {e}")
            
        return findings

    def run_pip_audit(self) -> List[Dict]:
        """运行Python依赖审计"""
        findings = []
        
        requirements = self.target_path / "requirements.txt"
        if not requirements.exists():
            return findings
            
        # 尝试使用pip-audit
        try:
            result = subprocess.run(
                ["pip-audit", "--format", "json", "-r", str(requirements)],
                cwd=self.target_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.stdout:
                audit_data = json.loads(result.stdout)
                for vuln in audit_data:
                    findings.append({
                        "type": "dependency_vulnerability",
                        "severity": "high",
                        "component": f"{vuln.get('name')}@{vuln.get('version')}",
                        "description": vuln.get("vulns", [{}])[0].get("id", "Unknown CVE"),
                        "remediation": f"升级 {vuln.get('name')}"
                    })
                    
        except FileNotFoundError:
            # 回退到safety
            try:
                result = subprocess.run(
                    ["safety", "check", "--json", "-r", str(requirements)],
                    cwd=self.target_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.stdout:
                    safety_data = json.loads(result.stdout)
                    for vuln in safety_data.get("vulnerabilities", []):
                        findings.append({
                            "type": "dependency_vulnerability",
                            "severity": "high",
                            "component": f"{vuln.get('package_name')}@{vuln.get('analyzed_version')}",
                            "description": vuln.get("vulnerability_id", "Unknown"),
                            "remediation": vuln.get("more_info_path", "查看安全公告")
                        })
            except:
                print("safety 和 pip-audit 都未安装")
        except Exception as e:
            print(f"Python依赖审计出错: {e}")
            
        return findings

    def run_bandit(self) -> List[Dict]:
        """运行Bandit Python SAST"""
        findings = []
        
        # 检查是否有Python文件
        py_files = list(self.target_path.rglob("*.py"))
        if not py_files:
            return findings
            
        try:
            result = subprocess.run(
                ["bandit", "-r", str(self.target_path), "-f", "json", 
                 "--exclude", ".venv,venv,node_modules,__pycache__"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.stdout:
                bandit_data = json.loads(result.stdout)
                for issue in bandit_data.get("results", []):
                    severity_map = {"HIGH": "high", "MEDIUM": "medium", "LOW": "low"}
                    findings.append({
                        "type": "code_vulnerability",
                        "severity": severity_map.get(issue.get("issue_severity"), "medium"),
                        "component": issue.get("filename", "unknown"),
                        "line": issue.get("line_number"),
                        "description": f"{issue.get('issue_text')} ({issue.get('test_id')})",
                        "remediation": issue.get("more_info", "查看Bandit文档")
                    })
                    
        except FileNotFoundError:
            print("Bandit未安装，跳过Python SAST")
        except Exception as e:
            print(f"Bandit扫描出错: {e}")
            
        return findings

    def scan_secrets(self) -> List[Dict]:
        """扫描硬编码的密钥和凭证"""
        import re
        findings = []
        
        # 密钥模式
        secret_patterns = [
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
            (r'["\']?[a-zA-Z_]*(?:api[_-]?key|apikey)["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{20,}["\']', 'API Key'),
            (r'["\']?[a-zA-Z_]*(?:secret|password|passwd|pwd)["\']?\s*[:=]\s*["\'][^"\']{8,}["\']', 'Secret/Password'),
            (r'-----BEGIN (?:RSA|DSA|EC|OPENSSH) PRIVATE KEY-----', 'Private Key'),
            (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Token'),
            (r'xox[baprs]-[0-9a-zA-Z-]{10,}', 'Slack Token'),
            (r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', 'JWT Token'),
        ]
        
        # 要排除的目录和文件
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}
        exclude_extensions = {'.min.js', '.map', '.lock', '.sum', '.png', '.jpg', '.gif', '.ico'}
        
        for filepath in self.target_path.rglob("*"):
            # 跳过目录
            if filepath.is_dir():
                continue
                
            # 跳过排除的目录
            if any(excluded in filepath.parts for excluded in exclude_dirs):
                continue
                
            # 跳过二进制和排除的扩展名
            if any(filepath.name.endswith(ext) for ext in exclude_extensions):
                continue
                
            try:
                content = filepath.read_text(errors='ignore')
                
                for pattern, secret_type in secret_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # 获取行号
                        line_num = content[:match.start()].count('\n') + 1
                        
                        # 避免重复报告
                        finding = {
                            "type": "secret_exposure",
                            "severity": "high",
                            "component": str(filepath.relative_to(self.target_path)),
                            "line": line_num,
                            "description": f"发现疑似 {secret_type}",
                            "remediation": "移除硬编码凭证，使用环境变量或密钥管理服务"
                        }
                        
                        # 简单去重
                        if finding not in findings:
                            findings.append(finding)
                            
            except Exception:
                continue
                
        return findings

    def generate_report(self):
        """生成扫描报告"""
        # 统计
        summary = {
            "total": 0,
            "critical": len(self.results["findings"]["critical"]),
            "high": len(self.results["findings"]["high"]),
            "medium": len(self.results["findings"]["medium"]),
            "low": len(self.results["findings"]["low"]),
            "info": len(self.results["findings"]["info"])
        }
        summary["total"] = sum(v for k, v in summary.items() if k != "total")
        self.results["summary"] = summary
        
        # 保存JSON报告
        report_json = self.output_dir / "security_report.json"
        with open(report_json, "w") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
            
        # 生成Markdown摘要
        report_md = self.output_dir / "summary.md"
        with open(report_md, "w") as f:
            f.write("# 安全扫描报告\n\n")
            f.write(f"**扫描时间**: {self.results['scan_time']}\n\n")
            f.write(f"**扫描目标**: {self.results['target']}\n\n")
            f.write("## 摘要\n\n")
            f.write(f"| 严重性 | 数量 |\n")
            f.write(f"|--------|------|\n")
            f.write(f"| 🔴 Critical | {summary['critical']} |\n")
            f.write(f"| 🟠 High | {summary['high']} |\n")
            f.write(f"| 🟡 Medium | {summary['medium']} |\n")
            f.write(f"| 🔵 Low | {summary['low']} |\n")
            f.write(f"| ⚪ Info | {summary['info']} |\n")
            f.write(f"| **总计** | **{summary['total']}** |\n\n")
            
            # 详细发现
            if summary['critical'] > 0 or summary['high'] > 0:
                f.write("## 高危发现\n\n")
                for finding in self.results["findings"]["critical"] + self.results["findings"]["high"]:
                    f.write(f"### {finding['type']}\n\n")
                    f.write(f"- **组件**: {finding.get('component', 'N/A')}\n")
                    if finding.get('line'):
                        f.write(f"- **行号**: {finding['line']}\n")
                    f.write(f"- **描述**: {finding.get('description', 'N/A')}\n")
                    f.write(f"- **修复建议**: {finding.get('remediation', 'N/A')}\n\n")
                    
        print(f"\n报告已生成: {self.output_dir}")
        return self.results

    def run(self):
        """运行完整扫描"""
        print("=" * 60)
        print("🔐 Security Audit - 安全扫描开始")
        print("=" * 60)
        print(f"扫描目标: {self.target_path}")
        
        self.setup_output_dir()
        
        # 检测项目类型
        print("\n[1/6] 检测项目类型...")
        project_types = self.detect_project_type()
        active_types = [k for k, v in project_types.items() if v]
        print(f"  检测到: {', '.join(active_types) if active_types else '未知'}")
        
        # React2Shell检查
        print("\n[2/6] 检查React2Shell漏洞 (CVE-2025-55182)...")
        react2shell_findings = self.check_react2shell()
        for f in react2shell_findings:
            self.results["findings"][f["severity"]].append(f)
        print(f"  发现: {len(react2shell_findings)} 个问题")
        
        # 依赖检查
        print("\n[3/6] 扫描依赖漏洞...")
        if project_types["nodejs"]:
            npm_findings = self.run_npm_audit()
            for f in npm_findings:
                self.results["findings"][f["severity"]].append(f)
            print(f"  npm audit: {len(npm_findings)} 个问题")
            
        if project_types["python"]:
            pip_findings = self.run_pip_audit()
            for f in pip_findings:
                self.results["findings"][f["severity"]].append(f)
            print(f"  pip audit: {len(pip_findings)} 个问题")
            
        # SAST扫描
        print("\n[4/6] 静态代码分析 (SAST)...")
        if project_types["python"]:
            bandit_findings = self.run_bandit()
            for f in bandit_findings:
                self.results["findings"][f["severity"]].append(f)
            print(f"  Bandit: {len(bandit_findings)} 个问题")
            
        # 密钥扫描
        print("\n[5/6] 扫描泄露的密钥...")
        secret_findings = self.scan_secrets()
        for f in secret_findings:
            self.results["findings"][f["severity"]].append(f)
        print(f"  发现: {len(secret_findings)} 个潜在泄露")
        
        # 生成报告
        print("\n[6/6] 生成报告...")
        self.generate_report()
        
        # 打印摘要
        print("\n" + "=" * 60)
        print("📊 扫描完成")
        print("=" * 60)
        s = self.results["summary"]
        print(f"  🔴 Critical: {s['critical']}")
        print(f"  🟠 High: {s['high']}")
        print(f"  🟡 Medium: {s['medium']}")
        print(f"  🔵 Low: {s['low']}")
        print(f"  总计: {s['total']} 个发现")
        
        if s['critical'] > 0:
            print("\n⚠️  发现严重漏洞，请立即修复！")
            return 1
        return 0


def main():
    parser = argparse.ArgumentParser(description="Security Audit - 全面安全扫描")
    parser.add_argument("target", help="扫描目标路径")
    parser.add_argument("-o", "--output", help="报告输出目录")
    args = parser.parse_args()
    
    scanner = SecurityScanner(args.target, args.output)
    sys.exit(scanner.run())


if __name__ == "__main__":
    main()
