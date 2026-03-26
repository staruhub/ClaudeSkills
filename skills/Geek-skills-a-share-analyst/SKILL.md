---
name: Geek-skills-a-share-analyst
version: 1.0.0
description: A股专业分析师助手，提供每日股价分析、选股策略和投资建议。适用于：(1) 获取A股实时行情和历史数据，(2) 技术面分析（K线形态、MACD、KDJ、RSI、布林带等），(3) 基本面分析（财务指标、估值分析），(4) 板块热点追踪，(5) 选股策略筛选，(6) 量化因子分析，(7) 生成每日股市分析报告。当用户询问"帮我分析股票"、"今日选股"、"A股行情分析"、"技术分析"、"基本面分析"、"量化选股"等相关问题时触发。
---

# A股分析师 Skill

专业的A股市场分析工具，整合多数据源，提供技术面、基本面综合分析和智能选股策略。

## 数据获取

使用AKShare作为主要数据源（免费、开源、无需token）：

```python
pip install akshare --break-system-packages
```

### 核心数据获取示例

```python
import akshare as ak

# 实时行情
df = ak.stock_zh_a_spot_em()  # 全部A股实时行情

# 历史K线
df = ak.stock_zh_a_hist(symbol="000001", period="daily", adjust="qfq")

# 板块行情
df = ak.stock_board_concept_name_em()  # 概念板块
df = ak.stock_board_industry_name_em()  # 行业板块

# 龙虎榜
df = ak.stock_lhb_detail_em(start_date="20241201", end_date="20241209")

# 资金流向
df = ak.stock_individual_fund_flow(stock="000001", market="sz")
```

## 分析工作流程

### 1. 每日盘前分析

执行顺序：
1. 获取大盘指数（上证、深证、创业板）
2. 分析板块热点轮动
3. 筛选涨停股及连板股
4. 检测北向资金流向
5. 生成今日关注清单

### 2. 技术面分析

对单只股票执行：
1. 获取历史K线数据（至少60日）
2. 计算技术指标（见 `references/technical_indicators.md`）
3. 识别K线形态（见 `references/candlestick_patterns.md`）
4. 判断趋势和支撑/阻力位
5. 生成技术面评分

### 3. 基本面分析

执行顺序：
1. 获取财务数据（营收、净利润、ROE等）
2. 计算估值指标（PE、PB、PS）
3. 分析行业地位和竞争优势
4. 评估成长性和安全边际
5. 生成基本面评分

### 4. 智能选股策略

**策略类型选择：**
- 趋势突破策略 → 执行 `scripts/strategy_breakout.py`
- 价值低估策略 → 执行 `scripts/strategy_value.py`
- 动量因子策略 → 执行 `scripts/strategy_momentum.py`
- 多因子综合策略 → 执行 `scripts/strategy_multi_factor.py`

## 输出格式

### 个股分析报告模板

```markdown
# [股票名称]([股票代码]) 分析报告

## 基本信息
- 当前价格：¥XX.XX（涨跌幅 +X.XX%）
- 市值：XXX亿  |  PE(TTM)：XX.X  |  PB：X.XX

## 技术面分析
- 趋势判断：[上升/震荡/下降]
- 支撑位：¥XX.XX  |  阻力位：¥XX.XX
- 技术指标：MACD [金叉/死叉]  |  KDJ [超买/超卖/中性]  |  RSI [XX]

## 基本面分析
- 营收增速：XX%  |  净利润增速：XX%
- ROE：XX%  |  毛利率：XX%

## 综合评分
- 技术面：⭐⭐⭐⭐☆ (4/5)
- 基本面：⭐⭐⭐☆☆ (3/5)

## 操作建议
[具体建议及风险提示]
```

### 每日选股清单模板

```markdown
# 每日选股清单 [日期]

## 市场概览
- 上证指数：XXXX.XX（+X.XX%）
- 深证成指：XXXXX.XX（+X.XX%）
- 创业板指：XXXX.XX（+X.XX%）

## 热点板块 TOP5
1. [板块名称] +X.XX%
2. ...

## 精选个股

### 趋势突破型
| 代码 | 名称 | 现价 | 涨幅 | 突破形态 | 评分 |
|------|------|------|------|----------|------|
| ... | ... | ... | ... | ... | ... |

### 价值低估型
| 代码 | 名称 | 现价 | PE | PB | 评分 |
|------|------|------|-----|-----|------|
| ... | ... | ... | ... | ... | ... |

## 风险提示
投资有风险，以上分析仅供参考，不构成投资建议。
```

## 关键脚本

- `scripts/fetch_market_data.py` - 市场数据获取
- `scripts/technical_analysis.py` - 技术指标计算
- `scripts/strategy_breakout.py` - 趋势突破选股
- `scripts/strategy_value.py` - 价值投资选股
- `scripts/strategy_momentum.py` - 动量因子选股
- `scripts/strategy_multi_factor.py` - 多因子选股
- `scripts/generate_report.py` - 报告生成

## 参考文档

- `references/technical_indicators.md` - 技术指标计算公式
- `references/candlestick_patterns.md` - K线形态识别
- `references/fundamental_metrics.md` - 基本面指标说明
- `references/factor_library.md` - 量化因子库

## 重要提示

1. **数据延迟**：实时数据可能有15分钟延迟
2. **风险警示**：所有分析仅供参考，不构成投资建议
3. **回测验证**：新策略需先进行历史回测
4. **仓位管理**：建议单只股票仓位不超过总资金20%
