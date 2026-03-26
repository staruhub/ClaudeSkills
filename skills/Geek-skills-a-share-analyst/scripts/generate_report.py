#!/usr/bin/env python3
"""
A股分析报告生成模块
生成个股分析报告和每日市场报告
"""

import akshare as ak
import pandas as pd
from datetime import datetime
from technical_analysis import analyze_stock


def generate_stock_report(symbol: str) -> str:
    """
    生成个股分析报告
    
    Args:
        symbol: 股票代码，如 "000001"
    """
    # 获取股票基本信息
    try:
        info = ak.stock_individual_info_em(symbol=symbol)
        info_dict = dict(zip(info['item'], info['value']))
    except:
        info_dict = {}
    
    # 获取实时行情
    spot = ak.stock_zh_a_spot_em()
    stock_spot = spot[spot['代码'] == symbol]
    if len(stock_spot) == 0:
        return f"未找到股票代码: {symbol}"
    stock_spot = stock_spot.iloc[0]
    
    # 获取历史K线
    df = ak.stock_zh_a_hist(symbol=symbol, period="daily", adjust="qfq")
    df = df.tail(120)
    
    # 技术分析
    analysis = analyze_stock(df)
    
    # 生成报告
    report = f"""
# {stock_spot['名称']}({symbol}) 分析报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 基本信息

| 项目 | 数值 |
|------|------|
| 当前价格 | ¥{stock_spot['最新价']} |
| 涨跌幅 | {stock_spot['涨跌幅']:+.2f}% |
| 成交量 | {stock_spot['成交量']/10000:.2f}万手 |
| 成交额 | {stock_spot['成交额']/100000000:.2f}亿 |
| 换手率 | {stock_spot['换手率']:.2f}% |
| 量比 | {stock_spot['量比']:.2f} |
| 市盈率(动态) | {stock_spot['市盈率-动态']:.2f} |
| 市净率 | {stock_spot['市净率']:.2f} |
| 总市值 | {stock_spot['总市值']/100000000:.2f}亿 |
| 流通市值 | {stock_spot['流通市值']/100000000:.2f}亿 |

---

## 技术面分析

### 趋势判断
- **当前趋势**: {analysis['trend']}
- **支撑位**: ¥{analysis['support_resistance']['support']}
- **阻力位**: ¥{analysis['support_resistance']['resistance']}
- **枢轴点**: ¥{analysis['support_resistance']['pivot']}

### 技术指标

| 指标 | 数值 | 信号 |
|------|------|------|
| MACD | DIF={analysis['indicators']['MACD']['DIF']:.4f}, DEA={analysis['indicators']['MACD']['DEA']:.4f} | {analysis['indicators']['MACD']['signal']} |
| KDJ | K={analysis['indicators']['KDJ']['K']:.2f}, D={analysis['indicators']['KDJ']['D']:.2f}, J={analysis['indicators']['KDJ']['J']:.2f} | {analysis['indicators']['KDJ']['signal']} |
| RSI(14) | {analysis['indicators']['RSI']['value']:.2f} | {analysis['indicators']['RSI']['signal']} |
| BOLL | 上轨={analysis['indicators']['BOLL']['upper']:.2f}, 中轨={analysis['indicators']['BOLL']['mid']:.2f}, 下轨={analysis['indicators']['BOLL']['lower']:.2f} | {analysis['indicators']['BOLL']['signal']} |
| ATR(14) | {analysis['indicators']['ATR']:.2f} | 波动参考 |

---

## 综合评分

- **技术评分**: {analysis['score']['score']}/100
- **评级**: {analysis['score']['rating']}
- **星级**: {'⭐' * analysis['score']['stars']}

---

## 操作建议

"""
    
    score = analysis['score']['score']
    if score >= 70:
        report += """
✅ **建议买入**

当前技术面表现良好，各项指标偏多，可考虑逢低布局。

**注意事项**:
- 建议分批建仓，控制单只股票仓位不超过20%
- 设置止损位在支撑位下方3-5%
- 关注成交量变化，无量上涨需谨慎
"""
    elif score >= 50:
        report += """
⚠️ **建议观望**

当前技术面处于震荡整理阶段，方向不明确。

**注意事项**:
- 等待趋势明朗后再做决策
- 关注是否突破关键支撑/阻力位
- 可设置价格提醒，突破后再介入
"""
    else:
        report += """
❌ **建议回避**

当前技术面偏弱，多项指标发出卖出信号。

**注意事项**:
- 如持有建议逢高减仓
- 等待企稳信号出现后再考虑
- 关注下方支撑位是否有效
"""
    
    report += """
---

## 风险提示

⚠️ **免责声明**: 以上分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。请根据自身风险承受能力做出投资决策。
"""
    
    return report


def generate_market_report() -> str:
    """生成每日市场报告"""
    
    # 获取指数数据
    indices = {
        '上证指数': 'sh000001',
        '深证成指': 'sz399001',
        '创业板指': 'sz399006',
    }
    
    index_data = []
    for name, code in indices.items():
        df = ak.stock_zh_index_daily(symbol=code)
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        change = (latest['close'] - prev['close']) / prev['close'] * 100
        index_data.append({
            'name': name,
            'close': latest['close'],
            'change': change,
            'volume': latest['volume'] / 1e8
        })
    
    # 获取板块数据
    concept_boards = ak.stock_board_concept_name_em()
    industry_boards = ak.stock_board_industry_name_em()
    
    top_concept = concept_boards.nlargest(5, '涨跌幅')
    bottom_concept = concept_boards.nsmallest(5, '涨跌幅')
    top_industry = industry_boards.nlargest(5, '涨跌幅')
    
    # 获取涨跌停数据
    try:
        zt_count = len(ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d')))
    except:
        zt_count = "N/A"
    
    try:
        dt_count = len(ak.stock_zt_pool_dtgc_em(date=datetime.now().strftime('%Y%m%d')))
    except:
        dt_count = "N/A"
    
    report = f"""
# 每日市场报告

**日期**: {datetime.now().strftime('%Y-%m-%d')}
**生成时间**: {datetime.now().strftime('%H:%M:%S')}

---

## 大盘指数

| 指数 | 收盘点位 | 涨跌幅 | 成交额(亿) |
|------|----------|--------|------------|
"""
    
    for idx in index_data:
        report += f"| {idx['name']} | {idx['close']:.2f} | {idx['change']:+.2f}% | {idx['volume']:.2f} |\n"
    
    report += f"""
---

## 市场情绪

- **涨停家数**: {zt_count}
- **跌停家数**: {dt_count}

---

## 热门概念板块 TOP5

| 排名 | 板块名称 | 涨跌幅 | 成交额(亿) |
|------|----------|--------|------------|
"""
    
    for i, (_, row) in enumerate(top_concept.iterrows(), 1):
        report += f"| {i} | {row['板块名称']} | {row['涨跌幅']:+.2f}% | {row['成交额']/1e8:.2f} |\n"
    
    report += f"""
---

## 热门行业板块 TOP5

| 排名 | 板块名称 | 涨跌幅 | 成交额(亿) |
|------|----------|--------|------------|
"""
    
    for i, (_, row) in enumerate(top_industry.iterrows(), 1):
        report += f"| {i} | {row['板块名称']} | {row['涨跌幅']:+.2f}% | {row['成交额']/1e8:.2f} |\n"
    
    report += f"""
---

## 跌幅居前概念板块 TOP5

| 排名 | 板块名称 | 涨跌幅 |
|------|----------|--------|
"""
    
    for i, (_, row) in enumerate(bottom_concept.iterrows(), 1):
        report += f"| {i} | {row['板块名称']} | {row['涨跌幅']:+.2f}% |\n"
    
    report += """
---

## 市场总结

"""
    
    # 简单判断市场情绪
    sh_change = index_data[0]['change']
    if sh_change > 1:
        report += "📈 **市场情绪**: 今日市场表现强势，做多情绪高涨。建议关注热点板块龙头，把握短线机会。\n"
    elif sh_change > 0:
        report += "📊 **市场情绪**: 今日市场小幅上涨，整体偏暖。可适度参与，但需控制仓位。\n"
    elif sh_change > -1:
        report += "📉 **市场情绪**: 今日市场小幅调整，情绪偏谨慎。建议观望为主，等待企稳信号。\n"
    else:
        report += "⚠️ **市场情绪**: 今日市场大幅下跌，恐慌情绪蔓延。建议控制仓位，防范风险。\n"
    
    report += """
---

## 风险提示

⚠️ **免责声明**: 以上分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。
"""
    
    return report


if __name__ == "__main__":
    # 生成市场报告
    print(generate_market_report())
    
    print("\n" + "="*60 + "\n")
    
    # 生成个股报告示例
    print(generate_stock_report("000001"))
