#!/usr/bin/env python3
"""
分析磁盘空间使用情况,找出占用空间最大的目录和文件
"""
import os
import sys
from pathlib import Path
from collections import defaultdict

def get_size(path):
    """获取文件或目录的大小"""
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        elif os.path.isdir(path):
            total = 0
            try:
                for entry in os.scandir(path):
                    try:
                        if entry.is_file(follow_symlinks=False):
                            total += entry.stat(follow_symlinks=False).st_size
                        elif entry.is_dir(follow_symlinks=False):
                            total += get_size(entry.path)
                    except (PermissionError, FileNotFoundError, OSError):
                        continue
            except (PermissionError, FileNotFoundError, OSError):
                pass
            return total
    except (PermissionError, FileNotFoundError, OSError):
        return 0

def format_size(size):
    """格式化文件大小为人类可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def analyze_directory(root_path, max_depth=2, top_n=20):
    """
    分析目录结构,找出最大的子目录和文件
    
    Args:
        root_path: 要分析的根目录路径
        max_depth: 最大扫描深度
        top_n: 返回前N个最大项
    """
    dir_sizes = {}
    large_files = []
    
    print(f"正在分析 {root_path} ...")
    print(f"扫描深度: {max_depth} 层")
    print("-" * 80)
    
    try:
        # 分析一级子目录
        for entry in os.scandir(root_path):
            try:
                if entry.is_dir(follow_symlinks=False):
                    size = get_size(entry.path)
                    dir_sizes[entry.path] = size
                    print(f"扫描: {entry.name} ... {format_size(size)}")
                elif entry.is_file(follow_symlinks=False):
                    size = entry.stat(follow_symlinks=False).st_size
                    if size > 100 * 1024 * 1024:  # 大于100MB的文件
                        large_files.append((entry.path, size))
            except (PermissionError, FileNotFoundError, OSError) as e:
                print(f"跳过 {entry.name}: 无权限访问")
                continue
    except (PermissionError, FileNotFoundError, OSError) as e:
        print(f"无法访问 {root_path}: {e}")
        return
    
    # 输出结果
    print("\n" + "=" * 80)
    print(f"📊 前 {top_n} 个最大目录:")
    print("=" * 80)
    
    sorted_dirs = sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True)[:top_n]
    for path, size in sorted_dirs:
        print(f"{format_size(size):>15} - {path}")
    
    if large_files:
        print("\n" + "=" * 80)
        print(f"📄 大文件 (>100MB):")
        print("=" * 80)
        sorted_files = sorted(large_files, key=lambda x: x[1], reverse=True)[:top_n]
        for path, size in sorted_files:
            print(f"{format_size(size):>15} - {path}")
    
    # 输出总计
    total_size = sum(dir_sizes.values())
    print("\n" + "=" * 80)
    print(f"总计扫描空间: {format_size(total_size)}")
    print("=" * 80)

def main():
    if len(sys.argv) < 2:
        print("使用方法: python analyze_disk.py <目录路径> [扫描深度] [显示数量]")
        print("示例: python analyze_disk.py C:\\ 2 20")
        sys.exit(1)
    
    root_path = sys.argv[1]
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    top_n = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    
    if not os.path.exists(root_path):
        print(f"错误: 路径不存在: {root_path}")
        sys.exit(1)
    
    analyze_directory(root_path, max_depth, top_n)

if __name__ == "__main__":
    main()
