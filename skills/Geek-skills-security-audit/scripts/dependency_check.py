#!/usr/bin/env python3
"""
Security Audit - Dependency Check Script
专门的依赖漏洞检查脚本，检测已知CVE
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import re

# 已知高危漏洞版本
KNOWN_VULNERABLE = {
    # React2Shell (CVE-2025-55182)
    "react": {
        "vulnerable": ["19.0.0", "19.1.0", "19.1.1", "19.2.0"],
        "cve": "CVE-2025-55182",
        "severity": "CRITICAL",
        "fix": "升级到 19.1.0-rc.1+"
    },
    "react-server-dom-webpack": {
        "vulnerable": ["19.0.0", "19.1.0", "19.1.1", "19.2.0"],
        "cve": "CVE-2025-55182",
        "severity": "CRITICAL",
        "fix": "升级到安全版本"
    },
    "react-server-dom-turbopack": {
        "vulnerable": ["19.0.0", "19.1.0", "19.1.1", "19.2.0"],
        "cve": "CVE-2025-55182",
        "severity": "CRITICAL",
        "fix": "升级到安全版本"
    },
    # Log4Shell
    "log4j-core": {
        "vulnerable_range": ("2.0-beta9", "2.14.1"),
        "cve": "CVE-2021-44228",
        "severity": "CRITICAL",
        "fix": "升级到 2.17.0+"
    },
    # 其他常见漏洞
    "lodash": {
        "vulnerable_below": "4.17.21",
        "cve": "CVE-2021-23337",
        "severity": "HIGH",
        "fix": "升级到 4.17.21+"
    },
    "axios": {
        "vulnerable_below": "0.21.1",
        "cve": "CVE-2021-3749",
        "severity": "HIGH",
        "fix": "升级到 0.21.1+"
    },
    "minimist": {
        "vulnerable_below": "1.2.6",
        "cve": "CVE-2021-44906",
        "severity": "CRITICAL",
        "fix": "升级到 1.2.6+"
    },
    "node-forge": {
        "vulnerable_below": "1.3.0",
        "cve": "CVE-2022-24771",
        "severity": "HIGH",
        "fix": "升级到 1.3.0+"
    }
}


def parse_version(version: str) -> Tuple:
    """解析版本号为可比较的元组"""
    # 移除前缀 ^, ~, >=, 等
    version = re.sub(r'^[\^~>=<]+', '', version)
    # 提取数字部分
    parts = re.findall(r'\d+', version)
    return tuple(int(p) for p in parts) if parts else (0,)


def version_compare(v1: str, v2: str) -> int:
    """比较两个版本号，返回 -1, 0, 1"""
    t1, t2 = parse_version(v1), parse_version(v2)
    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    return 0


def check_npm_dependencies(project_path: Path) -> List[Dict]:
    """检查npm依赖"""
    findings = []
    package_json = project_path / "package.json"
    
    if not package_json.exists():
        return findings
        
    try:
        with open(package_json) as f:
            pkg = json.load(f)
            
        all_deps = {}
        all_deps.update(pkg.get("dependencies", {}))
        all_deps.update(pkg.get("devDependencies", {}))
        
        # 检查已知漏洞
        for dep_name, dep_version in all_deps.items():
            if dep_name in KNOWN_VULNERABLE:
                vuln_info = KNOWN_VULNERABLE[dep_name]
                is_vulnerable = False
                
                # 精确版本匹配
                if "vulnerable" in vuln_info:
                    clean_version = re.sub(r'^[\^~>=<]+', '', dep_version)
                    if clean_version in vuln_info["vulnerable"]:
                        is_vulnerable = True
                        
                # 版本范围检查
                elif "vulnerable_below" in vuln_info:
                    if version_compare(dep_version, vuln_info["vulnerable_below"]) < 0:
                        is_vulnerable = True
                        
                if is_vulnerable:
                    findings.append({
                        "package": dep_name,
                        "version": dep_version,
                        "cve": vuln_info["cve"],
                        "severity": vuln_info["severity"],
                        "fix": vuln_info["fix"]
                    })
                    
        # 特殊检查：Next.js版本
        next_version = all_deps.get("next", "")
        if next_version:
            # 检查是否是有漏洞的版本
            clean_version = re.sub(r'^[\^~>=<]+', '', next_version)
            if "15." in clean_version or "16." in clean_version:
                # 需要检查具体版本
                if version_compare(clean_version, "15.1.4") < 0:
                    findings.append({
                        "package": "next",
                        "version": next_version,
                        "cve": "CVE-2025-66478",
                        "severity": "CRITICAL",
                        "fix": "升级到 15.1.4+ 或运行 npx fix-react2shell-next"
                    })
            elif "14.3.0-canary" in clean_version:
                findings.append({
                    "package": "next",
                    "version": next_version,
                    "cve": "CVE-2025-66478",
                    "severity": "CRITICAL",
                    "fix": "降级到稳定版 14.2.21"
                })
                
    except Exception as e:
        print(f"解析package.json出错: {e}")
        
    return findings


def check_python_dependencies(project_path: Path) -> List[Dict]:
    """检查Python依赖"""
    findings = []
    requirements = project_path / "requirements.txt"
    
    if not requirements.exists():
        return findings
        
    # Python常见漏洞
    python_vulnerable = {
        "pyyaml": {
            "vulnerable_below": "5.4",
            "cve": "CVE-2020-14343",
            "severity": "CRITICAL",
            "fix": "升级到 5.4+"
        },
        "django": {
            "vulnerable_below": "3.2.14",
            "cve": "CVE-2022-34265",
            "severity": "HIGH",
            "fix": "升级到最新安全版本"
        },
        "flask": {
            "vulnerable_below": "2.2.5",
            "cve": "CVE-2023-30861",
            "severity": "HIGH",
            "fix": "升级到 2.2.5+"
        },
        "requests": {
            "vulnerable_below": "2.31.0",
            "cve": "CVE-2023-32681",
            "severity": "MEDIUM",
            "fix": "升级到 2.31.0+"
        },
        "cryptography": {
            "vulnerable_below": "41.0.0",
            "cve": "Multiple",
            "severity": "HIGH",
            "fix": "升级到最新版本"
        },
        "pillow": {
            "vulnerable_below": "10.0.1",
            "cve": "CVE-2023-44271",
            "severity": "HIGH",
            "fix": "升级到 10.0.1+"
        }
    }
    
    try:
        with open(requirements) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                # 解析依赖行
                match = re.match(r'^([a-zA-Z0-9_-]+)\s*([>=<~!]+)?\s*([\d.]+)?', line.lower())
                if match:
                    pkg_name = match.group(1)
                    pkg_version = match.group(3) or "0.0.0"
                    
                    if pkg_name in python_vulnerable:
                        vuln_info = python_vulnerable[pkg_name]
                        if version_compare(pkg_version, vuln_info["vulnerable_below"]) < 0:
                            findings.append({
                                "package": pkg_name,
                                "version": pkg_version,
                                "cve": vuln_info["cve"],
                                "severity": vuln_info["severity"],
                                "fix": vuln_info["fix"]
                            })
                            
    except Exception as e:
        print(f"解析requirements.txt出错: {e}")
        
    return findings


def run_official_audit(project_path: Path) -> Dict:
    """运行官方审计工具"""
    results = {"npm": [], "pip": []}
    
    # npm audit
    if (project_path / "package.json").exists():
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.stdout:
                data = json.loads(result.stdout)
                results["npm"] = data
        except Exception as e:
            print(f"npm audit 失败: {e}")
            
    # pip-audit / safety
    if (project_path / "requirements.txt").exists():
        try:
            result = subprocess.run(
                ["pip-audit", "--format", "json"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.stdout:
                results["pip"] = json.loads(result.stdout)
        except FileNotFoundError:
            try:
                result = subprocess.run(
                    ["safety", "check", "--json"],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.stdout:
                    results["pip"] = json.loads(result.stdout)
            except:
                pass
        except Exception as e:
            print(f"Python依赖审计失败: {e}")
            
    return results


def main():
    if len(sys.argv) < 2:
        print("用法: python dependency_check.py <项目路径>")
        sys.exit(1)
        
    project_path = Path(sys.argv[1]).resolve()
    
    if not project_path.exists():
        print(f"错误: 路径不存在 {project_path}")
        sys.exit(1)
        
    print("=" * 60)
    print("🔍 依赖安全检查")
    print("=" * 60)
    print(f"扫描路径: {project_path}\n")
    
    all_findings = []
    
    # 检查npm依赖
    print("[1/3] 检查npm依赖...")
    npm_findings = check_npm_dependencies(project_path)
    all_findings.extend(npm_findings)
    print(f"  发现 {len(npm_findings)} 个漏洞")
    
    # 检查Python依赖
    print("[2/3] 检查Python依赖...")
    python_findings = check_python_dependencies(project_path)
    all_findings.extend(python_findings)
    print(f"  发现 {len(python_findings)} 个漏洞")
    
    # 运行官方审计工具
    print("[3/3] 运行官方审计工具...")
    official_results = run_official_audit(project_path)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📊 扫描结果")
    print("=" * 60)
    
    if not all_findings:
        print("\n✅ 未发现已知漏洞依赖")
    else:
        critical_count = sum(1 for f in all_findings if f["severity"] == "CRITICAL")
        high_count = sum(1 for f in all_findings if f["severity"] == "HIGH")
        
        print(f"\n发现 {len(all_findings)} 个有漏洞的依赖:")
        print(f"  🔴 Critical: {critical_count}")
        print(f"  🟠 High: {high_count}")
        print(f"  🟡 其他: {len(all_findings) - critical_count - high_count}")
        
        print("\n详细信息:")
        for finding in sorted(all_findings, key=lambda x: 0 if x["severity"] == "CRITICAL" else 1):
            severity_icon = "🔴" if finding["severity"] == "CRITICAL" else "🟠"
            print(f"\n{severity_icon} {finding['package']}@{finding['version']}")
            print(f"   CVE: {finding['cve']}")
            print(f"   修复: {finding['fix']}")
            
        if critical_count > 0:
            print("\n⚠️  发现严重漏洞！请立即修复。")
            sys.exit(1)
            
    # 保存报告
    report_path = project_path / "dependency_audit.json"
    with open(report_path, "w") as f:
        json.dump({
            "findings": all_findings,
            "official_audit": official_results
        }, f, indent=2, ensure_ascii=False)
    print(f"\n报告已保存: {report_path}")


if __name__ == "__main__":
    main()
