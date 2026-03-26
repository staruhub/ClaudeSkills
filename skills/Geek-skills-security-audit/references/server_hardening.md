# 服务器安全加固指南

## SSH安全配置

### /etc/ssh/sshd_config 推荐配置

```bash
# 禁止root登录
PermitRootLogin no

# 禁止密码认证，只允许密钥
PasswordAuthentication no
PubkeyAuthentication yes

# 限制登录用户
AllowUsers deploy admin

# 修改默认端口
Port 2222

# 禁止空密码
PermitEmptyPasswords no

# 设置登录超时
LoginGraceTime 60

# 限制最大认证尝试次数
MaxAuthTries 3

# 禁止X11转发
X11Forwarding no

# 禁止TCP转发
AllowTcpForwarding no

# 客户端活动检测
ClientAliveInterval 300
ClientAliveCountMax 2

# 使用协议2
Protocol 2

# 禁止用户环境
PermitUserEnvironment no
```

### 应用配置

```bash
# 备份原配置
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# 验证配置
sudo sshd -t

# 重启SSH服务
sudo systemctl restart sshd
```

---

## 防火墙配置

### UFW (Ubuntu)

```bash
# 启用UFW
sudo ufw enable

# 默认策略：拒绝入站，允许出站
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 允许SSH（如果改了端口记得修改）
sudo ufw allow 2222/tcp

# 允许HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 限制SSH连接速率
sudo ufw limit 2222/tcp

# 查看状态
sudo ufw status verbose
```

### iptables

```bash
# 清空现有规则
sudo iptables -F
sudo iptables -X

# 默认策略
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# 允许环回接口
sudo iptables -A INPUT -i lo -j ACCEPT

# 允许已建立的连接
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 允许SSH
sudo iptables -A INPUT -p tcp --dport 2222 -j ACCEPT

# 允许HTTP/HTTPS
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 防止SYN洪水
sudo iptables -A INPUT -p tcp --syn -m limit --limit 1/s -j ACCEPT

# 保存规则
sudo iptables-save > /etc/iptables/rules.v4
```

---

## 用户权限管理

### 创建非root用户

```bash
# 创建deploy用户
sudo adduser deploy

# 添加到sudo组
sudo usermod -aG sudo deploy

# 配置sudo无密码（可选，仅限自动化场景）
echo "deploy ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/deploy
```

### 配置SSH密钥

```bash
# 在本地生成密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥到服务器
ssh-copy-id -i ~/.ssh/id_ed25519.pub -p 2222 deploy@server

# 设置权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

---

## 文件系统安全

### 检查危险权限

```bash
# 查找SUID文件
sudo find / -perm -4000 -type f 2>/dev/null

# 查找SGID文件
sudo find / -perm -2000 -type f 2>/dev/null

# 查找world-writable文件
sudo find / -perm -002 -type f 2>/dev/null

# 查找无主文件
sudo find / -nouser -o -nogroup 2>/dev/null

# 查找.rhosts文件
sudo find / -name ".rhosts" 2>/dev/null
```

### 关键目录权限

```bash
# /etc权限
sudo chmod 755 /etc
sudo chmod 644 /etc/passwd
sudo chmod 640 /etc/shadow
sudo chmod 644 /etc/group

# 用户目录
sudo chmod 700 /home/*

# 临时目录设置sticky bit
sudo chmod 1777 /tmp
sudo chmod 1777 /var/tmp
```

### 挂载选项安全

编辑 `/etc/fstab`:
```
/tmp     tmpfs   defaults,noexec,nosuid,nodev   0 0
/var/tmp tmpfs   defaults,noexec,nosuid,nodev   0 0
```

---

## 系统更新与补丁

### 自动安全更新

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades

# 配置 /etc/apt/apt.conf.d/50unattended-upgrades
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
};
```

### 手动更新

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 检查待重启的服务
sudo needrestart -r a
```

---

## 日志与审计

### 配置auditd

```bash
# 安装auditd
sudo apt install auditd audispd-plugins

# 启用服务
sudo systemctl enable auditd
sudo systemctl start auditd

# 添加审计规则 /etc/audit/rules.d/audit.rules
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/gshadow -p wa -k identity
-w /etc/sudoers -p wa -k sudoers
-w /var/log/auth.log -p wa -k auth_log

# 重载规则
sudo auditctl -R /etc/audit/rules.d/audit.rules
```

### 配置日志轮转

```bash
# /etc/logrotate.d/security
/var/log/security.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root adm
}
```

### 集中日志

```bash
# rsyslog配置发送到远程服务器
*.* @logserver.example.com:514
```

---

## Fail2ban配置

```bash
# 安装
sudo apt install fail2ban

# 创建本地配置
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```

编辑 `/etc/fail2ban/jail.local`:
```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
destemail = admin@example.com
action = %(action_mwl)s

[sshd]
enabled = true
port = 2222
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
port = http,https
logpath = /var/log/nginx/error.log
```

---

## 网络安全

### 禁用不需要的服务

```bash
# 列出运行的服务
systemctl list-units --type=service --state=running

# 禁用不需要的服务
sudo systemctl disable cups
sudo systemctl disable avahi-daemon
sudo systemctl disable bluetooth
```

### 内核参数加固

编辑 `/etc/sysctl.conf`:
```bash
# 禁用IP转发
net.ipv4.ip_forward = 0

# 禁用ICMP重定向
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0

# 禁用源路由
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0

# 启用SYN cookies
net.ipv4.tcp_syncookies = 1

# 忽略广播ping
net.ipv4.icmp_echo_ignore_broadcasts = 1

# 日志可疑包
net.ipv4.conf.all.log_martians = 1

# 启用反向路径过滤
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
```

应用配置：
```bash
sudo sysctl -p
```

---

## Docker安全

### Docker守护进程加固

编辑 `/etc/docker/daemon.json`:
```json
{
  "icc": false,
  "userns-remap": "default",
  "no-new-privileges": true,
  "seccomp-profile": "/etc/docker/seccomp/default.json",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}
```

### 容器运行安全

```bash
# 非root用户运行
docker run --user 1000:1000 image

# 只读文件系统
docker run --read-only image

# 限制资源
docker run --memory=512m --cpus=0.5 image

# 删除所有capabilities
docker run --cap-drop ALL image

# 禁止权限提升
docker run --security-opt=no-new-privileges image
```

---

## 安全检查清单

### 每日检查
- [ ] 查看认证日志 `/var/log/auth.log`
- [ ] 检查fail2ban状态
- [ ] 监控系统资源使用

### 每周检查
- [ ] 系统安全更新
- [ ] 检查用户账户
- [ ] 审查sudo日志
- [ ] 扫描rootkit

### 每月检查
- [ ] 完整系统审计
- [ ] 密钥轮换
- [ ] 证书检查
- [ ] 备份验证

### 每季度检查
- [ ] 渗透测试
- [ ] 安全策略审查
- [ ] 灾难恢复演练
