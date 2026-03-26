# Windows C盘清理参考指南

本文档提供Windows系统中常见垃圾文件位置、清理建议和注意事项。

## 📁 常见垃圾文件位置

### 1. 临时文件目录

| 路径 | 说明 | 清理建议 |
|------|------|----------|
| `%TEMP%` | 用户临时文件夹 | 可安全清理 |
| `%TMP%` | 系统临时文件夹 | 可安全清理 |
| `C:\Windows\Temp` | Windows系统临时文件 | 可安全清理 |
| `C:\Windows\Prefetch` | 预读取文件(加速启动) | 不建议清理 |

### 2. 浏览器缓存

| 浏览器 | 缓存路径 | 大小估计 |
|--------|----------|----------|
| Chrome | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache` | 500MB-2GB |
| Edge | `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache` | 500MB-2GB |
| Firefox | `%APPDATA%\Mozilla\Firefox\Profiles\*.default\cache2` | 500MB-1GB |

**注意**: 清理前需要关闭浏览器

### 3. Windows更新文件

| 路径 | 说明 | 清理建议 |
|------|------|----------|
| `C:\Windows\SoftwareDistribution\Download` | 更新下载缓存 | 可清理 |
| `C:\Windows\WinSxS` | 组件存储 | 仅通过DISM清理 |
| `C:\Windows.old` | 旧Windows安装 | 升级后30天可删除 |

**警告**: `WinSxS`目录不要手动删除,应使用:
```bash
DISM.exe /Online /Cleanup-Image /StartComponentCleanup /ResetBase
```

### 4. 系统日志

| 路径 | 说明 | 清理建议 |
|------|------|----------|
| `C:\Windows\Logs` | Windows日志 | 可清理旧日志 |
| `C:\Windows\Panther` | 安装日志 | 安装完成后可清理 |
| `C:\Windows\System32\LogFiles` | 系统服务日志 | 可清理旧日志 |

### 5. 回收站

| 路径 | 说明 |
|------|------|
| `C:\$Recycle.Bin` | C盘回收站 |
| `D:\$Recycle.Bin` | D盘回收站 |

**提示**: 每个磁盘都有独立的回收站

### 6. 休眠文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `C:\hiberfil.sys` | 等于内存大小 | 休眠数据文件 |
| `C:\pagefile.sys` | 根据设置 | 虚拟内存文件 |

**注意**: 这些是系统文件,不建议删除。可通过系统设置调整大小。

## 🛡️ 不应删除的目录

以下目录包含重要系统文件,**绝对不要删除**:

- `C:\Windows\System32` - 核心系统文件
- `C:\Windows\WinSxS` - Windows组件存储
- `C:\Program Files` - 已安装程序
- `C:\Program Files (x86)` - 32位程序
- `C:\ProgramData` - 程序数据
- `C:\Users\[用户名]\AppData\Roaming` - 用户配置

## 📊 空间占用分析

### 典型C盘空间分配

| 组件 | 占用空间 | 说明 |
|------|----------|------|
| Windows系统 | 20-30GB | 取决于版本 |
| WinSxS | 5-10GB | 组件存储 |
| 休眠文件 | 内存大小 | 可禁用 |
| 虚拟内存 | 根据设置 | 可调整 |
| 程序文件 | 10-50GB | 取决于安装量 |
| 用户数据 | 变动 | 文档、下载等 |

### 释放空间的优先级

1. **高优先级** (安全且效果明显)
   - 清理临时文件
   - 清理回收站
   - 清理浏览器缓存
   - 卸载不需要的程序

2. **中优先级** (需要谨慎)
   - 清理旧的Windows更新
   - 清理系统日志
   - 转移用户文件到其他盘

3. **低优先级** (专业操作)
   - DISM清理组件存储
   - 禁用休眠
   - 调整虚拟内存

## 🔧 常用清理命令

### 磁盘清理工具
```cmd
cleanmgr /sageset:1  # 配置清理选项
cleanmgr /sagerun:1  # 执行清理
```

### DISM清理
```cmd
DISM.exe /Online /Cleanup-Image /StartComponentCleanup
DISM.exe /Online /Cleanup-Image /StartComponentCleanup /ResetBase
```

### 禁用休眠
```cmd
powercfg -h off  # 禁用休眠,删除hiberfil.sys
```

### 查看磁盘空间
```cmd
dir /s C:\  # 递归显示所有文件
```

## ⚠️ 安全注意事项

1. **备份重要数据**: 清理前务必备份
2. **关闭程序**: 清理前关闭相关程序
3. **管理员权限**: 某些操作需要管理员权限
4. **测试模式**: 先用模拟模式测试,确认后再执行
5. **系统还原点**: 建议创建系统还原点

## 🎯 清理最佳实践

### 定期清理计划

| 频率 | 清理内容 |
|------|----------|
| 每周 | 临时文件、回收站 |
| 每月 | 浏览器缓存、下载文件夹 |
| 每季度 | 系统更新清理、大文件整理 |
| 每年 | 全面清理、磁盘整理 |

### 预防措施

1. **下载位置**: 将下载文件夹设置到其他盘
2. **程序安装**: 尽量安装到D盘
3. **用户文件**: 文档、图片等转移到其他盘
4. **监控工具**: 使用磁盘空间监控工具
5. **定期检查**: 定期检查大文件和重复文件

## 📝 文件扩展名参考

### 可能的垃圾文件类型

| 扩展名 | 说明 | 清理建议 |
|--------|------|----------|
| `.tmp` | 临时文件 | 可删除 |
| `.log` | 日志文件 | 旧日志可删除 |
| `.bak` | 备份文件 | 确认后可删除 |
| `.old` | 旧文件 | 确认后可删除 |
| `.cache` | 缓存文件 | 可删除 |
| `.dmp` | 转储文件 | 可删除 |

### 大文件类型

| 类型 | 扩展名 | 典型大小 |
|------|--------|----------|
| 视频 | `.mp4, .avi, .mkv, .mov` | 500MB-5GB |
| 镜像 | `.iso, .img` | 2GB-8GB |
| 安装包 | `.exe, .msi` | 100MB-2GB |
| 压缩包 | `.zip, .rar, .7z` | 变动 |
| 数据库 | `.bak, .sql` | 100MB+ |

## 🔍 高级技巧

### PowerShell脚本示例

**查找30天未访问的大文件**:
```powershell
Get-ChildItem C:\ -Recurse -File | 
Where-Object {$_.Length -gt 100MB -and $_.LastAccessTime -lt (Get-Date).AddDays(-30)} | 
Sort-Object Length -Descending | 
Select-Object FullName, @{N='Size(MB)';E={$_.Length/1MB}}, LastAccessTime
```

**查找重复文件**:
```powershell
Get-ChildItem C:\Users -Recurse -File | 
Group-Object Length | 
Where-Object {$_.Count -gt 1}
```

### 使用存储感知

Windows 10/11自带存储感知功能:
1. 设置 -> 系统 -> 存储
2. 启用"存储感知"
3. 配置自动清理规则

## 📚 资源链接

- [Microsoft官方磁盘清理指南](https://support.microsoft.com/windows)
- [DISM命令参考](https://docs.microsoft.com/windows-hardware/manufacture/desktop/dism)
- [磁盘清理最佳实践](https://docs.microsoft.com/troubleshoot/windows-server/backup-and-storage/disk-cleanup-tool)
