#!/usr/bin/env python3
"""
A股技术分析模块
包含常用技术指标计算和信号判断
"""

import pandas as pd
import numpy as np


def calc_ma(close: pd.Series, periods: list = [5, 10, 20, 60, 120]) -> pd.DataFrame:
    """计算移动平均线"""
    ma_df = pd.DataFrame(index=close.index)
    for p in periods:
        ma_df[f'MA{p}'] = close.rolling(window=p).mean()
    return ma_df


def calc_ema(close: pd.Series, period: int = 12) -> pd.Series:
    """计算指数移动平均"""
    return close.ewm(span=period, adjust=False).mean()


def calc_macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    """计算MACD指标"""
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd = (dif - dea) * 2
    
    return {
        'DIF': dif,
        'DEA': dea,
        'MACD': macd,
        'signal': get_macd_signal(dif, dea)
    }


def get_macd_signal(dif: pd.Series, dea: pd.Series) -> str:
    """判断MACD信号"""
    if len(dif) < 2:
        return "数据不足"
    
    # 金叉/死叉判断
    if dif.iloc[-1] > dea.iloc[-1] and dif.iloc[-2] <= dea.iloc[-2]:
        return "金叉买入"
    elif dif.iloc[-1] < dea.iloc[-1] and dif.iloc[-2] >= dea.iloc[-2]:
        return "死叉卖出"
    elif dif.iloc[-1] > dea.iloc[-1]:
        if dif.iloc[-1] > 0:
            return "多头强势"
        else:
            return "多头初现"
    else:
        if dif.iloc[-1] < 0:
            return "空头强势"
        else:
            return "空头初现"


def calc_kdj(high: pd.Series, low: pd.Series, close: pd.Series, 
             n: int = 9, m1: int = 3, m2: int = 3) -> dict:
    """计算KDJ指标"""
    low_n = low.rolling(window=n).min()
    high_n = high.rolling(window=n).max()
    rsv = (close - low_n) / (high_n - low_n) * 100
    rsv = rsv.fillna(50)
    
    k = rsv.ewm(com=m1-1, adjust=False).mean()
    d = k.ewm(com=m2-1, adjust=False).mean()
    j = 3 * k - 2 * d
    
    return {
        'K': k,
        'D': d,
        'J': j,
        'signal': get_kdj_signal(k, d)
    }


def get_kdj_signal(k: pd.Series, d: pd.Series) -> str:
    """判断KDJ信号"""
    if len(k) < 2:
        return "数据不足"
    
    k_val = k.iloc[-1]
    
    if k.iloc[-1] > d.iloc[-1] and k.iloc[-2] <= d.iloc[-2]:
        if k_val < 20:
            return "超卖金叉-强买"
        elif k_val < 50:
            return "金叉买入"
        else:
            return "高位金叉"
    elif k.iloc[-1] < d.iloc[-1] and k.iloc[-2] >= d.iloc[-2]:
        if k_val > 80:
            return "超买死叉-强卖"
        elif k_val > 50:
            return "死叉卖出"
        else:
            return "低位死叉"
    elif k_val > 80:
        return "超买区域"
    elif k_val < 20:
        return "超卖区域"
    else:
        return "中性震荡"


def calc_rsi(close: pd.Series, period: int = 14) -> dict:
    """计算RSI指标"""
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return {
        'RSI': rsi,
        'signal': get_rsi_signal(rsi)
    }


def get_rsi_signal(rsi: pd.Series) -> str:
    """判断RSI信号"""
    if len(rsi) < 1:
        return "数据不足"
    
    rsi_val = rsi.iloc[-1]
    
    if rsi_val > 80:
        return "严重超买"
    elif rsi_val > 70:
        return "超买"
    elif rsi_val < 20:
        return "严重超卖"
    elif rsi_val < 30:
        return "超卖"
    else:
        return f"中性({rsi_val:.1f})"


def calc_boll(close: pd.Series, period: int = 20, std_dev: int = 2) -> dict:
    """计算布林带"""
    mid = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()
    upper = mid + std_dev * std
    lower = mid - std_dev * std
    
    return {
        'UPPER': upper,
        'MID': mid,
        'LOWER': lower,
        'signal': get_boll_signal(close, upper, mid, lower)
    }


def get_boll_signal(close: pd.Series, upper: pd.Series, mid: pd.Series, lower: pd.Series) -> str:
    """判断布林带信号"""
    if len(close) < 1:
        return "数据不足"
    
    price = close.iloc[-1]
    u = upper.iloc[-1]
    m = mid.iloc[-1]
    l = lower.iloc[-1]
    
    if price > u:
        return "突破上轨-超买"
    elif price < l:
        return "跌破下轨-超卖"
    elif price > m:
        return "中轨上方-偏多"
    else:
        return "中轨下方-偏空"


def calc_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """计算ATR真实波幅"""
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()


def calc_vol_ma(volume: pd.Series, periods: list = [5, 10, 20]) -> pd.DataFrame:
    """计算成交量均线"""
    vol_df = pd.DataFrame(index=volume.index)
    for p in periods:
        vol_df[f'VOL_MA{p}'] = volume.rolling(window=p).mean()
    return vol_df


def detect_trend(close: pd.Series, ma_short: int = 20, ma_long: int = 60) -> str:
    """判断趋势方向"""
    ma_s = close.rolling(ma_short).mean()
    ma_l = close.rolling(ma_long).mean()
    
    if len(ma_s) < 1 or len(ma_l) < 1:
        return "数据不足"
    
    if ma_s.iloc[-1] > ma_l.iloc[-1] and close.iloc[-1] > ma_s.iloc[-1]:
        return "上升趋势"
    elif ma_s.iloc[-1] < ma_l.iloc[-1] and close.iloc[-1] < ma_s.iloc[-1]:
        return "下降趋势"
    else:
        return "震荡整理"


def find_support_resistance(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 20) -> dict:
    """计算支撑位和阻力位"""
    support = low.rolling(window=period).min().iloc[-1]
    resistance = high.rolling(window=period).max().iloc[-1]
    pivot = (high.iloc[-1] + low.iloc[-1] + close.iloc[-1]) / 3
    
    return {
        'support': round(support, 2),
        'resistance': round(resistance, 2),
        'pivot': round(pivot, 2)
    }


def technical_score(macd_signal: str, kdj_signal: str, rsi_signal: str, 
                    boll_signal: str, trend: str) -> dict:
    """综合技术评分"""
    score = 50  # 基础分
    
    # MACD评分
    if '金叉' in macd_signal or '多头' in macd_signal:
        score += 15
    elif '死叉' in macd_signal or '空头' in macd_signal:
        score -= 15
    
    # KDJ评分
    if '强买' in kdj_signal:
        score += 15
    elif '买入' in kdj_signal:
        score += 10
    elif '强卖' in kdj_signal:
        score -= 15
    elif '卖出' in kdj_signal:
        score -= 10
    
    # RSI评分
    if '超卖' in rsi_signal:
        score += 10
    elif '超买' in rsi_signal:
        score -= 10
    
    # 布林带评分
    if '超卖' in boll_signal:
        score += 10
    elif '超买' in boll_signal:
        score -= 10
    elif '偏多' in boll_signal:
        score += 5
    elif '偏空' in boll_signal:
        score -= 5
    
    # 趋势评分
    if trend == "上升趋势":
        score += 15
    elif trend == "下降趋势":
        score -= 15
    
    # 评级
    if score >= 80:
        rating = "强烈买入"
        stars = 5
    elif score >= 65:
        rating = "买入"
        stars = 4
    elif score >= 50:
        rating = "中性"
        stars = 3
    elif score >= 35:
        rating = "卖出"
        stars = 2
    else:
        rating = "强烈卖出"
        stars = 1
    
    return {
        'score': min(max(score, 0), 100),
        'rating': rating,
        'stars': stars
    }


def analyze_stock(df: pd.DataFrame) -> dict:
    """
    完整技术分析
    
    Args:
        df: 包含 open, high, low, close, volume 的DataFrame
    """
    close = df['收盘'] if '收盘' in df.columns else df['close']
    high = df['最高'] if '最高' in df.columns else df['high']
    low = df['最低'] if '最低' in df.columns else df['low']
    volume = df['成交量'] if '成交量' in df.columns else df['volume']
    
    # 计算各项指标
    ma_data = calc_ma(close)
    macd_data = calc_macd(close)
    kdj_data = calc_kdj(high, low, close)
    rsi_data = calc_rsi(close)
    boll_data = calc_boll(close)
    atr = calc_atr(high, low, close)
    trend = detect_trend(close)
    sr = find_support_resistance(high, low, close)
    
    # 综合评分
    score_data = technical_score(
        macd_data['signal'],
        kdj_data['signal'],
        rsi_data['signal'],
        boll_data['signal'],
        trend
    )
    
    return {
        'price': {
            'current': round(close.iloc[-1], 2),
            'change_pct': round((close.iloc[-1] / close.iloc[-2] - 1) * 100, 2)
        },
        'trend': trend,
        'support_resistance': sr,
        'indicators': {
            'MACD': {
                'DIF': round(macd_data['DIF'].iloc[-1], 4),
                'DEA': round(macd_data['DEA'].iloc[-1], 4),
                'signal': macd_data['signal']
            },
            'KDJ': {
                'K': round(kdj_data['K'].iloc[-1], 2),
                'D': round(kdj_data['D'].iloc[-1], 2),
                'J': round(kdj_data['J'].iloc[-1], 2),
                'signal': kdj_data['signal']
            },
            'RSI': {
                'value': round(rsi_data['RSI'].iloc[-1], 2),
                'signal': rsi_data['signal']
            },
            'BOLL': {
                'upper': round(boll_data['UPPER'].iloc[-1], 2),
                'mid': round(boll_data['MID'].iloc[-1], 2),
                'lower': round(boll_data['LOWER'].iloc[-1], 2),
                'signal': boll_data['signal']
            },
            'ATR': round(atr.iloc[-1], 2)
        },
        'score': score_data
    }


if __name__ == "__main__":
    # 测试
    import akshare as ak
    
    df = ak.stock_zh_a_hist(symbol="000001", period="daily", adjust="qfq")
    df = df.tail(120)
    
    result = analyze_stock(df)
    print("=== 平安银行(000001) 技术分析 ===")
    print(f"当前价格: {result['price']['current']} ({result['price']['change_pct']:+.2f}%)")
    print(f"趋势判断: {result['trend']}")
    print(f"支撑位: {result['support_resistance']['support']} | 阻力位: {result['support_resistance']['resistance']}")
    print(f"\n技术指标:")
    for name, data in result['indicators'].items():
        print(f"  {name}: {data}")
    print(f"\n综合评分: {result['score']['score']} - {result['score']['rating']} ({'⭐' * result['score']['stars']})")
