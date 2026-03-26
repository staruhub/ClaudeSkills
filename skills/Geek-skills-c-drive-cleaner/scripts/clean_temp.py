#!/usr/bin/env python3
"""
清理Windows系统的临时文件、缓存和垃圾文件
"""
import os
import sys
import shutil
from pathlib import Path
import tempfile

def format_size(size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def safe_remove(path, dry_run=True):
    """
    安全删除文件或目录
    
    Args:
        path: 要删除的路径
        dry_run: 如果为True,只模拟删除不实际删除
    
    Returns:
        删除的字节数
    """
    try:
        size = 0
        if os.path.isfile(path):
            size = os.path.getsize(path)
            if not dry_run:
                os.remove(path)
            return size
        elif os.path.isdir(path):
            # 计算目录大小
            for root, dirs, files in os.walk(path):
                for f in files:
                    try:
                        size += os.path.getsize(os.path.join(root, f))
                    except:
                        pass
            if not dry_run:
                shutil.rmtree(path, ignore_errors=True)
            return size
    except (PermissionError, FileNotFoundError, OSError):
        return 0

def clean_temp_files(dry_run=True):
    """清理Windows临时文件"""
    print("\n" + "=" * 80)
    print("🗑️  清理临时文件")
    print("=" * 80)
    
    temp_locations = [
        os.environ.get('TEMP', 'C:\\Windows\\Temp'),
        os.environ.get('TMP', 'C:\\Windows\\Temp'),
        'C:\\Windows\\Temp',
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
    ]
    
    total_freed = 0
    file_count = 0
    
    for temp_dir in set(temp_locations):  # 去重
        if not os.path.exists(temp_dir):
            continue
        
        print(f"\n扫描: {temp_dir}")
        try:
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    size = safe_remove(item_path, dry_run)
                    if size > 0:
                        total_freed += size
                        file_count += 1
                        if size > 10 * 1024 * 1024:  # 只显示大于10MB的项
                            print(f"  {'[模拟]' if dry_run else '[删除]'} {format_size(size):>12} - {item}")
                except (PermissionError, OSError) as e:
                    continue
        except (PermissionError, OSError):
            print(f"  无权限访问此目录")
            continue
    
    print(f"\n✅ 临时文件清理完成:")
    print(f"   文件/目录数: {file_count}")
    print(f"   释放空间: {format_size(total_freed)}")
    return total_freed

def clean_recycle_bin(dry_run=True):
    """清理回收站"""
    print("\n" + "=" * 80)
    print("🗑️  清理回收站")
    print("=" * 80)
    
    # Windows回收站路径
    recycle_paths = []
    
    # 检查所有驱动器的回收站
    for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        recycle_path = f"{drive}:\\$Recycle.Bin"
        if os.path.exists(recycle_path):
            recycle_paths.append(recycle_path)
    
    total_freed = 0
    file_count = 0
    
    for recycle_dir in recycle_paths:
        print(f"\n扫描: {recycle_dir}")
        try:
            for root, dirs, files in os.walk(recycle_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        size = safe_remove(file_path, dry_run)
                        total_freed += size
                        file_count += 1
                    except:
                        continue
        except (PermissionError, OSError):
            print(f"  无权限访问此目录")
            continue
    
    print(f"\n✅ 回收站清理完成:")
    print(f"   文件数: {file_count}")
    print(f"   释放空间: {format_size(total_freed)}")
    return total_freed

def clean_browser_cache(dry_run=True):
    """清理浏览器缓存"""
    print("\n" + "=" * 80)
    print("🌐 清理浏览器缓存")
    print("=" * 80)
    
    localappdata = os.environ.get('LOCALAPPDATA', '')
    
    cache_locations = {
        'Chrome': os.path.join(localappdata, 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
        'Edge': os.path.join(localappdata, 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
        'Firefox': os.path.join(os.environ.get('APPDATA', ''), 'Mozilla', 'Firefox', 'Profiles'),
    }
    
    total_freed = 0
    
    for browser, cache_path in cache_locations.items():
        if not os.path.exists(cache_path):
            continue
        
        print(f"\n清理 {browser} 缓存: {cache_path}")
        try:
            if browser == 'Firefox':
                # Firefox有多个配置文件
                for profile in os.listdir(cache_path):
                    profile_cache = os.path.join(cache_path, profile, 'cache2')
                    if os.path.exists(profile_cache):
                        size = safe_remove(profile_cache, dry_run)
                        total_freed += size
                        print(f"  {'[模拟]' if dry_run else '[删除]'} {format_size(size)}")
            else:
                size = safe_remove(cache_path, dry_run)
                total_freed += size
                print(f"  {'[模拟]' if dry_run else '[删除]'} {format_size(size)}")
        except (PermissionError, OSError) as e:
            print(f"  无权限或浏览器正在运行")
            continue
    
    print(f"\n✅ 浏览器缓存清理完成:")
    print(f"   释放空间: {format_size(total_freed)}")
    return total_freed

def clean_windows_logs(dry_run=True):
    """清理Windows日志文件"""
    print("\n" + "=" * 80)
    print("📝 清理系统日志")
    print("=" * 80)
    
    log_locations = [
        'C:\\Windows\\Logs',
        'C:\\Windows\\Panther',
        'C:\\Windows\\System32\\LogFiles',
    ]
    
    total_freed = 0
    file_count = 0
    
    for log_dir in log_locations:
        if not os.path.exists(log_dir):
            continue
        
        print(f"\n扫描: {log_dir}")
        try:
            for root, dirs, files in os.walk(log_dir):
                for file in files:
                    if file.endswith(('.log', '.etl', '.old')):
                        file_path = os.path.join(root, file)
                        try:
                            size = safe_remove(file_path, dry_run)
                            if size > 10 * 1024 * 1024:  # 只显示大于10MB的日志
                                total_freed += size
                                file_count += 1
                                print(f"  {'[模拟]' if dry_run else '[删除]'} {format_size(size):>12} - {file}")
                        except:
                            continue
        except (PermissionError, OSError):
            print(f"  无权限访问此目录")
            continue
    
    print(f"\n✅ 系统日志清理完成:")
    print(f"   文件数: {file_count}")
    print(f"   释放空间: {format_size(total_freed)}")
    return total_freed

def main():
    print("=" * 80)
    print("🧹 C盘清理大师")
    print("=" * 80)
    
    # 解析命令行参数
    dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        dry_run = False
        print("\n⚠️  警告: 将实际删除文件!")
        response = input("确认继续? (输入 YES 继续): ")
        if response != 'YES':
            print("已取消操作")
            sys.exit(0)
    else:
        print("\n💡 提示: 当前为模拟模式,不会实际删除文件")
        print("   使用 --execute 参数执行实际清理")
    
    # 执行清理
    total = 0
    total += clean_temp_files(dry_run)
    total += clean_recycle_bin(dry_run)
    total += clean_browser_cache(dry_run)
    total += clean_windows_logs(dry_run)
    
    # 总结
    print("\n" + "=" * 80)
    print("📊 清理总结")
    print("=" * 80)
    print(f"总计可释放空间: {format_size(total)}")
    
    if dry_run:
        print("\n💡 这是模拟运行,没有实际删除任何文件")
        print("   使用 --execute 参数执行实际清理")

if __name__ == "__main__":
    main()
