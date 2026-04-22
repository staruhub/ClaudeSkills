# 模型漂移检测与校准协议

## 什么是模型漂移

模型漂移（Model Drift）：模型的输出行为随时间发生变化，
即使输入不变，输出的质量、风格、准确性也可能偏移。

AI-native产品中漂移不可避免，原因包括：
- 模型提供商的更新（静默升级）
- 上下文积累导致的降智（dumb zone）
- 用户行为模式变化（data drift）
- prompt与模型版本的兼容性变化

---

## 漂移检测四信号

### 信号1: 输出分布偏移
```
监控指标：
- 输出平均长度变化 > 20%
- 特定关键词/短语出现频率异常
- 输出结构（JSON字段、段落数）与基线不符
- 语气/风格评分（用轻量分类器打分）偏移

检测方法：
baseline_distribution = 上线首周的输出统计
current_distribution = 最近24h的输出统计
drift_score = KL_divergence(current, baseline)
if drift_score > threshold: alert()
```

### 信号2: 用户满意度下降
```
监控指标：
- 用户主动纠正/重试比例上升
- 负面反馈增加
- 会话平均轮数增加（用户需要更多轮才能达成目标）
- 功能使用率下降（用户绕开AI自己操作）

检测方法：
daily_satisfaction = aggregate(feedback_scores)
if rolling_7day_avg < threshold: alert()
```

### 信号3: 异常行为增多
```
监控指标：
- 超时比例上升
- 拒答/无法处理比例上升
- 幻觉（输出虚假信息）报告增加
- Agent间通信失败增加

检测方法：
error_rate = errors / total_requests
if error_rate > baseline * 1.5: alert()
```

### 信号4: Agent间不一致
```
监控指标（多专精Agent架构特有）：
- 理解Agent输出的意图 vs 执行Agent实际执行的动作不匹配
- 校验Agent的拒绝率异常上升
- Agent间格式/schema不对齐

检测方法：
mismatch_rate = mismatches / total_pipelines
if mismatch_rate > threshold: alert()
```

---

## 校准协议

### Level 1: 提示词迭代（最快，小时级）

```
触发条件：漂移轻微，输出还在acceptable范围边缘
操作：
1. 分析漂移方向（输出变长/变短？变保守/变激进？）
2. 调整system prompt中的约束
3. A/B测试新旧prompt（至少100个请求）
4. 确认改善后全量切换
```

### Level 2: 模型切换（中等，天级）

```
触发条件：当前模型持续漂移，prompt调整无效
操作：
1. 候选模型列表中选择替代
2. 用行为属性测试集验证
3. 小流量灰度（5% → 20% → 50% → 100%）
4. 持续监控漂移信号
```

### Level 3: 架构调整（最慢，周级）

```
触发条件：多个Agent同时漂移，或用户行为模式发生根本变化
操作：
1. 重新评估行为模式簇
2. 调整Agent分工/新增Agent
3. 更新降级策略
4. 全面回归测试
```

---

## Dumb Zone防护协议

```
监控：tracking context_usage / context_window_size

国模（GLM-5.1等）：
  if context_usage > 0.4: warn("approaching dumb zone")
  if context_usage > 0.5: force_compact()

国际Top2（GPT/Gemini）：
  if context_usage > 0.6: warn("approaching dumb zone")  
  if context_usage > 0.7: force_compact()

compact后：
  验证关键上下文是否保留
  如果丢失关键信息 → 重新注入
```

---

## 行为审计模板

### 日报（自动化）

```markdown
## 行为审计日报 - [日期]

### 请求概况
- 总请求数：[N]
- 成功率：[%]
- 平均响应时间：[ms]

### 漂移检测
- 输出分布漂移分数：[score] (阈值: [threshold])
- 用户满意度（7日滚动）：[score]
- 异常行为比例：[%]
- Agent间不一致率：[%]

### 告警
- [告警列表，如有]

### 建议
- [自动生成的建议，如有]
```

### 周报（人工+自动化）

```markdown
## 行为审计周报 - [日期范围]

### 采样审核
- 采样数量：[N]
- 人工审核数量：[N]
- 质量评分分布：[图表]

### 漂移趋势
- [7日漂移趋势图]
- 是否需要校准：[是/否]

### 行为模式簇覆盖度
- 能归类的请求比例：[%]
- 无法归类的top5新模式：[列表]
- 是否需要新增模式簇：[是/否]

### 成本分析
- 模型路由分布：[大模型X% / 中模型Y% / 小模型Z%]
- 总token消耗：[N]
- 成本优化建议：[如有]
```

---

## 快速启动清单

1. ☐ 定义baseline：上线首周数据作为基线
2. ☐ 部署四信号监控
3. ☐ 设定告警阈值（建议先松后紧）
4. ☐ 建立校准SOP（Level 1/2/3）
5. ☐ 设置dumb zone自动compact
6. ☐ 配置日报自动化
7. ☐ 排定周报人工审核时间
