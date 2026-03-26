#!/usr/bin/env python3
"""
查找磁盘中的大文件
"""
import os
import sys
from pathlib import Path
from datetime import datetime

def format_size(size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def format_date(timestamp):
    """格式化时间戳"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def find_large_files(root_path, min_size_mb=100, max_results=50, file_types=None):
    """
    查找大文件
    
    Args:
        root_path: 搜索路径
        min_size_mb: 最小文件大小(MB)
        max_results: 最大返回结果数
        file_types: 文件类型过滤列表,如 ['.mp4', '.avi', '.iso']
    """
    print(f"正在扫描 {root_path} 中大于 {min_size_mb}MB 的文件...")
    print("-" * 100)
    
    min_size_bytes = min_size_mb * 1024 * 1024
    large_files = []
    scanned = 0
    skipped = 0
    
    # 跳过的系统目录
    skip_dirs = {
        'System Volume Information',
        '$Recycle.Bin',
        'Windows\\WinSxS',  # Windows组件存储,不建议清理
        'ProgramData\\Microsoft\\Windows\\WindowsUpdate',  # 更新缓存
    }
    
    try:
        for root, dirs, files in os.walk(root_path):
            # 跳过系统目录
            skip = False
            for skip_dir in skip_dirs:
                if skip_dir in root:
                    skip = True
                    break
            if skip:
                skipped += 1
                continue
            
            for filename in files:
                scanned += 1
                if scanned % 1000 == 0:
                    print(f"已扫描 {scanned} 个文件, 找到 {len(large_files)} 个大文件...", end='\r')
                
                try:
                    filepath = os.path.join(root, filename)
                    
                    # 文件类型过滤
                    if file_types:
                        ext = os.path.splitext(filename)[1].lower()
                        if ext not in file_types:
                            continue
                    
                    # 获取文件信息
                    stat_info = os.stat(filepath)
                    size = stat_info.st_size
                    
                    if size >= min_size_bytes:
                        large_files.append({
                            'path': filepath,
                            'size': size,
                            'modified': stat_info.st_mtime,
                            'accessed': stat_info.st_atime,
                        })
                    
                except (PermissionError, FileNotFoundError, OSError):
                    continue
    
    except KeyboardInterrupt:
        print("\n\n用户中断扫描")
    
    print(f"\n扫描完成: 共扫描 {scanned} 个文件, 跳过 {skipped} 个系统目录")
    print("-" * 100)
    
    # 排序并限制结果数量
    large_files.sort(key=lambda x: x['size'], reverse=True)
    large_files = large_files[:max_results]
    
    # 输出结果
    print(f"\n📊 找到的前 {len(large_files)} 个大文件:")
    print("=" * 100)
    print(f"{'大小':<12} {'最后修改':<20} {'最后访问':<20} {'路径'}")
    print("-" * 100)
    
    total_size = 0
    for file_info in large_files:
        print(f"{format_size(file_info['size']):<12} "
              f"{format_date(file_info['modified']):<20} "
              f"{format_date(file_info['accessed']):<20} "
              f"{file_info['path']}")
        total_size += file_info['size']
    
    print("-" * 100)
    print(f"总计: {format_size(total_size)}")
    
    # 按文件类型统计
    print("\n📈 按文件类型统计:")
    print("=" * 100)
    type_stats = {}
    for file_info in large_files:
        ext = os.path.splitext(file_info['path'])[1].lower() or '(无扩展名)'
        if ext not in type_stats:
            type_stats[ext] = {'count': 0, 'size': 0}
        type_stats[ext]['count'] += 1
        type_stats[ext]['size'] += file_info['size']
    
    sorted_types = sorted(type_stats.items(), key=lambda x: x[1]['size'], reverse=True)
    for ext, stats in sorted_types:
        print(f"{ext:<15} {stats['count']:>5} 个文件  {format_size(stats['size']):>12}")

def main():
    if len(sys.argv) < 2:
        print("使用方法: python find_large_files.py <目录> [最小大小MB] [最大结果数] [文件类型]")
        print("\n示例:")
        print("  python find_large_files.py C:\\ 100 50")
        print("  python find_large_files.py C:\\ 500 30")
        print("  python find_large_files.py C:\\Users 200 100 .mp4,.avi,.mkv")
        print("\n常见大文件类型:")
        print("  视频: .mp4,.avi,.mkv,.mov,.wmv,.flv")
        print("  安装包: .iso,.exe,.msi")
        print("  压缩包: .zip,.rar,.7z")
        print("  数据库: .bak,.sql")
        sys.exit(1)
    
    root_path = sys.argv[1]
    min_size_mb = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    
    # 解析文件类型
    file_types = None
    if len(sys.argv) > 4:
        file_types = [ft.strip() if ft.startswith('.') else f'.{ft.strip()}' 
                     for ft in sys.argv[4].split(',')]
        print(f"文件类型过滤: {', '.join(file_types)}")
    
    if not os.path.exists(root_path):
        print(f"错误: 路径不存在: {root_path}")
        sys.exit(1)
    
    find_large_files(root_path, min_size_mb, max_results, file_types)

if __name__ == "__main__":
    main()
