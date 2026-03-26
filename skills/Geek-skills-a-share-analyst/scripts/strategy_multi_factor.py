#!/usr/bin/env python3
"""
A股多因子选股策略
支持价值、成长、动量、质量等多种因子
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_stock_pool():
    """获取股票池（全部A股实时行情）"""
    df = ak.stock_zh_a_spot_em()
    
    # 基础筛选
    df = df[~df['名称'].str.contains('ST|退')]  # 剔除ST和退市股
    df = df[df['涨跌幅'] < 9.9]  # 剔除涨停
    df = df[df['涨跌幅'] > -9.9]  # 剔除跌停
    df = df[df['换手率'] > 0]  # 剔除停牌
    df = df[df['市盈率-动态'] > 0]  # 剔除亏损股（可选）
    
    return df


def strategy_value(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    """
    价值投资策略
    选股逻辑：低PE、低PB、高股息率
    """
    df = df.copy()
    
    # 计算因子排名（越小越好）
    df['PE_rank'] = df['市盈率-动态'].rank(pct=True)
    df['PB_rank'] = df['市净率'].rank(pct=True)
    
    # 综合评分
    df['value_score'] = df['PE_rank'] * 0.5 + df['PB_rank'] * 0.5
    
    # 排序选股
    result = df.nsmallest(top_n, 'value_score')
    
    return result[['代码', '名称', '最新价', '涨跌幅', '市盈率-动态', '市净率', 'value_score']]


def strategy_momentum(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    """
    动量策略
    选股逻辑：近期涨幅居前、成交活跃
    """
    df = df.copy()
    
    # 动量因子（涨幅越大越好）
    df['momentum_rank'] = df['涨跌幅'].rank(pct=True, ascending=False)
    
    # 换手率因子（适度活跃）
    df['turnover_rank'] = df['换手率'].rank(pct=True)
    
    # 综合评分
    df['momentum_score'] = df['momentum_rank'] * 0.7 + df['turnover_rank'] * 0.3
    
    # 排序选股
    result = df.nsmallest(top_n, 'momentum_score')
    
    return result[['代码', '名称', '最新价', '涨跌幅', '换手率', '成交额', 'momentum_score']]


def strategy_breakout(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    """
    突破策略
    选股逻辑：放量突破、近期强势
    """
    df = df.copy()
    
    # 量比因子（放量）
    df['vol_ratio_rank'] = df['量比'].rank(pct=True, ascending=False)
    
    # 涨幅因子
    df['change_rank'] = df['涨跌幅'].rank(pct=True, ascending=False)
    
    # 振幅因子（波动适中）
    df['amplitude_rank'] = df['振幅'].rank(pct=True)
    
    # 综合评分
    df['breakout_score'] = (df['vol_ratio_rank'] * 0.4 + 
                           df['change_rank'] * 0.4 + 
                           df['amplitude_rank'] * 0.2)
    
    # 额外筛选：量比>1.5，涨幅>2%
    df = df[(df['量比'] > 1.5) & (df['涨跌幅'] > 2)]
    
    result = df.nsmallest(top_n, 'breakout_score')
    
    return result[['代码', '名称', '最新价', '涨跌幅', '量比', '振幅', 'breakout_score']]


def strategy_quality(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    """
    质量因子策略
    选股逻辑：高ROE、低负债、稳定增长
    注意：此策略需要额外获取财务数据
    """
    df = df.copy()
    
    # 简化版：使用市盈率和市净率推算ROE
    # ROE ≈ 1 / (PE × PB)
    df['implied_roe'] = 1 / (df['市盈率-动态'] * df['市净率'] + 0.01)
    df['roe_rank'] = df['implied_roe'].rank(pct=True, ascending=False)
    
    # 市值因子（中大盘）
    df['cap_rank'] = df['总市值'].rank(pct=True)
    
    # 综合评分
    df['quality_score'] = df['roe_rank'] * 0.7 + df['cap_rank'] * 0.3
    
    result = df.nsmallest(top_n, 'quality_score')
    
    return result[['代码', '名称', '最新价', '涨跌幅', '市盈率-动态', '市净率', 'implied_roe', 'quality_score']]


def strategy_multi_factor(df: pd.DataFrame, top_n: int = 30,
                         weights: dict = None) -> pd.DataFrame:
    """
    多因子综合策略
    
    Args:
        df: 股票数据
        top_n: 选股数量
        weights: 因子权重配置
    """
    if weights is None:
        weights = {
            'value': 0.25,      # 价值因子
            'momentum': 0.25,   # 动量因子
            'quality': 0.25,    # 质量因子
            'size': 0.15,       # 规模因子
            'volatility': 0.10  # 波动率因子
        }
    
    df = df.copy()
    
    # 价值因子
    df['pe_rank'] = df['市盈率-动态'].rank(pct=True)
    df['pb_rank'] = df['市净率'].rank(pct=True)
    df['value_factor'] = (df['pe_rank'] + df['pb_rank']) / 2
    
    # 动量因子
    df['momentum_factor'] = df['涨跌幅'].rank(pct=True, ascending=False)
    
    # 质量因子（隐含ROE）
    df['implied_roe'] = 1 / (df['市盈率-动态'] * df['市净率'] + 0.01)
    df['quality_factor'] = df['implied_roe'].rank(pct=True, ascending=False)
    
    # 规模因子（偏好中盘）
    df['log_cap'] = np.log(df['总市值'])
    median_cap = df['log_cap'].median()
    df['size_factor'] = -abs(df['log_cap'] - median_cap)
    df['size_factor'] = df['size_factor'].rank(pct=True, ascending=False)
    
    # 波动率因子（偏好低波动）
    df['volatility_factor'] = df['振幅'].rank(pct=True)
    
    # 综合评分
    df['total_score'] = (
        df['value_factor'] * weights['value'] +
        df['momentum_factor'] * weights['momentum'] +
        df['quality_factor'] * weights['quality'] +
        df['size_factor'] * weights['size'] +
        df['volatility_factor'] * weights['volatility']
    )
    
    # 排序选股
    result = df.nsmallest(top_n, 'total_score')
    
    return result[['代码', '名称', '最新价', '涨跌幅', '市盈率-动态', '市净率', 
                  '换手率', '总市值', 'total_score']]


def get_board_leaders(board_type: str = "concept", top_n: int = 5) -> pd.DataFrame:
    """
    获取板块龙头股
    
    Args:
        board_type: concept/industry
        top_n: 每个板块取前N只
    """
    if board_type == "concept":
        boards = ak.stock_board_concept_name_em()
    else:
        boards = ak.stock_board_industry_name_em()
    
    # 取涨幅前10的板块
    top_boards = boards.nlargest(10, '涨跌幅')
    
    results = []
    for _, board in top_boards.iterrows():
        board_name = board['板块名称']
        try:
            if board_type == "concept":
                stocks = ak.stock_board_concept_cons_em(symbol=board_name)
            else:
                stocks = ak.stock_board_industry_cons_em(symbol=board_name)
            
            stocks = stocks.nlargest(top_n, '涨跌幅')
            stocks['所属板块'] = board_name
            stocks['板块涨幅'] = board['涨跌幅']
            results.append(stocks)
        except:
            continue
    
    if results:
        return pd.concat(results, ignore_index=True)
    return pd.DataFrame()


def generate_daily_picks(save_path: str = None) -> dict:
    """
    生成每日选股清单
    """
    print("正在获取股票数据...")
    df = get_stock_pool()
    
    print("运行价值策略...")
    value_picks = strategy_value(df)
    
    print("运行动量策略...")
    momentum_picks = strategy_momentum(df)
    
    print("运行突破策略...")
    breakout_picks = strategy_breakout(df)
    
    print("运行多因子策略...")
    multi_factor_picks = strategy_multi_factor(df)
    
    results = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'value': value_picks,
        'momentum': momentum_picks,
        'breakout': breakout_picks,
        'multi_factor': multi_factor_picks
    }
    
    if save_path:
        # 保存到Excel
        with pd.ExcelWriter(save_path) as writer:
            value_picks.to_excel(writer, sheet_name='价值型', index=False)
            momentum_picks.to_excel(writer, sheet_name='动量型', index=False)
            breakout_picks.to_excel(writer, sheet_name='突破型', index=False)
            multi_factor_picks.to_excel(writer, sheet_name='多因子', index=False)
        print(f"选股结果已保存至: {save_path}")
    
    return results


if __name__ == "__main__":
    results = generate_daily_picks()
    
    print("\n" + "="*60)
    print(f"每日选股清单 - {results['date']}")
    print("="*60)
    
    print("\n【价值型选股 TOP10】")
    print(results['value'].head(10).to_string(index=False))
    
    print("\n【动量型选股 TOP10】")
    print(results['momentum'].head(10).to_string(index=False))
    
    print("\n【突破型选股 TOP10】")
    if len(results['breakout']) > 0:
        print(results['breakout'].head(10).to_string(index=False))
    else:
        print("今日无符合条件的突破型股票")
    
    print("\n【多因子选股 TOP10】")
    print(results['multi_factor'].head(10).to_string(index=False))
