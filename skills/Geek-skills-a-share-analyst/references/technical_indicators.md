# 技术指标计算公式

## 趋势指标

### MA (移动平均线)
```python
def calc_ma(close, period):
    return close.rolling(window=period).mean()
# 常用周期：MA5, MA10, MA20, MA60, MA120, MA250
```

### EMA (指数移动平均)
```python
def calc_ema(close, period):
    return close.ewm(span=period, adjust=False).mean()
```

### MACD (指数平滑异同移动平均线)
```python
def calc_macd(close, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow  # 快线
    dea = dif.ewm(span=signal, adjust=False).mean()  # 慢线
    macd = (dif - dea) * 2  # 柱状图
    return dif, dea, macd
# 金叉：DIF上穿DEA | 死叉：DIF下穿DEA
```

## 震荡指标

### KDJ (随机指标)
```python
def calc_kdj(high, low, close, n=9, m1=3, m2=3):
    low_n = low.rolling(window=n).min()
    high_n = high.rolling(window=n).max()
    rsv = (close - low_n) / (high_n - low_n) * 100
    k = rsv.ewm(com=m1-1, adjust=False).mean()
    d = k.ewm(com=m2-1, adjust=False).mean()
    j = 3 * k - 2 * d
    return k, d, j
# K>80超买 | K<20超卖 | 金叉：K上穿D
```

### RSI (相对强弱指标)
```python
def calc_rsi(close, period=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
# RSI>70超买 | RSI<30超卖
```

### WR (威廉指标)
```python
def calc_wr(high, low, close, period=14):
    hh = high.rolling(window=period).max()
    ll = low.rolling(window=period).min()
    return -100 * (hh - close) / (hh - ll)
# WR>-20超买 | WR<-80超卖
```

## 波动率指标

### BOLL (布林带)
```python
def calc_boll(close, period=20, std_dev=2):
    mid = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()
    upper = mid + std_dev * std
    lower = mid - std_dev * std
    return upper, mid, lower
# 突破上轨：超买/强势 | 跌破下轨：超卖/弱势
```

### ATR (真实波动幅度)
```python
def calc_atr(high, low, close, period=14):
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()
# 用于止损设置：止损位 = 入场价 - N * ATR
```

## 成交量指标

### OBV (能量潮)
```python
def calc_obv(close, volume):
    direction = np.where(close > close.shift(1), 1, 
                np.where(close < close.shift(1), -1, 0))
    return (direction * volume).cumsum()
# OBV上升趋势配合价格上涨确认趋势
```

### VOL_MA (成交量均线)
```python
def calc_vol_ma(volume, period):
    return volume.rolling(window=period).mean()
# 放量突破：当日成交量 > 2 * VOL_MA5
```

## 形态识别

### 趋势判断
```python
def trend_direction(close, ma_short=20, ma_long=60):
    ma_s = close.rolling(ma_short).mean()
    ma_l = close.rolling(ma_long).mean()
    if ma_s.iloc[-1] > ma_l.iloc[-1] and close.iloc[-1] > ma_s.iloc[-1]:
        return "上升趋势"
    elif ma_s.iloc[-1] < ma_l.iloc[-1] and close.iloc[-1] < ma_s.iloc[-1]:
        return "下降趋势"
    else:
        return "震荡整理"
```

### 支撑阻力位
```python
def support_resistance(high, low, close, period=20):
    support = low.rolling(window=period).min()
    resistance = high.rolling(window=period).max()
    pivot = (high + low + close) / 3
    return support.iloc[-1], resistance.iloc[-1], pivot.iloc[-1]
```

## 信号评分系统

综合评分 = 趋势得分×0.3 + 动量得分×0.3 + 量能得分×0.2 + 波动得分×0.2

| 指标 | 强买入 | 买入 | 中性 | 卖出 | 强卖出 |
|------|--------|------|------|------|--------|
| MACD | DIF>0且金叉 | 金叉 | 中性 | 死叉 | DIF<0且死叉 |
| KDJ | K<20金叉 | K<50金叉 | 40<K<60 | K>50死叉 | K>80死叉 |
| RSI | RSI<30 | 30<RSI<40 | 40<RSI<60 | 60<RSI<70 | RSI>70 |
| BOLL | 下轨反弹 | 中轨支撑 | 中轨附近 | 中轨压力 | 上轨回落 |
